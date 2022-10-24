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

### Analyse

Certaines pipelines sont vides car elles sont appliquées sur une liste de fichiers : 

- open_e57_write_las.json
- open_las_create_OriginID_dimension.json

Pour ces pipelines, on pourra utiliser pdal-parallelizer avec -it à dir.

La pipeline merge_in_one_las.json ne nécessite pas l'utilisation de pdal-parallelizer, on pourra utiliser directement l'outil pdal-python.

Le reste des pipelines peuvent être exécutées avec pdal-parallelizer avec -it à single.

Attention à la mémoire, entre chaque étape penser à effacer la mémoire non gérée car on peut enchaîner plusieurs gros calculs.