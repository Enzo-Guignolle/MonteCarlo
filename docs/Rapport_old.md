Enzo GUIGNOLLE

<div align="center">
<img height="95" width="400" src="images/IUT_Velizy_Villacoublay_logo_2020_ecran.png" title="logo uvsq vélizy"/>
</div>

# Compte-Rendu des TPs

### [Introduction](#I)
### [Programmation avancée](#II)
- #### [Première séance de TP](#a)
- #### [Deuxième séance de TP](#b)
- #### [Troisième séance de TP](#c)
- #### [Quatrième séance de TP](#d)
- #### [Cinquième séance de TP](#e)
- #### [Sixième séance de TP](#f)
### [Qualité de développement](#III)

<br>

------------

# <a name="I"></a> Introduction 

# <a name="II"></a> Programmation avancée 

## <a name="a"></a> Première séance de TP

Durant la première séance de TP sur la méthode de Monte Carlo nous avons eu un cours sur ce qu'était la méthode et comment elle fonctionne pour d'approximer Pi. Je vais maintenant expliqué brièvement la méthode. La méthode de Monte Carlo est une méthode qui permet d'approximer Pi grâce au probabilité. Donc on prend un quart de cercle qui a pour rayon ```r=1``` dont l'aire est ```A = (pi*r**2)/4 = pi/4```. Après on prend un carré avec un coté de la taille du rayon du cercle ```c=1``` avec l'aire qui est ```Ac =c**2=1```. Ensuite on tire aléatoirement plusieurs points ```Xp=(xp,yp)``` et chaque coordonnée des points est tirée par une loi Uniforme ```U(]0,1[)```. Ensuite la probabilité que les points soit tirée dans le quart de cercle est ```P=A/Ac=pi/4```. <br>

#### Mettre la figure

Ensuite pour appoximer Pi on doit réaliser *ntot* tirage aléatoire de point. Ensuite on compte le nombre de point tombé dans le quart de cercle qu'on peut noter *ncible*. Maintenant on peut approcimer P par ```P = ncible/ntot = pi/4```. Grâce à cette formule pour approximer Pi on doit multiplier par 4 donc ça donne ```pi = (4*ncible)/ntot```. Donc maintenant nous pouvons approximer Pi.<br>
Après avoir réaliser cela nous devions réfléchir à des algorithme en pseudo-code pour réaliser la méthode de Monte Carlo tout en faisant de la programmation parallèle. Donc on avait réfléchi au modèle de parallélisme que cela pouvait être et nous avions décidé que c'étais un parallélisme de tâche. Ensuite nous devions identifier les différentes tâches que nous avions dans la méthode. Nous avions trouver ces tâches:
- T0 : tirer et compter ntot points
- T1 : calculer Pi <br>

On pouvait ensuite encore décomposer la tâche T0 en sous-tâche : 
- T0p1 : Tirer xp
- T0p2 : Incrémenter ncible <br>

Ensuite nous devions trouver les dépendances de tâches pour savoir quels tâches pouvait être fait en parallèle. Donc nous avion vu que T1 dépendait de T0 mais que les sous-tâches de T0 était indépendantes. Cependant dans les sous-tâches nous avons T0p2 qui dépend de T0p1. <br>
Après nous devions déterminer la ressource critique et la section critique, qui sont pour la ressource critique ncible et la section critique l'incrémentation de ncible.
Après nous devions réfléchir à des pseudo-code pour faire ces codes avec les paradigmes qui sont **Master/Worker** et **itérations parallèles**.


## <a name="b"></a> Deuxième séance de TP

Durant la deuxième partie de la séance, nous devions commencer par analyser un de deux code qui nous ont été donnée et qui réalise la méthode de Monte Carlo pour calculer Pi. C'est deux code sont Pi.java et Assignment102.java. Nous avons commencer par analyser Assignment102.java.

### **Faire le diagramme de classe de Assignment102**

