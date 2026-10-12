# Prédiction de la qualité de soudures sur aciers

**Équipe n° [A COMPLETER]** · Groupe de TD [A COMPLETER] · 12 octobre 2026

3IF3010 Apprentissage automatique · CentraleSupélec 3A, Mention IA

| Membre | Adresse |
|---|---|
| Marie Gozlan | marie.gozlan@student-cs.fr |
| Jules Mortreux | jules.mortreux@student-cs.fr |
| Grégoire Pascual | gregoire.pascual@student-cs.fr |
| Pétronille Tard | petronille.tard@student-cs.fr |

Dépôt : `github.com/julesmortreux/projet-soudures`. La série `notebooks/rendu/`
(1 à 7) présente la chaîne retenue et renvoie aux notebooks d'exploration
`notebooks/01` à `15` pour le détail des pistes essayées.

---

## 1. Le problème, et la difficulté qu'il cache

Le jeu `welddb` [1, 13] décrit 1652 essais sur soudures d'acier, caractérisées
par leur composition chimique et les paramètres du procédé de soudage. L'enjeu
posé par l'énoncé n'est pas de livrer un prédicteur mais **d'extraire de la
connaissance** : la qualité d'une soudure se transmet aujourd'hui d'expert à
expert, et l'objectif est d'en retrouver les déterminants dans les données.
Ce cadrage a gouverné nos choix, et nous y revenons en conclusion.

**Aucune colonne ne mesure la qualité.** Cinq propriétés mécaniques en sont des
indicateurs : limite d'élasticité, résistance à la traction, allongement,
striction, et résilience Charpy. Définir la cible faisait donc partie du
travail, et c'est la décision qui a le plus pesé sur le résultat.

Deux autres caractéristiques du corpus ont structuré toute la démarche.

**45,6 % de valeurs manquantes, organisées par blocs.** Le mécanisme n'est pas
aléatoire au sens strict mais conditionnellement aléatoire [9] : un laboratoire
qui réalise des essais de traction ne réalise généralement pas d'essais de
résilience. L'absence porte donc de l'information, et elle interdit de
supprimer les lignes incomplètes.

**Les 1652 lignes ne décrivent que 624 soudures distinctes.** Une même soudure
apparaît plusieurs fois, avec des traitements thermiques et des essais
différents. Les lignes ne sont donc pas indépendantes.

## 2. Construire la cible, sans jamais regarder un modèle

**L'observation qui décide de tout.** Résistance et ductilité sont fortement
anticorrélées sur ce corpus, jusqu'à **-0,76**. Durcir un acier le rend plus
résistant et moins déformable. Une bonne soudure n'est donc pas celle qui
maximise une propriété, c'est celle qui réalise un **compromis acceptable**.
Toute cible fondée sur une seule famille récompensera mécaniquement les
soudures médiocres dans l'autre.

**La construction.** Chaque mesure est convertie en **rang entre 0 et 1**, ce
qui supprime les unités et rend le résultat insensible aux valeurs extrêmes.
Les rangs sont pondérés par l'inverse du nombre de lignes de chaque soudure,
pour qu'une soudure testée vingt fois ne pèse pas vingt fois. Les deux familles
sont ensuite combinées par **moyenne géométrique**, qui pénalise les profils
déséquilibrés : des rangs de 0,9 et 0,1 donnent 0,30 au lieu de 0,50.

**Le choix entre cinq définitions candidates s'est fait sans aucun modèle.**
Choisir sur la performance serait circulaire, puisque la performance mesure la
prévisibilité d'une grandeur et non sa pertinence. Nous avons donc comparé les
cinq candidates sur quatre critères indépendants de tout apprentissage :
couverture du corpus, accord entre définitions, cohérence physique du meilleur
cinquième, et robustesse au rééchantillonnage au niveau de la soudure.

> **Le résultat qui justifie cette précaution.** La cible fondée sur la
> résistance seule est **la mieux prédite de toutes** et **la pire
> définition** : son meilleur cinquième réunit les soudures les moins ductiles
> du corpus, avec des rangs d'allongement et de striction sous la médiane. Un
> projet qui aurait choisi sa cible sur les performances aurait livré un
> excellent modèle recommandant des soudures fragiles.

