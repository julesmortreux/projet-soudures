"""Fonctions partagées par les notebooks : groupes, cible et préparation."""
import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CATEGORIES = ['AC_DC', 'Electrode_pol', 'WeldType']
MESURES = ['UTS_MPa', 'Elongation_pct']


def poids_groupes(groupes):
    """Donner un poids total de 1 à chaque groupe."""
    return (1 / groupes.map(groupes.value_counts())).to_numpy(dtype=float)


def reference_rangs(valeurs, groupes_apprentissage):
    """Calculer les mi-rangs pondérés sur l’apprentissage uniquement."""
    tableau = pd.DataFrame({'valeur': valeurs, 'poids': poids_groupes(groupes_apprentissage)})
    masse = tableau.groupby('valeur')['poids'].sum()
    rangs = (masse.cumsum() - masse / 2) / masse.sum()
    return masse.index.to_numpy(), rangs.to_numpy()


def calculer_cible(Y_apprentissage, groupes_apprentissage, Y_a_transformer):
    """Combiner les rangs UTS et allongement avec des poids égaux."""
    rangs = pd.DataFrame(index=Y_a_transformer.index)
    for mesure in MESURES:
        valeurs, positions = reference_rangs(Y_apprentissage[mesure], groupes_apprentissage)
        rangs[mesure] = np.interp(Y_a_transformer[mesure], valeurs, positions)
    return np.sqrt(rangs.prod(axis=1))


def creer_preparation(X_apprentissage, seuil=0.25, normaliser=True):
    """Choisir les colonnes sur l’apprentissage et créer leur traitement.

    Renvoie le prétraitement et la liste des colonnes gardées.
    Les médianes et catégories seront apprises lors de fit, pas ici.
    """
    taux = X_apprentissage.notna().mean()
    gardees = taux[taux >= seuil].index.tolist()
    numeriques = [c for c in gardees if c not in CATEGORIES]
    categorielles = [c for c in gardees if c in CATEGORIES]
    etapes_numeriques = [('mediane', SimpleImputer(strategy='median'))]
    if normaliser:
        etapes_numeriques.append(('standardisation', StandardScaler()))
    traitement_categories = Pipeline([
        ('manquants', SimpleImputer(strategy='constant', fill_value='manquant')),
        ('encodage', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))
    ])
    preparation = ColumnTransformer([
        ('nombres', Pipeline(etapes_numeriques), numeriques),
        ('categories', traitement_categories, categorielles)
    ])
    return preparation, gardees


def creer_pipeline(X_apprentissage, modele, normaliser=False, cache=None):
    """Enchaîner la préparation et le modèle ; sans standardisation pour les arbres."""
    preparation, _ = creer_preparation(X_apprentissage, normaliser=normaliser)
    return Pipeline([
        ('preparation', preparation),
        ('modele', clone(modele))
    ], memory=cache)
