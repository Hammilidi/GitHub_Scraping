import csv
from github import Github
from github import GithubException
import time
import datetime


# Créez une instance de l'objet Github en fournissant un jeton d'accès ou vos informations d'identification
g = Github("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", per_page=1000)

# Définissez la date de début (année, mois, jour)
date_debut = datetime.datetime(2023, 6, 1)

# Construisez la requête de recherche pour les dépôts créés à partir de la date de début
query = f"created:{date_debut.date()}"

# Recherchez les dépôts correspondants à la requête
results = g.search_repositories(query=query)

# Liste pour stocker les données des dépôts
data = []

# Parcourez les résultats et récupérez les informations nécessaires pour chaque dépôt
for repo in results:
    time.sleep(0.2)
    repo_data = {
        "Repository": repo.full_name,
        "Sujets": repo.get_topics(),
        "Etoiles": repo.stargazers_count, #interessant et tendance
        "Langages": list(repo.get_languages().keys()),
        "Views": repo.watchers_count, #interessant
        "PullRequests": repo.get_pulls(state='open', sort='created', base='master'), #interessant
        "Forks": repo.forks_count, #interessant
    }

    data.append(repo_data)


# Définir les noms des colonnes pour le fichier CSV
fieldnames = ["Repository", "Sujets", "Etoiles", "Langages", "Views", "PullRequests", "Forks"]

# Écrire les données dans un fichier CSV
with open("data1.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Export des données terminé. Les données ont été enregistrées dans un fichier .csv'.")
