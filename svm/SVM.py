# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import cv2
import torch

# df1 = pd.read_csv("projet-soudures/data/raw/welddb.data", header=None, sep=" ")
welddb_df = pd.read_csv("projet-soudures/data/raw/welddb.data", header=None, sep=r"\s+") # On importe la base de donnée avec la librairie pandas et on définit ni intitulé de colonnes, ni séparateurs
print(welddb_df.shape) # Taille du tableau extrait
welddb_df

print(welddb_df.isna().sum().sum()) # On regarde le nombre de NAN dans la base de données (=0)

# %% Nous allons implémenter un algorithme de SVM (Supervisé) et un algo
