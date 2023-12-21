import os
import sys

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "..", "..", "src"))

from utils import H5Normalizer

normalizer = H5Normalizer(
    os.path.join(root, "..", "..", "data", "chemical_descriptors", "eos8a4x.h5")
)
normalizer.run()

normalizer = H5Normalizer(
    os.path.join(root, "..", "..", "data", "chemical_descriptors", "eos78ao.h5")
)
normalizer.run()