Dans ce code nous avons remarquer qu'il utilisait différentes classes de l'API Concurrent donc la classe AtomicInteger, ExecutorService et Executors. Nous avons aussi remarqué que nAtomSuccess est le nCible que nous avions choisis durant la conception de nos codes et que nThrows est le nTotal que nous avions choisis.<br>
Ensuite nous avons analyser le code et ce que chaque classe servait. Nous avons vu que le code utilisait la méthode incremantAndGet() de la classe AtomicInteger ce qui permet d'incrémenter de 1 au nombre.<br>
Nous avons aussi souligner que la classe MonteCarlo compose la classe PiMonteCarlo car c'est une classe qui est créer elle-même dans un autre classe.<br>
Nous avons aussi déduis que *value* en étant de type double doit représenter le nombre pi quand il est calculer.<br>
A la suite de cela nous avons vu qu'un ExecutorService était déclarer mais avant de cela, nous avons la récupération du nombre de Processeur dans l'ordinateur qui exécute le code. Puisque nous avons RunTime qui représente l'environnement d'exécution et il ne faut pas le confondre avec le CPUTime qui représente le temps d'exécution.<br>
Ensuite il prépare une workStealingPool avec le nombre de processeur récupérer qui permet de réaliser le vol de tâche c'est-à-dire qu'un processeur peut récupérer une tâche quand la tâche qui l'a est bloqué ou terminer.
Nous avons terminer l'analyse de ce code par dire qu'il représentait le paradigme des itérations parallèles car nous avons une boucle qui lance tout les itérations de MonteCarlo qui sont des Runnable.
De plus nous avons appris que l'executor permet de réaliser ce que l'on faisait quand on associait un Runnable avec un Thread durant les premiers TP.

## <a name="c"></a> Troisième séance de TP

Nous avons commencer le cours par avoir de nouvelle informations sur certaines interface de l'API Concurrent.
Par exemple on a vu que les classe qui implémente la classe Callable peuvent renvoyer un résultat alors que ceux
qui implémente l'interface Runnable ne peut pas renvoyer de résultat.<br>
On a ensuite regarder comment améliorer le code pour éviter que trop de processus soit créer pour être exécuter et nous avons penser
à regarder les points qui tombe hors du quart de cercle et de calculer la différence. Cela optimisera les calculs en parallèles car
nous avions vu que seulement 75% des points tombait dans le cercle donc que 75% des processus allait devoir passer par la section critique
alors qu'avec cette nouvelle façon seulement 25% doivent passer pas la section critique. <br>
Dans la deuxième partie du cours nous avons analyser le code Pi.java qui nous a été fourni avec le code Assignment102.java. *

### **Faire le diagramme de classe Pi.java**

Nous avons vu qu'il utilisait plusieurs classes comme Future, ExecutionExeption ou encore Executor mais aussi une interface Callable qu'on 
nous a introduit précedemment qui font tous partie de l'API Concurrent.

### **Définir la classe Future**

Nous avons ensuite vu qu'il y avait deux classe principale qui sont la classe Master et Worker. Nous avons commencer par analyser la classe Master. Dans la classe Master nous avons vu qu'il y a une instanciation d'une liste de Callable, qui est la pour instancier les différents Worker qui vont être instancié. Ensuite dans le code nous avons pu voir une boucle qui parcours la liste de résultat des workers qui est une liste de Future défini précedemment. Ensuite on a essayer de savoir ce qu'était totalCount et nous avons dit que c'est le total de point qu'un Worker doit faire et que la variable total est le résultat de points qui sont dans la cible. Et nous avons fini par remarquer qu'au moment du calcul de Monte Carlo il fallait diviser par le nombre de Worker.
Nous avons ensuite regarder la classe Worker, qui implément l'interface Worker avec la classe Long qui est une classe générique. Nous avons ensuite vu que la classe exécutait la boucle de Monte Carlo avant de renvoyer le résultat au Master.
Nous avons fini par conclure cette analyse par dire que le paradigme de programmation parralèle de ce code est Master/Worker.