La cible retenue est la moyenne géométrique du rang moyen de résistance et du
rang moyen de ductilité, sur les quatre propriétés de traction. C'est la seule
des cinq dont le meilleur cinquième est au-dessus de la médiane sur les cinq
propriétés mesurées, y compris celles qu'elle n'utilise pas. La résilience
Charpy est traitée à part, car les essais Charpy et de traction portent sur des
soudures largement différentes et la résilience dépend trop de la température
d'essai pour être comparée hors de ses bandes de température.

## 3. Le protocole d'évaluation, et la fuite évitée

**Les lignes n'étant pas indépendantes, une validation croisée ordinaire est
invalide.** Nous l'avons quantifié : avec un découpage au hasard, **81,4 % des
lignes de validation appartiennent à une soudure déjà vue en apprentissage**.
Le modèle voit donc la réponse avant d'être évalué. Avec un découpage par
groupes, ce chevauchement tombe à 0 %.

Toute la chaîne repose donc sur `GroupKFold` à cinq plis, une pondération de
chaque ligne par l'inverse du nombre de lignes de sa soudure, et un
`Pipeline` [8] qui réajuste imputation, encodage et mise à l'échelle **dans
chaque pli**, ce qui rend la fuite impossible par construction. Un ensemble de
test de 123 lignes et 93 soudures a été réservé par découpage par groupes.

**Les métriques**, pour `n` observations de valeur réelle `y`, de prédiction `p`
et de poids `w` :

```
RMSE  =  racine( somme( w (y - p)^2 ) / somme(w) )
MAE   =  somme( w |y - p| ) / somme(w)
R2    =  1  -  somme( w (y - p)^2 ) / somme( w (y - moyenne ponderee de y)^2 )
gain  =  1  -  RMSE du modele / RMSE d'un predicteur constant appris sur l'apprentissage
```

Le **gain** est notre critère de lecture principal : il est sans unité, donc
comparable entre propriétés d'unités différentes, et il se compare à une
référence ajustée sur l'apprentissage seul, ce qui correspond à la situation
réelle d'un modèle déployé.

**Effet de l'imputation, vérifié et non supposé.** Remplacer les valeurs
absentes par une constante contracte l'écart-type et les corrélations d'un
facteur `racine(p)`, où `p` est la part observée ; nous avons vérifié cette
relation sur 26 colonnes, avec une corrélation de 0,998. Le coût est réel pour
l'exploration, une simulation à données constantes faisant chuter la variance
des deux premiers axes d'ACP de 48,2 % à 31 %, mais nul pour la prédiction.

## 4. Les modèles

**Onze familles, 657 configurations** évaluées sur la cible, toutes sur les
mêmes plis. Résultats en validation croisée par groupes :

| Famille | Gain | R2 | Écart-type entre plis |
|---|---|---|---|
| SVM à noyau gaussien [5] | **38,9 %** | 0,611 | 0,012 |
| Forêt aléatoire [3] | 38,0 % | 0,601 | 0,010 |
| Boosting de gradient [4] | 37,5 % | 0,593 | 0,008 |
| Bagging [2] | 37,0 % | 0,589 | 0,010 |
| k plus proches voisins | 31,4 % | 0,512 | 0,006 |
| Ridge | 25,7 % | 0,428 | 0,012 |
| Lasso [6] | 25,2 % | 0,416 | 0,012 |
| Arbre de décision | 22,4 % | 0,376 | 0,008 |
| Régression linéaire | 21,0 % | 0,358 | 0,018 |
| Référence (moyenne) | 0 % | -0,026 | 0,012 |

> **La coupure n'est pas entre familles, elle est entre linéaire et non
> linéaire.** Les quatre premières se tiennent dans un intervalle plus petit
> que leur écart-type entre plis : les désigner l'une meilleure que l'autre
> serait abusif. Ce qui compte sur ce problème est la capacité à représenter
> des effets non linéaires, et non le choix d'une famille particulière.

