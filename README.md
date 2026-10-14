# Prédiction de la qualité de soudures

Projet **3IF3010 - Apprentissage automatique** · CentraleSupélec 3A Mention IA
Rendu : **12 octobre 2026**

## Le rendu, en trois liens

| Quoi | Où |
|---|---|
| **Le rapport, cinq pages** | [`rapport/rapport.md`](rapport/rapport.md) |
| **Le diagramme de Gantt et la répartition des tâches** | [`rapport/gantt.md`](rapport/gantt.md) |
| **Les sept notebooks à lire, dans l'ordre** | [`notebooks/rendu/`](notebooks/rendu/) |

**Reproductibilité vérifiée.** Les sept notebooks de `notebooks/rendu/`
s'exécutent depuis un clone vierge de ce dépôt, sans aucune erreur, en
**26 minutes au total**. Il suffit de `pip install -r requirements.txt` puis de
lancer le notebook 1 en premier.

## Équipe

| Nom | Mail | GitHub |
|---|---|---|
| Jules Mortreux |jules.mortreux@student-cs.fr|@julesmortreux |
| Marie Gozlan | marie.gozlan@student-cs.fr | @MarieGozlan |
| Pétronille Tard | petronille.tard@student-cs.fr | @petronilletard |
| Grégoire Pascual | gregoire.pascual@student-cs.fr | @GregP14 |

Pas de numéro d'équipe. Marie est en **groupe de TD 1**, les trois autres en
**groupe 2** : l'équipe est à cheval sur les deux groupes.

## Objectif

Prédire la qualité de soudures sur aciers à partir de la composition chimique
et des paramètres du procédé de soudage.

**Attention : aucune variable du jeu de données ne mesure directement la « qualité ».**
Plusieurs propriétés mécaniques en sont des indicateurs. Définir la cible fait
partie du travail.

## Données

`welddb` - MAP Data Library, University of Cambridge
<https://www.phase-trans.msm.cam.ac.uk/map/data/materials/welddb-b.html>

**1652 soudures × 44 variables.** Fichier brut versionné dans `data/raw/`,
description des colonnes dans `data/raw/welddb.info`.

Dans le fichier brut, **`N` signifie « non renseigné », pas zéro.**

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Structure

```
data/raw/          données brutes , ne pas modifier
data/processed/    données nettoyées (non versionné)
notebooks/         notebooks d'exploration, numérotés 01 à 15
notebooks/rendu/   la série propre à lire en premier, 1 à 7
src/               code réutilisable (.py)
figures/           figures pour le rapport
biblio/            références
rapport/           rapport final + Gantt
```

### Par où commencer

Lire **`notebooks/rendu/`** dans l'ordre 1 à 7 : cette série reprend les
meilleurs choix issus de l'exploration, en expliquant chaque fois pourquoi, et
renvoie aux notebooks d'exploration quand le détail y est. Les notebooks `01` à
`15` à la racine de `notebooks/` sont cette exploration, dans l'ordre
chronologique où elle a été menée.

**Le notebook de rendu 1 doit être exécuté en premier**, car il régénère
`data/processed/`, que le `.gitignore` exclut volontairement, et dont le
notebook 6 a besoin. Les notebooks 3, 4, 5 et 7 lisent les sorties du
notebook 2, et le 7 lit en plus celles des notebooks 4, 5 et 6.

### L'état des notebooks d'exploration

Les quinze notebooks `01` à `15` sont conservés **comme trace de ce qui a été
essayé**, y compris les pistes écartées. Ils ne constituent pas le rendu, et
deux d'entre eux ne s'exécutent pas en l'état :

| Notebook | État | Pourquoi |
|---|---|---|
| `06_modeles_lineaires_knn` | sans sorties | il contient une assertion de cohérence avec les sorties du notebook `05`, et elle échoue : les plis calculés ne reproduisent pas ceux sauvegardés |
| `07_kmeans` | sans sorties | incompatibilité avec la version de pandas installée, sur un `groupby.apply` |

**Leurs résultats existent néanmoins** dans `outputs/06/` et `outputs/07/`, et
les notions qu'ils traitent sont reprises, vérifiées et exécutées dans la série
de rendu : les modèles linéaires et le k plus proches voisins au notebook 4, le
partitionnement par k-moyennes au notebook 3.

**Attention aux numéros des dossiers de sorties des notebooks
d'exploration.** Ils n'ont pas été renumérotés lorsque les notebooks l'ont été,
il y a donc un décalage de trois :

| Notebook d'exploration | Écrit dans |
|---|---|
| `11_comparaison_cibles` | `outputs/08/` |
| `12_reentrainement_cible_y3` | `outputs/09/` |
| `13_modeles_par_propriete` | `outputs/10/` |
| `14_selection_variables` | `outputs/11/` |
| `15_classification` | `outputs/12/` |

Les notebooks `01` à `07` et ceux de `notebooks/rendu/` n'ont pas ce décalage.

## Organisation du travail

- une branche par tâche : `feat/prenom-sujet`
- pas de push direct sur `main`, passer par une pull request
- **vider les sorties des notebooks avant de committer**
  (`Kernel > Restart & Clear All Outputs`)
- une **issue GitHub par tâche**, assignée à une personne
  → sert à construire le diagramme de Gantt exigé dans le rapport

## Avancement

- [x] structure du projet et données
- [x] compléter l'équipe ci-dessus
- [x] analyse descriptive et pré-traitement → `notebooks/rendu/1_donnees`
- [x] définir la cible « qualité de soudure » → `notebooks/rendu/2_cible`
- [x] ACP → `notebooks/rendu/3_preparation_exploration`
- [x] partitionnement par k-moyennes → `notebooks/rendu/3_preparation_exploration`
- [x] modèles supervisés + validation croisée → `notebooks/rendu/4_modelisation`
- [x] comparaison des performances → `notebooks/rendu/4_modelisation`
- [x] classification et sélection de variables → `notebooks/rendu/5_classification_selection`
- [x] une méthode semi-supervisée → `notebooks/rendu/6_semi_supervise`
- [x] synthèse et recommandations → `notebooks/rendu/7_synthese_recommandations`
- [x] bibliographie : 13 références citées dans le texte du rapport
- [x] bibliographie commentée dans `biblio/README.md`
- [x] rapport 5 pages + Gantt → `rapport/rapport.md`, `rapport/gantt.md`
- [x] charges par tâche du Gantt, estimées et à valider par chacun
