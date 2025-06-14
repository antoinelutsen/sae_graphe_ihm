SAE Graphe

Membres du groupe :
Dorian Hembert tpa - HembertD
Scott Sénéchal tpe - Yuikotegawa
Antoine Lutsen tpa - antoinelutsen
Antoine Molinaro tpa - AM2240

Le projet :

Nous devions créer deux applications destinées à la gestion d'un magasin type supermarché. Il y a d'un côté la première application, l'application destinée à l'administrateur et de l'autre, la deuxième destinée à l'utilisateur.

L'application administrateur :

Son accès est protégé par un mot de passe (admin).
L'administrateur a accès au plan du magasin. Le quadrillage et les différents secteurs/rayons.
Il peut modifier les paramètres et les diverses informations associées au projet/magasin en cliquant sur le "i". Les informations sont automatiquement enregistrées.
L'administrateur peut également ajouter des articles et les placer dans le magasin en cliquant sur l'une des cases. Il doit sauvegarder manuellement en cliquant sur sauvegarder pour conserver ses modifications.

Vous pouvez consulter la notice d'utilisation pour plus de précisions sur l'application administrateur.

L'application utilisateur :

Son accès n'est pas protégé par un mot de passe.
L'utilisateur accède à un plan simplifié du magasin. Ni le quadrillage ni les secteurs n'apparaissent.
S'il clique sur un rayon, une fenêtre avec les produits du rayon apparaît.
L'utilisateur peut créer sa propre liste de courses en ajoutant des produits. Le chemin le plus efficace (le plus court), de l'entrée du magasin jusqu'à la caisse lui sera donné.
Il peut également importer une liste de courses au format .txt. Le chemin le plus court lui sera affiché à l'écran.
L'algorithme de Dijkstra est ici utilisé afin de donner le plus court chemin afin de récupérer tous les produits.

L'utilisateur peut obtenir des informations sur le magasin en cliquant sur le "i" (information).


Les axes d'améliorations :

Avec plus de temps disponible, nous aurions apprécié ajouter plus de fonctionnalités à nos applications.
Nous aurions aimé pouvoir permettre l'utilisation d'autres plans et de pouvoir passer entre les différents projets/magasins.
Il aurait été intéressant d'avoir un système qui détecte les rayons et qui détermine les endroits inaccessibles dans le magasin.
Nous voulions aussi améliorer notre code, notamment sur la vue. L'idée est de mettre sous la forme de fichiers JSON les zones inaccessibles ainsi que les différents secteurs/rayons du magasin. Ainsi, le code de la vue aurait pu être moins conséquent.
Nous souhaiterions séparer le modèle utilisateur et le modèle administrateur pour plus de simplicité dans le code.
Il aurait pu être intéressant de mieux ordonner les différents fichiers (regrouper les fichiers csv dans un même dossier par exemple).
Enfin, il aurait été plus pertinent d'avoir les produits sur les rayons et non devant, ce qui est moins cohérent.


