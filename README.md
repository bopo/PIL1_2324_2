# Site de rencontre avec Django, HTML, CSS et Javascript _____ PIL1_2324_2 

## Contexte
  Chaque année, l'Institut de Formation et de Recherche en Informatique (IFRI) de l'Université Publique d'Abomey-Calavi soumet soumet un défi aux étudiants de Licence 1 en fin d'anéee. Le projet de cette année consiste à réaliser un service de rencontres en ligne sous la forme d’une application web en 4 semaines.
Le développement de cette application nous a permis de mettre en oeuvre et d'étendre nos connaissances du framework Django et de sa logique. Le style de l'application a été fait à l'aide de Bootstrap5.
Afin de la rendre plus facilement testable, le repository contient la base de données, la Secret Key Django, ainsi que des informations de connexions. Les instructions de déploiement ont été rajoutées un peu plus bas sur le dépôt.

# You_Me App

![Logo du Projet](./You_Me.jpg)

## Fonctionnalités

- **Inscription et Connexion** : Les utilisateurs peuvent s'inscrire et se connecter pour accéder à la plateforme.
- **Récupération de mot de passe** : Les utilisateurs peuvent récuperer leurs mots de passe en cas d'oubli.
- **Profil Utilisateur** : Chaque utilisateur a un profil où il peut gérer ses informations personnelles.
- **Messagerie Instantanée** : Discutez avec d'autres utilisateurs en temps réel.
- **Liste des Discussions** : Visualisez et accédez rapidement à vos discussions récentes.
- **Suggestions de Profils** : Découvrez et connectez-vous avec de nouveaux utilisateurs grâce à un superbe algorithme de matchmaking.
- **Dashboard Administrateur** : Accédez à un interface administrateur si vous y êtes autorisés.

## Installation

- [Python 3.9](https://www.python.org/downloads/)
- [Django 4.2.13](https://www.djangoproject.com/)
- Autres dépendances listées dans `requirements.txt`

  ### Installation
1- Créer un dossier puis ouvrez le dans votre éditeur de code : 
2- Créer votre environnement virtuel : 
    ```bash
    python -m venv mon_env 
    ```
3- Activez votre environnement virtuel : 
  - Sur Windows : 
      ```bash
      $ mon_env\Scripts\activate
      ```
  - Sur Linux :
     ```
      $ source mon_env/Scripts/activate
     ```
4. Clonez le dépôt :
    ```bash
    (mon_env) git clone https://github.com/rosasbehoundja/PIL1_2324_2.git
    ```
5. Naviguez dans le répertoire du projet :
    ```bash
    (mon_env) cd PIL1_2324_2
    ```
6. Installez les dépendances :
    ```bash
    (mon_env) pip install -r requirements.txt
    ```
7- Configurez votre base de données dans le fichier [settings.py](PIL1_2324_2/settings.py) :
    . Utilisation de SQLite :
      ```bash 
       DATABASES = {
          'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
    }
      ```
    . Utilisation de MySQL : 
      ```bash
      DATABASES = {
        'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'your_db_name',
          'USER': 'your_db_user',
          'PASSWORD': 'your_db_password',
          'HOST': 'your_db_host',  # Set to 'localhost' or '127.0.0.1' for local development
          'PORT': '3306',          # Default port for MySQL
          }
    }
        ```
8. Appliquez les migrations :
    ```bash
    (mon_env) python manage.py makemigrations
    (mon_env) python manage.py migrate
    ```
9- (Optionnel) Importez dans votre base de données les infos de 2000 utilisateurs prédéfinis : 
    ```bash
    (mon_env) python manage.py import_users
    (mon_env) python manage.py import_hobbies
    ```
5. Créez un superutilisateur :
    ```bash
    (mon_env) python manage.py createsuperuser
    ```
5. Démarrez le serveur de développement :
    ```bash
    (mon_env) python manage.py runserver
    ```
