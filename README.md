# Prédiction de la qualité de soudures

Projet **3IF3010 - Apprentissage automatique** · CentraleSupélec 3A Mention IA
Rendu : **12 octobre 2026**

## Équipe

| Nom | Mail | GitHub |
|---|---|---|
| Jules Mortreux |jules.mortreux@student-cs.fr|@julesmortreux |
| Marie Gozlan | marie.gozlan@student-cs.fr | @MarieGozlan |
| Pétronille Tard | petronille.tard@student-cs.fr | @petronilletard |
| | | |

Numéro d'équipe : *à compléter* · Groupe de TD : *à compléter*

## Objectif

Prédire la qualité de soudures sur aciers à partir de la composition chimique
et des paramètres du procédé de soudage.

⚠️ **Aucune variable du jeu de données ne mesure directement la « qualité ».**
Plusieurs propriétés mécaniques en sont des indicateurs. Définir la cible fait
partie du travail.

## Données

`welddb` - MAP Data Library, University of Cambridge
<https://www.phase-trans.msm.cam.ac.uk/map/data/materials/welddb-b.html>

**1652 soudures × 44 variables.** Fichier brut versionné dans `data/raw/`,
description des colonnes dans `data/raw/welddb.info`.

⚠️ Dans le fichier brut, **`N` signifie « non renseigné », pas zéro.**

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Structure

```
data/raw/          données brutes — ne pas modifier
data/processed/    données nettoyées (non versionné)
notebooks/         analyses
src/               code réutilisable (.py)
figures/           figures pour le rapport
biblio/            références
rapport/           rapport final + Gantt
```

## Organisation du travail

- une branche par tâche : `feat/prenom-sujet`
- pas de push direct sur `main`, passer par une pull request
- **vider les sorties des notebooks avant de committer**
  (`Kernel > Restart & Clear All Outputs`)
- une **issue GitHub par tâche**, assignée à une personne
  → sert à construire le diagramme de Gantt exigé dans le rapport

## À faire

- [ ] compléter l'équipe ci-dessus
- [ ] analyse descriptive et pré-traitement
- [ ] ACP
- [ ] définir la cible « qualité de soudure »
- [ ] modèles supervisés + validation croisée
- [ ] une méthode semi-supervisée (+ biblio)
- [ ] comparaison des performances
- [ ] rapport 5 pages + Gantt
