Enzo GUIGNOLLE

<div align="center">
<img height="95" width="400" src="images/IUT_Velizy_Villacoublay_logo_2020_ecran.png" title="logo uvsq vélizy"/>
</div>

# Compte-Rendu des TPs

### [Introduction](#I)
### [I/ Méthode de Monte Carlo](#II)
### [II/ Algorithme et parrallélisation](#III)
### [III/ Mise en oeuvre sur machine à mémoire partagée](#IV)
- #### [A/ Assignment102.java](#a)
- #### [B/ Pi.java](#b)
### [IV/ Mise en oeuvre en mémoire distribué ](#V)
### [V/ Evaluation et test de performance](#VI)

<br>

------------

# <a name="I"></a> Introduction 

# <a name="II"></a> I/ Méthode de Monte Carlo

Durant la première séance de TP sur la méthode de Monte Carlo nous avons eu un cours sur ce qu'était la méthode et comment elle fonctionne pour d'approximer Pi. Je vais maintenant expliqué brièvement la méthode. La méthode de Monte Carlo est une méthode qui permet d'approximer Pi grâce au probabilité. Donc on prend un quart de cercle qui a pour rayon ```r=1``` dont l'aire est ```A = (pi*r**2)/4 = pi/4```. Après on prend un carré avec un coté de la taille du rayon du cercle ```c=1``` avec l'aire qui est ```Ac =c**2=1```. Ensuite on tire aléatoirement plusieurs points ```Xp=(xp,yp)``` et chaque coordonnée des points est tirée par une loi Uniforme ```U(]0,1[)```. Ensuite la probabilité que les points soit tirée dans le quart de cercle est ```P=A/Ac=pi/4```. <br>

#### Mettre la figure

Ensuite pour appoximer Pi on doit réaliser *ntot* tirage aléatoire de point. Ensuite on compte le nombre de point tombé dans le quart de cercle qu'on peut noter *ncible*. Maintenant on peut approcimer P par ```P = ncible/ntot = pi/4```. Grâce à cette formule pour approximer Pi on doit multiplier par 4 donc ça donne ```pi = (4*ncible)/ntot```. Donc maintenant nous pouvons approximer Pi.

# <a name="III"></a> II/ Algorithme et parrallélisation

Après avoir réaliser cela nous devions réfléchir à des algorithme en pseudo-code pour réaliser la méthode de Monte Carlo tout en faisant de la programmation parallèle. Donc on avait réfléchi au modèle de parallélisme que cela pouvait être et nous avions décidé que c'étais un parallélisme de tâche. Ensuite nous devions identifier les différentes tâches que nous avions dans la méthode. Nous avions trouver ces tâches:
- T0 : tirer et compter ntot points
- T1 : calculer Pi <br>

On pouvait ensuite encore décomposer la tâche T0 en sous-tâche : 
- T0p1 : Tirer xp
- T0p2 : Incrémenter ncible <br>

Ensuite nous devions trouver les dépendances de tâches pour savoir quels tâches pouvait être fait en parallèle. Donc nous avion vu que T1 dépendait de T0 mais que les sous-tâches de T0 était indépendantes. Cependant dans les sous-tâches nous avons T0p2 qui dépend de T0p1. <br>
Après nous devions déterminer la ressource critique et la section critique, qui sont pour la ressource critique ncible et la section critique l'incrémentation de ncible.
Après nous devions réfléchir à des pseudo-code pour faire ces codes avec les paradigmes qui sont **Master/Worker** et **itérations parallèles**.

# <a name="IV"></a> III/ Mise en oeuvre sur machine à mémoire partagée

Après avoir réalisé cela, deux code nous a été fournie, Assignment102.java et Pi.java et nous devions les analysé chacun pour savoir comment ils implémentait Monte Carlo.

## <a name="a"></a> A/ Assignment102.java

Dans ce code nous avons remarquer qu'il utilisait différentes classes de l'API Concurrent donc la classe AtomicInteger, ExecutorService et Executors. Nous avons aussi remarqué que nAtomSuccess est le nCible que nous avions choisis durant la conception de nos codes et que nThrows est le nTotal que nous avions choisis.<br>
Ensuite nous avons analyser le code et ce que chaque classe servait. Nous avons vu que le code utilisait la méthode incremantAndGet() de la classe AtomicInteger ce qui permet d'incrémenter de 1 au nombre.<br>
Nous avons aussi souligner que la classe MonteCarlo compose la classe PiMonteCarlo car c'est une classe qui est créer elle-même dans un autre classe.<br>
Nous avons aussi déduis que *value* en étant de type double doit représenter le nombre pi quand il est calculer.<br>
A la suite de cela nous avons vu qu'un ExecutorService était déclarer mais avant de cela, nous avons la récupération du nombre de Processeur dans l'ordinateur qui exécute le code. Puisque nous avons RunTime qui représente l'environnement d'exécution et il ne faut pas le confondre avec le CPUTime qui représente le temps d'exécution.<br>
Ensuite il prépare une workStealingPool avec le nombre de processeur récupérer qui permet de réaliser le vol de tâche c'est-à-dire qu'un processeur peut récupérer une tâche quand la tâche qui l'a est bloqué ou terminer.
Nous avons terminer l'analyse de ce code par dire qu'il représentait le paradigme des itérations parallèles car nous avons une boucle qui lance tout les itérations de MonteCarlo qui sont des Runnable.
De plus nous avons appris que l'executor permet de réaliser ce que l'on faisait quand on associait un Runnable avec un Thread durant les premiers TP.<br>
On peut ensuite améliorer le code pour éviter que trop de processus doivent passer par la section critique et nous avons penser
à regarder les points qui tombe hors du quart de cercle et de calculer la différence. Cela optimisera les calculs en parallèles car
nous avions vu que seulement 75% des points tombait dans le cercle donc que 75% des processus allait devoir passer par la section critique
alors qu'avec cette nouvelle façon seulement 25% doivent passer pas la section critique. Il suffira juste de modifier le calcul de Pi pour trouver la bonne valeur.

## <a name="a"></a> B/ Pi.java

Dans Pi.java nous avons vu qu'il utilisait plusieurs classes comme Future, ExecutionExeption ou encore Executor mais aussi une interface Callable qu'on 
nous a introduit précedemment qui font tous partie de l'API Concurrent.

### **Définir la classe Future**

Nous avons ensuite vu qu'il y avait deux classe principale qui sont la classe Master et Worker. Nous avons commencer par analyser la classe Master. Dans la classe Master nous avons vu qu'il y a une instanciation d'une liste de Callable, qui est la pour instancier les différents Worker qui vont être instancié. Ensuite dans le code nous avons pu voir une boucle qui parcours la liste de résultat des workers qui est une liste de Future défini précedemment. Ensuite on a essayer de savoir ce qu'était totalCount et nous avons dit que c'est le total de point qu'un Worker doit faire et que la variable total est le résultat de points qui sont dans la cible. Et nous avons fini par remarquer qu'au moment du calcul de Monte Carlo il fallait diviser par le nombre de Worker.
Nous avons ensuite regarder la classe Worker, qui implément l'interface Worker avec la classe Long qui est une classe générique. Nous avons ensuite vu que la classe exécutait la boucle de Monte Carlo avant de renvoyer le résultat au Master.
Nous avons fini par conclure cette analyse par dire que le paradigme de programmation parralèle de ce code est Master/Worker.

# <a name="V"></a> IV/ Mise en oeuvre en mémoire distribué

# <a name="VI"></a> V/ Evaluation et test de performance