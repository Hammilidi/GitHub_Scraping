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

for repo in results:
    time.sleep(0.2)
    repo_data = {
        "Branches": list(repo.get_branches()), #tendance
        "NumberOfCommits": 0, #tendance
        "NumberOfContributors": set(), #tendance
        "Issues": repo.get_issues(state='open'), #tendance
        "Comments": repo.get_comments().totalCount, #interessant et tendance
        "Tags": repo.get_tags().totalCount
    }

    try:
        commits = repo.get_commits()
        repo_data["NomberOfCommits"] = commits.totalCount

        for commit in commits:
            author_name = commit.commit.author.name
            repo_data["NumberOfContributors"].add(author_name)

        repo_data["NumberOfContributors"] = len(repo_data["NumberOfContributors"])

    except GithubException as e:
        if e.status == 409 and "Git Repository is empty." in e.data["message"]:
            print(f"The repository '{repo.full_name}' is empty.")
            repo_data["NomberOfCommits"] = 0

    data.append(repo_data)

# Définir les noms des colonnes pour le fichier CSV
fieldnames = [ "Branches", "NomberOfCommits", "NumberOfContributors", "Issues", "Comments"]

# Écrire les données dans un fichier CSV
with open("data1.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print("Export des données terminé. Les données ont été enregistrées dans un fichier .csv'.")