**Le réglage des hyperparamètres** a été conduit famille par famille, avec deux
précautions. Pour le bagging et la forêt, le nombre d'arbres se règle
séparément, puisqu'en ajouter ne dégrade jamais. Pour le boosting, **le taux
d'apprentissage et le nombre d'itérations se compensent directement et ont donc
été explorés conjointement** sur une grille logarithmique. Chaque
hyperparamètre retenu a ensuite été comparé aux bornes de sa grille ; trois cas
restent à élargir et sont inscrits dans les limites.

**Prédire les quatre propriétés séparément plutôt que le score agrégé.** Le
SVM obtient la plus petite erreur sur chacune des quatre, avec la cible
standardisée pour que son paramètre `epsilon`, exprimé dans l'unité de la
cible, garde le même sens d'une propriété à l'autre.

| Propriété | Unité | R2 (validation croisée) | Gain | R2 (test) |
|---|---|---|---|---|
| Résistance à la traction | MPa | 0,844 | 61,9 % | 0,883 |
| Allongement | % | 0,772 | 52,6 % | 0,658 |
| Limite d'élasticité | MPa | 0,722 | 50,9 % | 0,666 |
| Striction | % | 0,721 | 48,6 % | 0,736 |

Ce classement **ne sépare pas la résistance de la ductilité**, contrairement à
ce que l'on attendrait si la composition d'alliage, bien renseignée, expliquait
la première et la propreté du métal, mal renseignée, la seconde. L'allongement,
qui mesure la ductilité, devance la limite d'élasticité, qui mesure la
résistance. Seuls les deux extrêmes se détachent, et nous présentons donc
l'hypothèse métallurgique comme une piste et non comme un résultat.

**Le coût de cette décomposition est de 2,1 points de gain** sur le score
recomposé, soit environ le quart de l'écart-type entre plis, donc un écart non
établi statistiquement mais non nul. Ce que ce coût achète : quatre valeurs en
**unités physiques** qu'un expert peut valider, la position de la soudure sur
l'arbitrage résistance contre ductilité, de 7 à 20 % de lignes exploitables en
plus par propriété, et un contrôle de cohérence physique sur les sorties. Pour
un projet dont l'objectif est l'extraction de connaissance, nous jugeons
l'échange favorable.

**Sur l'ensemble de test**, le score recomposé obtient 44,3 % de gain, soit
mieux que l'estimation par validation croisée. Les modèles finaux apprennent
sur un quart de données en plus, le test ne compte que 93 soudures, et deux des
quatre propriétés y font d'ailleurs moins bien. **Le chiffre à annoncer est
donc celui de la validation croisée**, plus prudent ; le test confirme
l'absence de surajustement de notre procédure de sélection, ce qui était son
rôle.

## 5. Classification, sélection de variables, semi-supervisé

**Classification en trois niveaux de qualité.** Cinq approches comparées, dont
une décomposition ordinale par classifieurs binaires emboîtés et une régression
suivie d'un seuillage. Les **F1 macro sont indistinguables**, de 0,657 à 0,677.
Ce qui les sépare est le nombre d'**erreurs graves**, les confusions entre
classes extrêmes : de 14 pour le boosting ordinal à 32 pour le boosting direct.
Aucune métrique de classification usuelle ne tient compte de l'ordre des
classes, et c'est pourtant ce critère qui départage ici.

**Sélection de variables.** Le meilleur sous-ensemble parmi 34 colonnes
demanderait 2^34, soit plus de 17 milliards de modèles, donc nous avons utilisé
la sélection ascendante et l'élimination descendante, avec Cp, AIC, BIC et R2
ajusté, puis la validation croisée [11]. Le minimum est atteint par le modèle
complet, mais **la règle de l'écart-type retient 7 variables pour 3,2 %
d'erreur en plus**. Vingt-sept variables de moins pour trois pourcents : c'est
l'arbitrage que cette règle permet d'expliciter.

