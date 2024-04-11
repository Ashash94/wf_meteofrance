# weather-forecast

## Contexte

À l'occasion d'un hackathon organisé par Météo France, entre autres, pour valoriser les données publiques météorologiques, mes camarades et moi nous mettons en place un projet de génération automatique de bulletin météo textuel et audio.


## API Prévision

[Lien vers la donnée](lien https)

## Structure

## Prérequis 

## Procédures 

Depuis le fichier *main.py* se lance une mise à jour de la table mf_data (qui contient les prévisions météo de J-J à J+9) en appelant l'API MétéoFrance afin de récupérer les prévisions pour une liste de villes données provenant d'un fichier .json de [data.gouv.fr](https://www.data.gouv.fr/en/datasets/villes-de-france/).

Les données de prévisions de l'API sont mises à jour par MeteoFrance chaque jour aux heures suivantes : 0h05, 5h00, 12h05 et 17h00. Par conséquent, on lance une mise à jour de notre base de données quotidiennement à 1h10, 6h05, 12h10 et à 18h05 (soit une heure et cinq minutes après MétéoFrance)

### Dossier **mf_api** : Base de données météorologiques et géographiques

Les fonctions relativent à la récupération et à la gestion des données météorologiques sont contenues dans le fichier *meteo.py*

Les fonctions relativent à la récupération et à la gestion des données géographiques sont contenues dans le fichier *city_list.py*

Les appels vers l'API se font grâce à la bibliothèque *meteofrance_api* via le module *MeteoFranceClient*.

La base de données est gérée par PostgreSQL. (Outil libre de système de gestion de base de données relationnelle)

### Dossier **nlp** : Génération de bulletin

Le fichier *nlp.py* génère le bulletin météo au format texte via l'API EdenAI qui utilise le modèle d'OpenAI et transforme le texte généré en audio grâce à *pyttsx3* (bibliothèque de text to speech)