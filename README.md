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
1. Installer la machine virtuelle PC_1 sur virtual Box en s'assurant dans l'aide que la version de virtual box est en version "7.3.10", puis démarrer la.

2. Aller sur le site internet portainer.io http://localhost:9000 qui est deja préinstaller et possèdant déjà les images. il s'agira donc par la suite de les deployer.

3. Connectez-vous en tant que admin. Cliquer sur local puis aller dans l'onglet "stacks" puis cliquez sur "add stack"

4. Maintenant il s'agit de configuer la stack donc pour cela il faut y mettre le nom, puis aller dans web editor et coller le contenue du fichier Docker compose.yml.

Cliquez ensuite sur "deploy the stack" et vérifiez que les deux serveurs sont en running. Le temps de chargement peut parraitre long, attendez un peu le temps que l'image Odoo15 ce créer.

Une fois le Docker créer vous pouvez récuperer un backup du serveur ERP.

5. Collez les fichiers de la clé USB dans un emplacement de votre ordinateur que vous souhaitez.

6. Ouvrez Le serveur ERP Odoo sur un navigateur avec ce lien : http://localhost:8069 ou aller sur le docker que vous venez de créer et cliquer sur "8069" dans la colonne "published ports".

7. Une fois sur le site, sélectionner "Gestion des bases de données" puis "Restore Database";

8. Ecrivez le Master Password (MSIR5) cliquez sur parcourir et selectionner le fichier .ZIP que vous venez de telecharger qui est dans le repertoire NomDeVotreRepertoire/SOUMSOUM, puis affecter un nom à votre Database, celui-ci doit être "SOUMSOUM";
   
9. Modifier les paramètres réseau de votre machine virtuelle pour passer en accès par pont puis valider. Changer l'adresse IP de votre machine virtuelle contenant le docker pour celle ci : 172.31.10.158. Déconnectez vous du réseau wifi sur la machine virtuelle puis reconnectez vous pour qu'il prenne en compte les modification.
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
