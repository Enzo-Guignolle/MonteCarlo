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
### [IV/ Mise en oeuvre en mémoire distribué](#V)
### [V/ Evaluation et test de performance](#VI)

<br>

------------

# <a name="I"></a> Introduction 

Ce document permet de synthétisé ce que j'ai pu réalisé durant les séances de Programmation avancée. Vous retrouverez les différents tests de performance des codes présenté durant ce rapport mais aussi les explications et la manière de réfléxion qu'il y a eu durant ces différentes séance de TP

## <a name="II"></a> I/ Méthode de Monte Carlo

Durant la première séance de TP sur la méthode de Monte Carlo nous avons eu un cours sur ce qu'était la méthode et comment elle fonctionne pour d'approximer Pi. Je vais maintenant expliqué brièvement la méthode. La méthode de Monte Carlo est une méthode qui permet d'approximer Pi grâce au probabilité. Donc on prend un quart de cercle qui a pour rayon ```r=1``` dont l'aire est ```A = (pi*r**2)/4 = pi/4```. Après on prend un carré avec un coté de la taille du rayon du cercle ```c=1``` avec l'aire qui est ```Ac =c**2=1```. Ensuite on tire aléatoirement plusieurs points ```Xp=(xp,yp)``` et chaque coordonnée des points est tirée par une loi Uniforme ```U(]0,1[)```. Ensuite la probabilité que les points soit tirée dans le quart de cercle est ```P=A/Ac=pi/4```. <br>
Voici un schéma représentant cette méthode : 

<img src="images/schema_methode_monte_carlo.png" width="300">

Ensuite pour appoximer Pi on doit réaliser *ntot* tirage aléatoire de point. Ensuite on compte le nombre de point tombé dans le quart de cercle qu'on peut noter *ncible*. Maintenant on peut approcimer P par ```P = ncible/ntot = pi/4```. Grâce à cette formule pour approximer Pi on doit multiplier par 4 donc ça donne ```pi = (4*ncible)/ntot```. Donc maintenant nous pouvons approximer Pi.

## <a name="III"></a> II/ Algorithme et parrallélisation

Après avoir réaliser cela nous devions réfléchir à des algorithme en pseudo-code pour réaliser la méthode de Monte Carlo tout en faisant de la programmation parallèle. Donc on avait réfléchi au modèle de parallélisme que cela pouvait être et nous avions décidé que c'étais un parallélisme de tâche. Ensuite nous devions identifier les différentes tâches que nous avions dans la méthode. Nous avions trouver ces tâches:
- T0 : tirer et compter ntot points
- T1 : calculer Pi <br>

On pouvait ensuite encore décomposer la tâche T0 en sous-tâche : 
- T0p1 : Tirer xp
- T0p2 : Incrémenter ncible <br>

Ensuite nous devions trouver les dépendances de tâches pour savoir quels tâches pouvait être fait en parallèle. Donc nous avion vu que T1 dépendait de T0 mais que les sous-tâches de T0 était indépendantes. Cependant dans les sous-tâches nous avons T0p2 qui dépend de T0p1. <br>
Après nous devions déterminer la ressource critique et la section critique, qui sont pour la ressource critique ncible et la section critique l'incrémentation de ncible.
Après nous devions réfléchir à des pseudo-code pour faire ces codes avec les paradigmes qui sont **Master/Worker** et **itérations parallèles**.

## <a name="IV"></a> III/ Mise en oeuvre sur machine à mémoire partagée

Après avoir réalisé cela, deux codes nous a été fournie, Assignment102.java et Pi.java et nous devions les analysé chacun pour savoir comment ils implémentait Monte Carlo.

### <a name="a"></a> A/ Assignment102.java