**Méthode semi-supervisée.** 771 lignes ont des entrées complètes sans cible
calculable. Nous avons implémenté une ridge régularisée par le laplacien d'un
graphe de voisinage [7], semi-supervisée mais **inductive**, donc capable de
prédire un point nouveau, contrairement à une propagation d'étiquettes. Le gain
dépend de la rareté des étiquettes, comme la théorie le prévoit : **+9,7 % avec
un dixième des soudures étiquetées, +1,1 % avec toutes**. Sur notre corpus
complet, l'écart entre supervisé et semi-supervisé est de l'ordre du quart de
pourcent, alors que l'écart entre un modèle linéaire et un modèle non linéaire
est de 21,7 %. **Ce n'est donc pas la supervision qui limite ici, c'est la
classe de modèle.**

**Non supervisé.** Un partitionnement par k-moyennes, avec choix de `k` par
silhouette [10] croisée avec la stabilité au rééchantillonnage, ne retrouve pas
les niveaux de qualité : prédire la moyenne de son groupe ne gagne que 4 % sur
la référence, contre 39 % pour un modèle supervisé. **C'est un résultat
négatif, et c'en est un** : les regroupements naturels des soudures ne sont pas
des regroupements de qualité, parce que ce sont des détails du procédé et du
traitement thermique qui tranchent entre deux compositions voisines.

## 6. Conclusions et recommandations

**L'approche retenue** est un modèle par propriété mécanique, de la famille SVM
à noyau gaussien avec cible standardisée, et le score de qualité recalculé à
partir des quatre prédictions. Performance annoncée : **38,9 % de gain sur une
référence constante**, en validation croisée par groupes.

Nous graduons les recommandations par niveau de confiance, car présenter sur le
même plan ce qui est établi et ce qui est suggéré serait trompeur.

**Niveau 1, établi.** La **teneur en manganèse**, désignée par les quatre
déterminations indépendantes sur quatre : importance par permutation [12],
sélection ascendante stable sur les cinq plis, Lasso, et arbre lisible. Son
effet est important, le score prédit passant de 0,16 à 0,38 entre 0,6 et 1,8 %
de manganèse. L'**énergie de soudage** l'est par trois sur quatre, avec un
effet monotone de 0,41 à 0,32 entre 0,6 et 3,5 kJ/mm. La méthode dissidente est
l'importance par permutation, qui la classe au rang 14 sur 30 : cette mesure
dilue les variables corrélées, et l'énergie de soudage est une grandeur que
nous avons construite à partir de la tension, de l'intensité et de la vitesse,
l'intensité figurant au rang 8 de la même liste.

**Niveau 2, suggéré sans pouvoir les séparer.** Le traitement thermique
post-soudage en température et en durée, le silicium, le titane et le carbone.
Leur ordre change d'un rééchantillonnage à l'autre. Le traitement thermique
mérite une mention particulière : c'est le seul levier disponible **après** que
la soudure a été réalisée.

**Niveau 3, à éviter.** Ne pas optimiser une seule propriété, pour la raison
établie en section 2. Ne pas traiter ces résultats comme des effets causaux :
ce sont des associations observées dans un corpus de résultats publiés, et leur
validation demande une expérience à un paramètre variable. Ne pas utiliser le
modèle pour chercher des soudures exceptionnelles, car il est le moins fiable
sur les cas extrêmes par contraction vers la moyenne.

**La validation la plus convaincante est venue de l'extérieur des données.** Le
modèle a retrouvé seul des régularités que la métallurgie connaît déjà [1] sans
qu'on les lui ait fournies : plus de manganèse améliore, plus d'énergie de
soudage dégrade par un refroidissement plus lent qui grossit le grain, le
phosphore et l'oxygène nuisent. C'est ce que l'énoncé appelle extraire la
connaissance experte, et cela rend le modèle crédible lorsqu'il suggère quelque
chose que l'on ne savait pas.

**Les limites, et elles sont réelles.** La pondération entre résistance et
ductilité **ne peut pas être choisie par les données**, puisqu'elle dépend de
l'usage final que le corpus ne contient pas ; la déplacer ne conserve que la
moitié du meilleur cinquième, donc le choix compte. La **microstructure
manque** : elle est l'intermédiaire physique entre composition et propriétés,
donc la variable la plus informative, mais elle n'est observable qu'après la
soudure et reste très peu renseignée. Enfin, l'ensemble de test a été consulté
trois fois au cours de l'exploration et une seule fois dans la série de rendu,
ce qui rend les chiffres de test des notebooks d'exploration légèrement
optimistes. Un défaut de qualité des données a par ailleurs été détecté par les
erreurs du modèle lui-même : trois lignes d'une même publication ont une limite
d'élasticité exactement égale à leur résistance à la traction, ce qui est
physiquement impossible. Nous les avons signalées sans les exclure, deux
d'entre elles étant dans l'ensemble de test.

