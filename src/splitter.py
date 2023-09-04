# for now, check the AI notebook

import pandas as pd
import numpy as np
import random
from rdkit import Chem
from tqdm import tqdm
from sklearn.metrics import roc_auc_score
import sys
from lol import LOL
from rdkit import RDLogger 
RDLogger.DisableLog('rdApp.*')