Dans ce code nous avons remarquer qu'il utilisait différentes classes de l'API Concurrent dont la classe AtomicInteger, ExecutorService et Executors. Nous avons aussi remarqué que nAtomSuccess représentait le nCible que nous avions choisis durant la conception de nos codes et que nThrows est le nTotal que nous avions choisis.<br>
Ensuite nous avons analyser le code et ce que chaque classe servait. Nous avons vu que le code utilisait la méthode incremantAndGet() de la classe AtomicInteger ce qui permet d'incrémenter de 1 au nombre.<br>
Nous avons aussi souligner que la classe MonteCarlo compose la classe PiMonteCarlo car c'est une classe qui est créer elle-même dans un autre classe.<br>
Nous avons aussi déduis que *value* en étant de type double doit représenter le nombre pi quand il est calculer.<br>
A la suite de cela nous avons vu qu'un ExecutorService était déclarer mais avant de cela, nous avons la récupération du nombre de Processeur dans l'ordinateur qui exécute le code. Puisque nous avons RunTime qui représente l'environnement d'exécution et il ne faut pas le confondre avec le CPUTime qui représente le temps d'exécution.<br>
Ensuite il prépare une workStealingPool avec le nombre de processeur récupérer qui permet de réaliser le vol de tâche c'est-à-dire qu'un processeur peut récupérer une tâche quand la tâche qui l'a est bloqué ou terminer.
Nous avons terminer l'analyse de ce code par dire qu'il représentait le paradigme des itérations parallèles car nous avons une boucle qui lance tout les itérations de MonteCarlo qui sont des Runnable.
De plus nous avons appris que l'executor permet de réaliser ce que l'on faisait quand on associait un Runnable avec un Thread durant les premiers TP.<br>
On peut ensuite améliorer le code pour éviter que trop de processus doivent passer par la section critique et nous avons penser à regarder les points qui tombe hors du quart de cercle et de calculer la différence. Cela optimisera les calculs en parallèles car nous avions vu que seulement 75% des points tombait dans le cercle donc que 75% des processus allait devoir passer par la section critique alors qu'avec cette nouvelle façon seulement 25% doivent passer pas la section critique. Il suffira juste de modifier le calcul de Pi pour trouver la bonne valeur.
Voici le diagramme de classe du code de Assignment102.java après avoir réalisé l'analyse du code : 

<img src="images/Assignment102.jpg" width="300">

### <a name="a"></a> B/ Pi.java


Nous allons maintenant analyser le code Pi.java avant de réalisé le diagramme de classe
Dans Pi.java nous avons vu qu'il utilisait plusieurs classes comme Future, ExecutionExeption ou encore Executor mais aussi une interface Callable qu'on 
nous a introduit précedemment qui font tous partie de l'API Concurrent. La classe Future permet de gérer des calculs asynchrone, elle permet de faire des tâches en arrière plan. On l'utilise souvent pour récupérer les résultats des Callable en utilisant la méthode get de la classe Future et on peut aussi voir si la tâches est terminée ou pas.<br>
Nous avons ensuite vu qu'il y avait deux classe principale qui sont la classe Master et Worker. Nous avons commencer par analyser la classe Master. Dans la classe Master nous avons vu qu'il y a une instanciation d'une liste de Callable, qui est la pour instancier les différents Worker qui vont être instancié. Ensuite dans le code nous avons pu voir une boucle qui parcours la liste de résultat des workers qui est une liste de Future défini précedemment. Ensuite on a essayer de savoir ce qu'était totalCount et nous avons dit que c'est le total de point qu'un Worker doit faire et que la variable total est le résultat de points qui sont dans la cible. Et nous avons fini par remarquer qu'au moment du calcul de Monte Carlo il fallait diviser par le nombre de Worker.
Nous avons ensuite regarder la classe Worker, qui implément l'interface Worker avec la classe Long qui est une classe générique. Nous avons ensuite vu que la classe exécutait la boucle de Monte Carlo avant de renvoyer le résultat au Master.
Nous avons fini par conclure cette analyse par dire que le paradigme de programmation parralèle de ce code est Master/Worker. Pour comprendre le fonctionnement du paradigme Master/Worker en mémoire partagé voici un schéma qui résume : 

<img src="images/schema_master_worker.png" height="300">