## <a name="d"></a> Quatrième séance de TP

Durant la première partie de cette séance de TP nous devions modifier le code Pi.java et Assignment102.java pour faire en sorte que les deux code renvoieles mêmes sorties dans le terminal. Pour ma part l'ordre de sortie que j'ai réalisé, est la valeur de pi puis le temps d'exécution puis le nombre total de point puis le nombre de processus puis le nombre de point compté dans le quart de cercle puis l'erreur entre la valeur trouvé et la véritable valeur de pi puis la différence entre la véritable valeur de pi et celle trouver par l'algorithme. En faisant cela, ça nous permettra d'analyser plus facilement les performances du code plus tard. Nous devions faire un deuxième truc qui permettra aussi de facilité l'analyser, c'est d'écrire les données de sortie dans un fichier pour pouvoir ensuite les utiliser pour faire des graphique et de calculer le speedup. Donc ça permettra encore plus de facilité l'analyse des performances.<br>
Dans cette deuxième partie de TP nous devions commencer la deuxième partie du TP4 qui est de faire la méthode de MonteCarlo mais en mémoire distribué. Un code permettant de réalisé cela nous a été fourni voici à quoi il ressemble.

### **Faire le diagramme de classe distributedMC**

Nous avons commencer par analyser le code qui nous a été fourni avec les MasterSocket et WorkerSocket. Tout d'abord ce code utilise la méthode des Sockets pour réalisé ce programme en mémoire distribué. C'est-à-dire qu'un socket est un petit fichier contenant les données qu'un autre programme peut avoir besoin pour exécuter.<br>
Après avoir analyser le code nous devions faire la boucle de MonteCarlo dans la classe WorkerSocket.

## <a name="e"></a> Cinquième séance de TP

**Diagramme UML distributedMC**

Pour réaliser Monte Carlo en programmation distribué, le paradigme de programmation parallèle utilisé est Master/Worker. C'est à dire que nous avons une machine qui fait le rôle de Master et plein d'autre machine qui fond le rôle de Worker. Pour communiquer entre eux cela se fait par envoie de message. Pour pouvoir faire marcher cela sur une seule et même machine car cela est possible nous devons commencer par lancer le nombre de Worker que nous voulons en leur associant à chacun un port différent. Ensuite nous devons lancer le Master pour qu'ils puissent donner à chaque Worker ce qu'il doit réaliser.

**Illustration du paradigme**

## <a name="f"></a> Sixième séance de TP

# <a name="III"></a> Qualité de développement 

## Mesure de performance 

### Assignment102.java

Scalabilité Forte (On augmente le nombre de process mais avec un nombre fixe de points)

| Nombre d'itération | Nombre de Worker | Temps d'exécution |
|--------------------|------------------|-------------------|
| 1000000            | 1                |                   |
| 1000000            | 2                |                   |
| 1000000            | 4                |                   |
| 1000000            | 8                |                   |
| 1000000            | 16               |                   |

Scalabilité Faible (On augmente le nombre de process mais avec un nombre fixe de points par process)

| Nombre d'itération | Nombre de Worker | Temps d'exécution |
|--------------------|------------------|-------------------|
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |


### Pi.java

Scalabilité Forte

| Nombre d'itération | Nombre de Worker | Temps d'exécution |
|--------------------|------------------|-------------------|
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |


Scalabilité Faible

| Nombre d'itération | Nombre de Worker | Temps d'exécution |
|--------------------|------------------|-------------------|
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |


### Calcul distribué

Scalabilité Forte

| Nombre d'itération | Nombre de Worker | Temps d'exécution |
|--------------------|------------------|-------------------|
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |


Scalabilité Faible

| Nombre d'itération | Nombre de Worker | Temps d'exécution |
|--------------------|------------------|-------------------|
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |
| 1000000            | 1                |                   |x
