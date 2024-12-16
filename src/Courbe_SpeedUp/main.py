import pandas as pd
import matplotlib.pyplot as plt
import math

def plot_scalability_forte(ax, csv_file, group_size=5, title=""):
    """
    Trace un graphique de scalabilité forte avec une ligne reliant les points de données et la courbe y = x.
    
    :param ax: L'axe de sous-graphique où tracer le graphique.
    :param csv_file: Chemin du fichier CSV contenant les données.
    :param group_size: Nombre de données à regrouper pour calculer la moyenne (par défaut 5).
    :param title: Titre personnalisé du graphique.
    """
    # Charger les données
    df = pd.read_csv(csv_file, sep=";")
    df_duree = df["Duree"].tolist()
    durees = [int(duree.replace('ms', '')) for duree in df_duree]

    # Calculer les durées moyennes
    meanDuration = []
    for i in range(0, len(durees), group_size):
        group = durees[i:i + group_size]
        avg = int(sum(group) / len(group))
        meanDuration.append(avg)

    print(title, meanDuration)

    # Liste des processeurs
    nbProcessor = sorted(list(set(df["nbProcessor"].tolist())))

    # Calculer le speedup
    duree_1_processeur = meanDuration[0]  # Temps avec 1 processeur
    speedup = [duree_1_processeur / duree for duree in meanDuration]

    # Tracer le graphique
    ax.plot(nbProcessor, speedup, label="Droite de SpeedUp", color='r', marker='o')
    ax.plot(nbProcessor, nbProcessor, label="SpeedUP idéal", color='b', linestyle='--')

    # Configuration du graphique
    ax.set_title(title, fontsize=14)  # Utilisation du titre personnalisé
    ax.set_xlabel("Nombre de processeurs", fontsize=12)
    ax.set_ylabel("Speedup", fontsize=12)
    ax.legend()
    ax.grid(True)

def plot_scalability_faible(ax, csv_file, group_size=50, title=""):
    """
    Trace un graphique de scalabilité faible avec une ligne reliant les points de données et la courbe y = 1.
    
    :param ax: L'axe de sous-graphique où tracer le graphique.
    :param csv_file: Chemin du fichier CSV contenant les données.
    :param group_size: Nombre de données à regrouper pour calculer la moyenne (par défaut 5).
    :param title: Titre personnalisé du graphique.
    """
    # Charger les données
    df = pd.read_csv(csv_file, sep=";")
    df_duree = df["Duree"].tolist()
    durees = [int(duree.replace('ms', '')) for duree in df_duree]

    # Calculer les durées moyennes
    meanDuration = []
    for i in range(0, len(durees), group_size):
        group = durees[i:i + group_size]
        avg = int(sum(group) / len(group))
        meanDuration.append(avg)

    print(title, meanDuration)

    # Liste des processeurs
    nbProcessor = sorted(list(set(df["nbProcessor"].tolist())))

    # Calculer le speedup
    duree_1_processeur = meanDuration[0]  # Temps avec 1 processeur
    speedup = [duree_1_processeur / duree for duree in meanDuration]

    # Tracer le graphique
    ax.plot(nbProcessor, speedup, label="Droite de SpeedUp", color='r', marker='o')
    ax.plot(nbProcessor, [1]*len(nbProcessor), label="SpeedUp idéal", color='b', linestyle='--')

    # Configuration du graphique
    ax.set_title(title, fontsize=14)  # Utilisation du titre personnalisé
    ax.set_xlabel("Nombre de processeurs", fontsize=12)
    ax.set_ylabel("Speedup", fontsize=12)
    ax.legend()
    ax.grid(True)

def plot_log_error_vs_iterations(ax, csv_file, title):
    # Charger le fichier CSV
    df = pd.read_csv(csv_file, sep=";")
    
    # Extraire les colonnes 'Error' et 'nbIteration'
    error = df['Error'].to_list()
    nb_iter = df["nbIteration"].to_list()

    # Initialiser une liste vide pour les erreurs transformées
    error_log = []

    # Appliquer la transformation logarithmique
    for i in error:
        try:
            # Convertir la virgule en point et calculer le logarithme
            log_error = math.log10(float(i.replace(',', '.')))
            error_log.append(log_error)
        except ValueError:
            # Gérer les erreurs de données invalides
            error_log.append(float('nan'))  # Ajouter NaN si une erreur survient

    # Assurer que les deux listes ont la même longueur (en supprimant les NaN de error_log et nb_iter)
    valid_data = [(nb_iter[i], error_log[i]) for i in range(len(nb_iter)) if not math.isnan(error_log[i])]

    # Si des données valides existent après le filtrage
    if valid_data:
        nb_iter_filtered, error_log_filtered = zip(*valid_data)

        # Tracer les données
        ax.scatter(nb_iter_filtered, error_log_filtered, c='b')
        ax.set_xlabel("Number of Iterations")
        ax.set_ylabel("Log(Error)")
        ax.set_title(title)
    else:
        print("Aucune donnée valide disponible pour afficher le graphique.")

# Créer la figure et les sous-graphique
fig, axes = plt.subplots(3, 2, figsize=(15, 10))

# Tracer les différents graphiques sur les sous-graphique avec des titres personnalisés
plot_scalability_forte(axes[0, 0], "data/output_G24_Assignment_forte.csv", title="Scalabilité Forte - Assignment")
plot_scalability_forte(axes[0, 1], "data/output_G24_Pi_forte.csv", title="Scalabilité Forte - Pi")
#plot_scalability_faible(axes[1, 0], "data/output_G24_Assignment_faible.csv", title="Scalabilité Faible - Assignment")
plot_scalability_faible(axes[1, 1], "data/output_G24_Pi_faible.csv", title="Scalabilité Faible - Pi")
plot_log_error_vs_iterations(axes[2, 0], "data/output_G24_Assignment_faible.csv", title="Error - Assignment")
plot_log_error_vs_iterations(axes[2, 1], "data/output_G24_Pi_faible.csv", title="Error - Pi")


# Ajuster l'espacement entre les graphiques
plt.tight_layout()

# Afficher tous les graphiques dans une même fenêtre
plt.show()