Donc le paradigme Master/Worker fonctionne de la manière suivante. Un programme fait office de Master c'est-à-dire que qu'il envoie des données que le Worker doit traiter pour réalisé ce qu'il lui a été attribué. Un fois que le Worker à réalisé ce qu'il lui a été attribué il renvoie ces résultat au Master qui analyse les données et les utilise pour finir ce qu'il doit faire.
Maintenant voici le diagramme de classe de Pi.java suite à son analyse.

<img src="images/Pi.jpg" width="400">
<br><br>

## <a name="V"></a> IV/ Mise en oeuvre en mémoire distribué

Pour réaliser Monte Carlo en mémoire distribué, il a été utilisé le paradigme Master/Worker pour comprendre comment cela fonctionne voici un schema qui synthétise son fonctionnement : 

<img src="images/schema_distributed.png" height="300">

Donc ce code permettra de faire en sorte que un Master soit sur une machine avec un certain nombre de Worker mais que d'autre Worker soit sur d'autre machine et qu'il puissent communiqué par envoie de message avec la machine qui contient le Master. De plus le paradigme fonctionne comme pour Pi.java donc je n'ai aps besoin d'expliquer de nouveau cela.<br>
Ensuite un code permettant de réalisé la méthode de Monte Carlo en mémoire distribué, nous a été fourni. Voici le diagramme de classe du code en question:

<img src="images/distributed_MC.jpg" width="400">

Ce code est composé de deux classes : MasterSocket et WorkerSocket. De plus, il utilise la méthode des sockets pour réaliser ce programme en mémoire distribuée. C'est-à-dire qu’un socket est un petit fichier contenant les données dont un autre programme peut avoir besoin pour s’exécuter. Après avoir analysé le code, nous devions intégrer la boucle de Monte Carlo dans la classe WorkerSocket.<br>
Pour pouvoir exécuter le code dans les bonnes conditions, nous devons passer un argument à la classe WorkerSocket afin qu’elle puisse définir le port à écouter pour l’envoi de messages. Ensuite, en exécutant la classe MasterSocket, nous devons spécifier le nombre de Worker que nous voulons utiliser ainsi que les différents ports à utiliser pour envoyer les messages.<br>
À la suite de cela, nous pouvons également faire de la programmation parallèle multi-niveau, c’est-à-dire que chaque WorkerSocket peut créer des Worker sur sa propre machine, comme dans Pi.java, et calculer les points de ces Worker qui les envoient ensuite au MasterSocket, comme prévu.

## <a name="VI"></a> V/ Evaluation et test de performance

Dans cette partie de mon rapport, on va faire les analyse de performance des différents codes que j'ai mentionné plus tôt. Nous allons commencer par préparer les tests de performance de Assignment102.java puis de Pi.java et on finira par le code en mémoire distribué.<br>
Avant de préparer et réalisé les différents tests de performance, je vais donné les différentes spécifications de l'ordianteur qui les aura réalisé. Cependant il est évident que les tests seront différents sur d'autre architecture matérielle.

- Processeur : Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz   1.50 GHz
- Nombre de coeur physique : 4
- Nombre de coeur logique : 8
- Mémoire RAM : 8 Go

De plus je vais rapidement expliquer ce qu'est la scalabilité forte et faible. La scalabilité forte permet de regarder si on laisse le nombre de points max à calculer dans ce cas mais qu'on augmente le nombre de processeur utilisé ce qui fait que le nombre de point par processeur diminue au fur et à mesure. La scalabilité faible est le faite de laisser fixe le nombre de point par processeur mais d'augmenter le nombre de point max à calculer mais aussi le nombre de processeur utilisé.
Pour pouvoir réalisé les courbes de la scalabilité forte mais aussi faible nous allons devoir calculé le speed up de chaque test. Pour cela nous devons utilisé cette formule :

```
SpeedUp = Temps_1_coeur / Temps_n_coeurs
```

Ensuite pour savoir si les speed up calculer après test de chaque programme soit optimal, nous allons nous fier à ce schéma : 

<img src="images/graphique_base_speedUp.JPG" width="300">

Pour avoir un speedUp optimal il faut que la courbe soit linéaire, c'est à dire que le speed up soit proportionnel en fonction du nombre de processeur comme le speed up de 1 processeur sera toujours 1, il faut que le speed up à N processeurs soit équivalent à 1*N.