## 7. Organisation du travail

Le travail a été mené en deux phases. Une **phase d'exploration** du 30
septembre au 9 octobre, répartie par méthode, un membre par famille de modèles,
qui a produit les quinze notebooks `notebooks/01` à `15` dans l'ordre
chronologique. Puis une **phase de consolidation** du 10 au 12 octobre, qui a
produit la série `notebooks/rendu/` de sept notebooks dans l'ordre logique, ne
retenant que les meilleurs choix en expliquant chaque fois pourquoi.

Cette seconde phase n'était pas prévue. Elle a été décidée après le constat
qu'une exploration répartie par méthode produit un parcours décousu pour un
lecteur : le choix de la cible avait été fait au notebook 02 puis remis en cause
au notebook 11, ce qui obligeait à relire l'ensemble dans un ordre que rien
n'indiquait. Son coût a été de trois jours pour quatre personnes, et nous la
considérons comme le meilleur investissement du projet.

**Chaque membre a poussé le notebook de rendu qui consolide son propre travail
d'exploration**, de sorte que l'historique Git reflète la contribution réelle.

| Membre | Exploration | Rendu | Pull request |
|---|---|---|---|
| Marie Gozlan | 02, 03, 04, 05 | 1, 2 | #2 |
| Pétronille Tard | 06, 07 | 3, 4 | #1 |
| Grégoire Pascual | 08, 09, 10 | 5, 6 | #5 |
| Jules Mortreux | 01, 11 à 15 | 7 | #3, #4 |

**Le diagramme de Gantt, la répartition détaillée par tâche et les charges
figurent en annexe** (`rapport/gantt.md`). Les dates y sont celles de
l'historique Git, donc vérifiables.

## Bibliographie

[1] T. Cool. *Design of Steel Weld Deposits*. Thèse de doctorat, University of
Cambridge, 1996.

[2] L. Breiman. Bagging predictors. *Machine Learning*, 24(2):123-140, 1996.

[3] L. Breiman. Random forests. *Machine Learning*, 45(1):5-32, 2001.

[4] J. H. Friedman. Greedy function approximation: a gradient boosting machine.
*The Annals of Statistics*, 29(5):1189-1232, 2001.

[5] C. Cortes et V. Vapnik. Support-vector networks. *Machine Learning*,
20(3):273-297, 1995.

[6] R. Tibshirani. Regression shrinkage and selection via the lasso. *Journal
of the Royal Statistical Society, Series B*, 58(1):267-288, 1996.

[7] M. Belkin, P. Niyogi et V. Sindhwani. Manifold regularization: a geometric
framework for learning from labeled and unlabeled examples. *Journal of Machine
Learning Research*, 7:2399-2434, 2006.

[8] F. Pedregosa et al. Scikit-learn: machine learning in Python. *Journal of
Machine Learning Research*, 12:2825-2830, 2011.

[9] R. J. A. Little et D. B. Rubin. *Statistical Analysis with Missing Data*.
Wiley, 3e édition, 2019.

[10] P. J. Rousseeuw. Silhouettes: a graphical aid to the interpretation and
validation of cluster analysis. *Journal of Computational and Applied
Mathematics*, 20:53-65, 1987.

[11] G. James, D. Witten, T. Hastie et R. Tibshirani. *An Introduction to
Statistical Learning*. Springer, 2e édition, 2021.

[12] C. Strobl, A.-L. Boulesteix, A. Zeileis et T. Hothorn. Bias in random
forest variable importance measures: illustrations, sources and a solution.
*BMC Bioinformatics*, 8:25, 2007.

[13] MAP Data Library, jeu `MAP_DATA_WELD`, University of Cambridge.
<https://www.phase-trans.msm.cam.ac.uk/map/data/materials/welddb-b.html>
