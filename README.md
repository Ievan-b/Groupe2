Notice d'utilisation:

Sommaire:
- Contexte
- PC1 (ERP odoo)
    - Introduction
    - Configuration
    - Déployement des containers
    - 
- PC2 (Fichier Logistique)
    - Introduction
    - Fichier.exe
    - Fichier.py
- PC3 (Fichier Production)
    - Introduction
    - Fichier.exe
    - Fichier.py

================================================================================
Installation de la machine virtuelle PC_1 sur Virtual Box :
    1.Assurez-vous que la version de Virtual Box est "7.3.10".
    2.Démarrez la machine virtuelle PC_1.
    
Configuration de Portainer :
    1.Accédez au site internet portainer.io http://localhost:9000, qui est déjà préinstallé et        contient les images nécessaires.
    2.Connectez-vous en tant qu'administrateur.
    3.Cliquez sur "Local", puis allez dans l'onglet "Stacks".
    4.Cliquez sur "Add Stack".
    
Configuration de la stack :
    1.Entrez un nom pour la stack.
    2.Allez dans le web editor et collez le contenu du fichier Docker compose.yml.
    3.Cliquez sur "Deploy the Stack" et vérifiez que les trois serveurs sont en running.
    
Configuration du serveur ERP Odoo :
    1.Ouvrez le serveur ERP Odoo sur un navigateur en utilisant ce lien : &                 
http://localhost:8069, ou accédez au docker que vous venez de créer et cliquez sur "8069" dans la colonne "published ports".
    2.Sur le site, sélectionnez "Gestion des bases de données", puis "Restore Database".
    3.Entrez le Master Password (MSIR5), cliquez sur "Parcourir" et sélectionnez le fichier 
     .ZIP téléchargé dans le répertoire spécifié (NomDeVotreRepertoire/SOUMSOUM).
    4.Attribuez un nom à votre base de données, qui doit être "SOUMSOUM".
Modification des paramètres réseau de la machine virtuelle :
    1.Passez en accès par pont dans les paramètres réseau de votre machine virtuelle.
    2.Changez l'adresse IP de votre machine virtuelle contenant le docker pour 172.31.10.158.
    3.Déconnectez-vous du réseau wifi sur la machine virtuelle, puis reconnectez-vous pour que 
     les modifications soient prises en compte.
================================================================================

Contexte :

Cette procédure à pour but d'aider à l'installation complete de l'ERP et de l'utilisation des fichier python.
Cela devra donc être effectuer sur une machine virtuel via Virtual box en version "7.0.10". Les machines virtuel devront être parametrer en en NAT et non en bridge pour permettre les connections pour notre application.

- PC1 (ERP odoo)
    - Introduction
    - Configuration
    - Déployement des containers


      
- PC2 (Fichier Logistique)
    - Introduction
    - Fichier.exe
    - Fichier.py
- PC3 (Fichier Production)
    - Introduction
    - Fichier.exe
    - Fichier.py