### Assignment102.java

#### Scalabilité Forte

| Nombre total de points | Nombre de point par processeur | Nombre de processeur utilisable | Temps d'exécution |
|------------------------|--------------------------------|---------------------------------|-------------------|
| 1000000                | 1000000                        | 1                               | 195 ms            |
| 1000000                | 500000                         | 2                               | 264 ms            |
| 1000000                | 250000                         | 4                               | 494 ms            |
| 1000000                | 125000                         | 8                               | 549 ms            |
| 1000000                | 62500                          | 16                              | 566 ms            |

Après avoir réalisé les tests et calculer le speedUp cela nous donne une courbe de cette manière : 

<img src="images/courbe_scalabilitéForte_Assignment.JPG" width="400">

#### Scalabilité Faible

| Nombre total de points | Nombre de point par processeur | Nombre de processeur utilisable | Temps d'exécution |
|------------------------|--------------------------------|---------------------------------|-------------------|
| 1000000                | 1000000                        | 1                               | 248 ms            |
| 2000000                | 1000000                        | 2                               | 551 ms            |
| 4000000                | 1000000                        | 4                               | 2116 ms           |
| 8000000                | 1000000                        | 8                               | 4979 ms           |
| 16000000               | 1000000                        | 16                              | 12659 ms          |

Après avoir réalisé les tests et calculer le speedUp cela nous donne une courbe de cette manière : 

<img src="images/courbe_scalabilitéFaible_Assignment.JPG" width="400">

### Pi.java

#### Scalabilité Forte

| Nombre total de points | Nombre de point par processeur | Nombre de processeur utilisable | Temps d'exécution |
|------------------------|--------------------------------|---------------------------------|-------------------|
| 1000000                | 1000000                        | 1                               | 588 ms            |
| 1000000                | 500000                         | 2                               | 329 ms            |
| 1000000                | 250000                         | 4                               | 215 ms            |
| 1000000                | 125000                         | 8                               | 121 ms            |
| 1000000                | 62500                          | 16                              | 134 ms            |

Après avoir réalisé les tests et calculer le speedUp cela nous donne une courbe de cette manière : 

<img src="images/courbe_scalabilitéForte_Pi.JPG" width="400">

#### Scalabilité Faible

| Nombre total de points | Nombre de point par processeur | Nombre de processeur utilisable | Temps d'exécution |
|------------------------|--------------------------------|---------------------------------|-------------------|
| 1000000                | 1000000                        | 1                               | 600 ms            |
| 2000000                | 1000000                        | 2                               | 597 ms            |
| 4000000                | 1000000                        | 4                               | 749 ms            |
| 8000000                | 1000000                        | 8                               | 1107 ms           |
| 16000000               | 1000000                        | 16                              | 2019 ms           |

Après avoir réalisé les tests et calculer le speedUp cela nous donne une courbe de cette manière : 

<img src="images/courbe_scalabilitéFaible_Pi.JPG" width="400">

### Calcul distribué

#### Scalabilité Forte

| Nombre total de points | Nombre de point par processeur | Nombre de processeur utilisable | Temps d'exécution |
|------------------------|--------------------------------|---------------------------------|-------------------|
| 1000000                | 1000000                        | 1                               |                   |
| 1000000                | 500000                         | 2                               |                   |
| 1000000                | 250000                         | 4                               |                   |
| 1000000                | 125000                         | 8                               |                   |
| 1000000                | 62500                          | 16                              |                   |

#### Scalabilité Faible

| Nombre total de points | Nombre de point par processeur | Nombre de processeur utilisable | Temps d'exécution |
|------------------------|--------------------------------|---------------------------------|-------------------|
| 1000000                | 1000000                        | 1                               |                   |
| 2000000                | 1000000                        | 2                               |                   |
| 4000000                | 1000000                        | 4                               |                   |
| 8000000                | 1000000                        | 8                               |                   |
| 16000000               | 1000000                        | 16                              |                   |