# Touch Tech Solution - ERP Odoo

![Logo Touch Tech Solutions](Logo%20TouchTech%20Solutions.png)

## Description

Touch Tech Solution est une entreprise spécialisée dans l'achat-revente de souris et clavier pour ordinateur. Ce référentiel contient le fichiers Python nécessaires pour traiter et afficher les données de la base de données de l'ERP Odoo.

## Contenu

1. [Odoo ERP](#odoo-erp)
2. [Fichiers Python](#fichiers-python)
3. [Installation](#installation)
4. [Configuration](#configuration)


## Odoo ERP

Odoo, notre système ERP, sert de base de données centralisée pour la gestion des stocks des articles. Les processus de gestion des ordres de production et des sorties de stock sont pris en charge de manière personnalisée à l'aide d'une application Python dédiée.
Afin de procéder à la configuration de l'ERP nous avons mis à disposition un fichier ".zip" contenant les données concernant la base de données ainsi que le fichier "docker-compose.yml" qui possède l'ensemble des configuration et parametre nécessaire au portainer.
la procédure d'installation de l'ERP sous linux est la suivante:
-ce connecter au réseau Wifi Guest
- se connecter à portainer.io avec les identifiant suivant:
  Identifiant : admin
  mot de passe : portainer
une fois connecter à portainer.io, il s'agit de créer les containers en le nommant "odoo" et en y appliquant le le contenue du fichier joint "docker-compose.yml". Selectionner la méthode de construction "Web editor" puis finaliser la configuration des containers avec le bouton de validation. 

- Une fois avoir créer les deux container il faut les passer en mode "running"
- Au premier lancement, le serveur demande de rentrer des identifiant qui sont les suivants dans notre aplication:
  Master Password : MSIR5
  Database Name : Touch_db
  Email : admin
  Password : 1234

- une fois que cela est fait il faut importer les data du fichier Zip joint dans le GIT.


## Fichiers Python

Le fichier Python inclus dans ce projet:
- `PYTHON.py`: [Application Logistique]


## Installation

1. Clonez le référentiel :
    ```bash
    git clone https://github.com/votre-utilisateur/touch-tech-solution.git
    ```

2. Accédez au répertoire du projet :


3. Installez les dépendances :


## Configuration

1. Configurez les paramètres de connexion à la base de données dans le fichier `config.yaml`.


