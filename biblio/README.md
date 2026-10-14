# Bibliographie

Les treize références citées dans le texte du rapport
[`rapport/rapport.md`](../rapport/rapport.md), avec le numéro d'appel utilisé
dans le rapport et l'endroit du projet qu'elles justifient.

## Le domaine : soudage et métallurgie

**[1]** T. Cool. *Design of Steel Weld Deposits*. Thèse de doctorat, University
of Cambridge, 1996.
Source du jeu de données et référence métallurgique sur les dépôts soudés.
Justifie notre validation extérieure : le sens des effets du manganèse, de
l'énergie de soudage, du phosphore et de l'oxygène.

**[13]** MAP Data Library, jeu `MAP_DATA_WELD`, University of Cambridge.
<https://www.phase-trans.msm.cam.ac.uk/map/data/materials/welddb-b.html>
Le corpus `welddb` lui-même, et la documentation qui précise que `N` signifie
non renseigné et pas zéro.

Une troisième référence du même groupe est citée par le README du projet :
T. Cool, H. K. D. H. Bhadeshia, D. J. C. MacKay, *Materials Science and
Engineering*, 1997.

## Les méthodes d'ensemble

**[2]** L. Breiman. Bagging predictors. *Machine Learning*, 24(2):123-140, 1996.
Justifie notre stratégie de réglage : le nombre d'arbres n'est pas un paramètre
de compromis, donc il se règle séparément de la forme des arbres.

**[3]** L. Breiman. Random forests. *Machine Learning*, 45(1):5-32, 2001.
Le tirage de variables à chaque coupure, et la décomposition de la variance en
`rho * sigma^2 + (1 - rho) * sigma^2 / B` qui explique pourquoi la forêt bat le
bagging.

**[4]** J. H. Friedman. Greedy function approximation: a gradient boosting
machine. *The Annals of Statistics*, 29(5):1189-1232, 2001.
Justifie que le taux d'apprentissage et le nombre d'itérations se compensent et
doivent donc être explorés conjointement.

## Les marges et les noyaux

**[5]** C. Cortes et V. Vapnik. Support-vector networks. *Machine Learning*,
20(3):273-297, 1995.
Le modèle retenu du projet, dans sa variante de régression. La perte insensible
à epsilon et le tube de tolérance, qui expliquent pourquoi il a fallu
standardiser la cible.

## La régularisation et la sélection

**[6]** R. Tibshirani. Regression shrinkage and selection via the lasso.
*Journal of the Royal Statistical Society, Series B*, 58(1):267-288, 1996.
Le Lasso, l'une des quatre déterminations indépendantes qui désignent le
manganèse et l'énergie de soudage comme leviers.

**[11]** G. James, D. Witten, T. Hastie et R. Tibshirani. *An Introduction to
Statistical Learning*. Springer, 2e édition, 2021.
Les critères Cp, AIC, BIC et R2 ajusté, et la règle de l'écart-type qui nous
fait retenir 17 variables sur 34 pour 3,5 % d'erreur en plus.

## Le semi-supervisé

**[7]** M. Belkin, P. Niyogi et V. Sindhwani. Manifold regularization: a
geometric framework for learning from labeled and unlabeled examples. *Journal
of Machine Learning Research*, 7:2399-2434, 2006.
Le cadre de notre ridge régularisée par le laplacien d'un graphe. C'est aussi lui
qui fournit la version à noyau, inscrite dans nos perspectives comme la piste
d'un semi-supervisé non linéaire.

## Les données manquantes

**[9]** R. J. A. Little et D. B. Rubin. *Statistical Analysis with Missing
Data*. Wiley, 3e édition, 2019.
La typologie MCAR, MAR et MNAR. Justifie notre conclusion que le mécanisme est
MAR, et les trois conséquences qui en découlent sur toute la chaîne.

## L'évaluation et l'interprétation

**[10]** P. J. Rousseeuw. Silhouettes: a graphical aid to the interpretation and
validation of cluster analysis. *Journal of Computational and Applied
Mathematics*, 20:53-65, 1987.
Le coefficient de silhouette, croisé chez nous avec la stabilité au
rééchantillonnage pour choisir le nombre de groupes.

**[12]** C. Strobl, A.-L. Boulesteix, A. Zeileis et T. Hothorn. Bias in random
forest variable importance measures: illustrations, sources and a solution.
*BMC Bioinformatics*, 8:25, 2007.
Justifie notre choix de l'importance par permutation plutôt que par impureté, et
documente sa limite sur les variables corrélées, qui est exactement le cas de
l'énergie de soudage chez nous.

## L'outillage

**[8]** F. Pedregosa et al. Scikit-learn: machine learning in Python. *Journal of
Machine Learning Research*, 12:2825-2830, 2011.
La bibliothèque utilisée, et en particulier le `Pipeline` et le
`ColumnTransformer` qui rendent la fuite d'information impossible par
construction.

---

**Note.** Les documents eux-mêmes ne sont pas versionnés dans ce dossier, les
articles cités étant sous droits. Les références sont données sous une forme
permettant de les retrouver, et les deux sources en accès libre, le corpus et la
thèse de Cool, sont accessibles par les liens ci-dessus.
