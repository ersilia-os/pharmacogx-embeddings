python 0_prepare_training_data.py --exp 10
python 0_prepare_training_data.py --only_pk --exp 10
python 0_prepare_training_data.py --only_adme_genes --only_pk --exp 10
python 1_prepare_prediction_input.py 10
python 1_training_data_as_matrix.py 10
python 2_run_training_experiment_miscl.py --only_pk --only_adme_genes --miscl_perc 10
python 2_run_training_experiment_miscl.py --only_pk --miscl_perc 10
python 2_run_training_experiment_miscl.py --miscl_perc 10
python 3_run_prediction_experiment_chunks.py 10
python 4_annotate_variants.py 10
python 5_merge_results.py 10

python 0_prepare_training_data.py --exp 20
python 0_prepare_training_data.py --only_pk --exp 20
python 0_prepare_training_data.py --only_adme_genes --only_pk --exp 20
python 1_prepare_prediction_input.py 20
python 1_training_data_as_matrix.py 20
python 2_run_training_experiment_miscl.py --only_pk --only_adme_genes --miscl_perc 20
python 2_run_training_experiment_miscl.py --only_pk --miscl_perc 20
python 2_run_training_experiment_miscl.py --miscl_perc 20
python 3_run_prediction_experiment_chunks.py 20
python 4_annotate_variants.py 20
python 5_merge_results.py 20

python 0_prepare_training_data.py --exp 50
python 0_prepare_training_data.py --only_pk --exp 50
python 0_prepare_training_data.py --only_adme_genes --only_pk --exp 50
python 1_prepare_prediction_input.py 50
python 1_training_data_as_matrix.py 50
python 2_run_training_experiment_miscl.py --only_pk --only_adme_genes --miscl_perc 50
python 2_run_training_experiment_miscl.py --only_pk --miscl_perc 50
python 2_run_training_experiment_miscl.py --miscl_perc 50
python 3_run_prediction_experiment_chunks.py 50
python 4_annotate_variants.py 50
python 5_merge_results.py 50