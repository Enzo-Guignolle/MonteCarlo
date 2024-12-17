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

def plot_log_error_vs_iterations(ax, csv_file, group_size=50, title=""):
    # Charger les données et les convertir
    df = pd.read_csv(csv_file, sep=";")
    errors = [float(e.replace(',', '.')) for e in df['Error']]
    iterations = df["nbIteration"].to_list()

    # Calcul des logs des erreurs
    log_errors = [math.log10(e) if e > 0 else float('nan') for e in errors]

    # Calcul des moyennes par groupe
    mean_log_errors = [
        math.log10(sum(errors[i:i + group_size]) / len(errors[i:i + group_size]))
        for i in range(0, len(errors), group_size)
    ]

    # Filtrer les données valides
    valid_data = [(iterations[i], log_errors[i]) for i in range(len(log_errors)) if not math.isnan(log_errors[i])]
    
    if valid_data:
        nb_iter_filtered, log_errors_filtered = zip(*valid_data)

        # Tracer les points et les moyennes
        ax.scatter(nb_iter_filtered, log_errors_filtered, c='b', label="Erreur par nombre d'itération")
        ax.scatter(sorted(set(iterations)), mean_log_errors, c='r', label="Médiane")
        ax.set_xlabel("Number of Iterations")
        ax.set_ylabel("Log(Error)")
        ax.set_title(title)
        ax.legend()
    else:
        print("Aucune donnée valide disponible pour afficher le graphique.")


# Créer la figure et les sous-graphique
fig, axes = plt.subplots(3, 2, figsize=(15, 10))

# Tracer les différents graphiques sur les sous-graphique avec des titres personnalisés
plot_scalability_forte(axes[0, 0], "data/output_G24_Assignment_forte.csv", title="Scalabilité Forte - Assignment")
plot_scalability_forte(axes[0, 1], "data/output_G24_Pi_forte.csv", title="Scalabilité Forte - Pi")
#plot_scalability_faible(axes[1, 0], "data/output_G24_Assignment_faible.csv", title="Scalabilité Faible - Assignment")
plot_scalability_faible(axes[1, 1], "data/output_G24_Pi_faible.csv", title="Scalabilité Faible - Pi")
#plot_log_error_vs_iterations(axes[2, 0], "data/output_G24_Assignment_faible.csv", title="Error - Assignment")
plot_log_error_vs_iterations(axes[2, 1], "data/output_G24_Pi_faible.csv", title="Error - Pi")


# Ajuster l'espacement entre les graphiques
plt.tight_layout()

# Afficher tous les graphiques dans une même fenêtre
plt.show()
