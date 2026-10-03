# Prediction de la qualite de soudures

Projet **3IF3010 - Apprentissage automatique**, CentraleSupelec 3A Mention IA
Rendu : **12 octobre 2026**

## Equipe

| Nom | Mail | GitHub |
|---|---|---|
| Jules Mortreux | | |
| | | |
| | | |
| | | |

Numero d'equipe : *a completer* - Groupe de TD : *a completer*

## Objectif

Predire la qualite de soudures sur aciers a partir de la composition chimique
et des parametres du procede de soudage.

Attention : **aucune variable du jeu de donnees ne mesure directement la
"qualite".** Plusieurs proprietes mecaniques en sont des indicateurs. Definir
la cible fait partie du travail.

## Donnees

`welddb`, MAP Data Library, University of Cambridge
<https://www.phase-trans.msm.cam.ac.uk/map/data/materials/welddb-b.html>

**1652 soudures x 44 variables.** Fichier brut versionne dans `data/raw/`,
description des colonnes dans `data/raw/welddb.info`.

Points a connaitre avant de manipuler ces donnees :

- Dans le fichier brut, **`N` signifie "non renseigne", pas zero.** La
  documentation officielle le precise explicitement.
- Les 1652 lignes ne correspondent qu'a **624 soudures physiques distinctes** :
  une meme soudure apparait plusieurs fois, avec des traitements thermiques et
  des essais differents. Les lignes ne sont donc pas independantes, ce qui
  impose de **grouper par soudure lors de la validation croisee**
  (`GroupKFold` plutot que `KFold`), sous peine de fuite de donnees.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Structure

```
data/raw/          donnees brutes, ne pas modifier
data/processed/    donnees nettoyees (non versionne)
notebooks/         analyses
src/               code reutilisable (.py)
figures/           figures pour le rapport
biblio/            references
rapport/           rapport final et diagramme de Gantt
```

Le code qui sert a plusieurs endroits va dans `src/`, pas dans un notebook :
les fichiers `.py` se fusionnent proprement dans Git, les `.ipynb` non.

## Organisation du travail

- une branche par tache : `feat/prenom-sujet`, ou `explo/prenom` pour
  l'exploration
- pas de push direct sur `main`, passer par une pull request relue par un
  coequipier
- une **issue GitHub par tache**, assignee a une personne : les dates
  d'ouverture et de fermeture servent a construire le diagramme de Gantt exige
  dans le rapport

### Sorties des notebooks

**On garde les sorties des notebooks dans Git.** GitHub affiche les notebooks
avec leurs resultats : les conserver permet de lire l'analyse directement en
ligne, sans rien executer.

Seule exception : si plusieurs personnes editent **le meme** notebook, videz
les sorties avant de committer (`Kernel > Restart and Clear All Outputs`), car
les sorties generent des conflits de fusion illisibles. Tant que chacun
travaille sur son propre notebook, le probleme ne se pose pas.

## Avancement

- [x] structure du projet et donnees
- [ ] completer l'equipe ci-dessus
- [ ] analyse descriptive et pre-traitement
- [ ] ACP
- [ ] definir la cible "qualite de soudure"
- [ ] selection de variables
- [ ] modeles supervises et validation croisee
- [ ] une methode semi-supervisee et bibliographie
- [ ] comparaison des performances
- [ ] rapport 5 pages et Gantt

## References

1. T. Cool, *Design of Steel Weld Deposits*, PhD Thesis, University of
   Cambridge, 1996.
2. T. Cool, H. K. D. H. Bhadeshia, D. J. C. MacKay, *Materials Science and
   Engineering*, 1997.
3. MAP Data Library, `MAP_DATA_WELD`, University of Cambridge.
