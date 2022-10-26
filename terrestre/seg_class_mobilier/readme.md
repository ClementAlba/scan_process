# Reprise du projet scan_process terrestre

### Problèmes

- Les pipelines pdal et les fichiers pythons sont tous mélangés
- Fichiers json vides
- Mono-process
- Gros blocs de code dans les scripts python
- Chemins en dur dans le code
- Le process n'est pas automatisé, besoin d'appuyer sur une touche pour continuer le traitement

### Pipelines utilisées

- open_e57_write_las.json --> marquage_DOS.bat
- open_las_create_OriginID_dimension.json --> marquage_DOS.bat
- merge_in_one_las.json --> marquage_DOS.bat
- pipe_seg_sursol.json --> seg_sursol.bat
- Seg_sol_sursol.json --> traitement.bat
- classification_objets_mobiles.json --> traitement.bat
- calcul_scattering_anisotropy.json --> traitement.bat
- classification_sursol.json --> traitement.bat

À priori, la pipeline Classif_sol_v3.2_optim.json n'est pas utilisée.

### Scripts utilisés

- cluster_to_ground_v2.py --> Seg_sol_sursol.json
- mean_dimensions.py --> calcul_scattering_anisotropy.json
- mobile_objects_classification.py --> calcul_scattering_anisotropy.json
- global_descriptors_tranfo_meth.py --> classification_sursol.json
- marquage_obj_mobiles.py --> open_las_create_OriginID_dimension.json
- flying_cluster.py --> pipe_seg_sursol.json

À priori, la pipeline class_globals_desc.py n'est pas utilisée.

### Optimisations

- Séparer les pipelines des scripts python des fichiers .bat pour améliorer la lisibilité
- Replir les fichiers json vides quand c'est nécessaire
- Utiliser pdal-parallelizer quand c'est possible
- Découpage du code en plusieurs fonctions pour éviter les gros blocs difficiles à comprendre
- Supprimer les pipelines et scripts non-utilisés
- Remplacer les chemins absolus en dur par un fichier de configuration json ou par des chemins relatifs quand c'est possible
- Automatiser le process en remplaçant les fichiers .bat par des scripts python
- 
### Enchaînement du process

Dans un premier temps tous les fichiers e57 sont transformés en fichiers las, puis sur ces fichiers las la dimension OriginId est ajoutée pour chaque point du nuage. On rassemble ensuite tous ces fichiers pour n'en former qu'un.

Ensuite, le nuage est découpé en clusters de points et chaque point de chaque cluster est analysé pour déterminer son HAG. Grâce à cela on peut déterminer quels points font parti du sol et lesquels font parti du sursol. Les point ayant la classe 2 font parti du sol et les points ayant la classe 1 font parti du sursol.

On répète exactement le même procédé pour les points du sursol. Parmis ces points, on attribue la classe 65 aux points qui ne sont pas reliés au sol.

Ensuite, on cherche à determiner les objets mobiles et les objets fixes. Si un objet est en mouvement (mobile), ses points proviendront de plusieurs sources. On applique donc un filtre python qui va permettre de dresser un tableau contenant : le cluster, sa première source, le nombre de source du cluster.
Si le nombre de source est à 1, cela veut dire que l'objet est fixe et on lui attribue donc la classe 66.

On calcule l'orientation moyenne et la variation moyenne de surface du cluster et on les ajoute en tant que dimension du nuage. 

Enfin, pour classifier le sursol, on établi un score pour chacun des clusters, ce score déterminera si le cluster appartient à :
- de la végétation basse (classe 3)
- de la végétation intermédiaire (classe 4)
- de la végétation haute (classe 5)
- du bati (classe 6)

### Solution

Pour la transformation des fichiers e57 en las et aussi pour l'ajout de la dimension OriginId, l'utilisation de pdal_parallelizer me emble nécessaire : on parcourt tous les points du nuage donc le traitement bien que très simple peut en revanche être très long.
Pour le rassemblement de tous ces fichiers par contre, j'opterais pour l'utilisation de pdal en ligne de commande, ce qui simplifierai le code et qui nous éviterais un fichier json supplémentaire.

Toutes les étapes d'après étant reliées à des filtres python, que l'on applique sur un seul nuage, il serait intéressant d'utiliser ici pdal_parallelizer avec -it à single pour paralléliser ces traitements.
Il faut cependant garder en tête qu'il est nécessaire d'ajouter une étape qui merge toutes les tuiles produites pour repartir à chaque fois d'un seul fichier.

Et pour toutes les commandes liées à cloudcompare, l'idéal serait d'utiliser la librairie python qui permettrait d'uniformiser toute la chaîne en ayant que des fichiers python.
Attention à l'état de la mémoire à la fin de chacune des étapes : risque de débordement

### Graphe du projet

![graph](https://user-images.githubusercontent.com/93247842/197959895-6afd429c-9287-4d94-a28e-695c2f5efa4d.svg)
