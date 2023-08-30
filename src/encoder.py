import numpy as np
import pandas as pd
import gc

gc.enable()
import h5py

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.backend import clear_session, set_session, get_session
from tensorflow.keras.optimizers import Adam

import tensorflow as tf

tf.keras.mixed_precision.set_global_policy("mixed_float16")

import optuna


LATENT_DIM = (
    512  # TODO Check Ligand Discovery project, where this was initially developed.
)
BATCH_SIZE = 1024


def reset_keras():
    sess = get_session()
    clear_session()
    sess.close()
    sess = get_session()
    print(gc.collect())
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 1
    config.gpu_options.visible_device_list = "0"
    set_session(tf.compat.v1.Session(config=config))


def get_layer_sizes(num_layers, endpoint_dim):
    v = np.linspace(endpoint_dim, LATENT_DIM, num_layers + 2)[1:-1]
    return [int(x) for x in v]


def start_encoder(h5_data, trials, epochs, timeout, skip_optuna_with_params=None):
    with h5py.File(h5_data, "r") as f:
        input_dim = f["Y"].shape[1]
        output_dim = f["X"].shape[1]

    def read_hdf5_data(mode):
        if mode is None:
            suffix = ""
        else:
            suffix = "_{0}".format(mode)
        with h5py.File(h5_data, "r") as f:
            input_features = f["Y" + suffix][:]
            output_features = f["X" + suffix][:]
        return input_features, output_features

    input_features, output_features = read_hdf5_data(mode=None)

    def create_model(activation, layers_num, dropout_prob, kernel_initializer):
        reset_keras()
        encoder = Sequential()
        the_sizes = get_layer_sizes(layers_num, input_dim)
        for i in range(layers_num, 0, -1):
            encoder.add(
                Dense(
                    the_sizes[-i],
                    input_shape=(input_dim,),
                    activation=activation,
                    kernel_initializer=kernel_initializer,
                    name="encoder" + str(layers_num - i),
                )
            )
            if i == layers_num:
                encoder.add(Dropout(dropout_prob))

        encoder.add(
            Dense(
                LATENT_DIM,
                activation=activation,
                kernel_initializer=kernel_initializer,
                name="bottleneck" + str(layers_num),
            )
        )

        the_sizes = get_layer_sizes(layers_num, output_dim)
        for i in range(1, layers_num + 1):
            encoder.add(
                Dense(
                    the_sizes[-i],
                    activation=activation,
                    kernel_initializer=kernel_initializer,
                    name="decoder" + str(i + layers_num),
                )
            )
            if i == layers_num - 1:
                encoder.add(Dropout(dropout_prob))

        encoder.add(
            Dense(
                output_dim,
                activation=activation,
                kernel_initializer="normal",
                name="output",
            )
        )
        return encoder

    if skip_optuna_with_params is None:

        def objective(trial):
            activation = trial.suggest_categorical("activation", ["relu", "swish"])
            layers_num = trial.suggest_int("layers_num", 1, 5, 1)
            dropout_rate = trial.suggest_float("dropout_prob", 0.1, 0.5, step=0.1)
            learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-1, log=True)
            epsilon = trial.suggest_float("epsilon", 1e-7, 1.0, log=True)

            optimizer = Adam(learning_rate=learning_rate, epsilon=epsilon)

            if activation == "relu":
                model = create_model(
                    activation, layers_num, dropout_rate, kernel_initializer="HeNormal"
                )
            else:
                model = create_model(
                    activation,
                    layers_num,
                    dropout_rate,
                    kernel_initializer="GlorotNormal",
                )
            model.compile(optimizer=optimizer, loss="mse")
            callback = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=10)
            history = model.fit(
                input_features,
                output_features,
                batch_size=BATCH_SIZE,
                epochs=epochs,
                callbacks=[callback],
                verbose=2,
            )
            gc.collect()
            return history.history["loss"][-1]

        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=trials, timeout=timeout)

    else:

        class Study:
            def __init__(self):
                self.best_params = skip_optuna_with_params

        study = Study()

    print("Best hyperparams found by Optuna: \n", study.best_params)
    if study.best_params["activation"] == "relu":
        model = create_model(
            study.best_params["activation"],
            int(study.best_params["layers_num"]),
            study.best_params["dropout_prob"],
            kernel_initializer="HeUniform",
        )
    else:
        model = create_model(
            study.best_params["activation"],
            int(study.best_params["layers_num"]),
            study.best_params["dropout_prob"],
            kernel_initializer="GlorotUniform",
        )
    optimizer = Adam(
        learning_rate=study.best_params["learning_rate"],
        epsilon=study.best_params["epsilon"],
    )
    model.compile(loss="mse")
    model.summary()
    callback = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=10)
    history = model.fit(
        input_features,
        output_features,
        batch_size=BATCH_SIZE,
        epochs=int(epochs * 3),
        callbacks=[callback],
        verbose=2,
    )
    print(pd.DataFrame(history.history))
    feature_extractor = keras.Model(
        inputs=model.inputs,
        outputs=model.get_layer(
            name="bottleneck" + str(study.best_params["layers_num"])
        ).output,
    )
    feature_extractor.compile(optimizer=optimizer, loss="mse")
    return feature_extractor, study.best_params
