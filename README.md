Notice d'utilisation:

Sommaire:

- PC1 (ERP odoo)

- PC2 (Fichier Logistique)

- PC3 (Fichier Production)

========================================================================================

Installation de la Machine Virtuelle PC_1 sur VirtualBox :
- Assurez-vous d'avoir installé VirtualBox version "7.3.10" sur votre ordinateur.
- Démarrez la machine virtuelle PC_1.
- La machine virtuel devra être configurer en NAT afin de permettre la connexion.
- IL faudra s'assurer que odoo est en version 15 et que PostrgreSQL est en version 13.

Configuration de Portainer :
- Accédez au site internet portainer.io à l'adresse http://localhost:9000. Ce site est déjà préinstallé et contient les images nécessaires.
- Le mot de passe de portainer est "portainer"
- Connectez-vous en tant qu'administrateur.
- Cliquez sur "Local", puis allez dans l'onglet "Stacks".
- Cliquez sur "Add Stack".

Configuration de la Stack :
- Entrez un nom pour la stack.
- Allez dans le web editor et collez le contenu du fichier Docker compose.yml.
- Cliquez sur "Deploy the Stack" et vérifiez que les trois serveurs sont en running.
Si des difficulté sont rencontrer, assurez-vous qu'il n'y ai pas d'autre container occupant le port 8069, dans ce cas suprimé les container sauf celui nommées "portainer" et retenter la configuration.
Redémarer la machine virtuel peut aussi être une solution.

Configuration du Serveur ERP Odoo :
- Ouvrez le serveur ERP Odoo sur un navigateur en utilisant le lien : http://localhost:8069, ou accédez au docker que vous venez de créer et cliquez sur "8069" dans la colonne "published ports".
- Sur le site, sélectionnez "Gestion des bases de données", puis "Restore Database".
- Entrez le Master Password (MSIR5), cliquez sur "Parcourir" et sélectionnez le fichier .ZIP téléchargé dans le disque dur.
- Attribuez un nom à votre base de données, qui doit être "Touch_db".

Modification des Paramètres Réseau de la Machine Virtuelle :
- Passez en accès par pont dans les paramètres réseau de votre machine virtuelle.
- Changez l'adresse IP de votre machine virtuelle contenant le docker pour 172.31.11.13
- Déconnectez-vous du réseau wifi sur la machine virtuelle, puis reconnectez-vous pour que les modifications soient prises en compte.

========================================================================================
      
PC2 (Fichier Logistique).
Introduction:
- Le fichier Logistique comprend les instructions pour installer et exécuter le programme sur PC2.
      - L'identifiant : "Log"
      - Le moot de passe : "1234"
      - Adresse IP : 172.31.11.13
      - Version python : 3.10 (Utile selon le moyen Utiliser)
      - Version Pillow 8.4.0 (Utile selon le moyen Utiliser)

Installer la machine virtuelle PC_2 sur Virtual Box :
- Téléchargez et installez Virtual Box sur votre ordinateur.
- Créez une nouvelle machine virtuelle PC_2 et démarrez-la.

Connexion au réseau afpicfai_wifi_guests :
- Assurez-vous que la machine virtuelle est connectée au réseau afpicfai_wifi_guests.

Copier les fichiers depuis la clé USB :
- Insérez la clé USB contenant les fichiers dans votre ordinateur hôte.
- Copiez les fichiers de la clé USB vers un emplacement de votre choix sur la machine virtuelle PC_2.


Fichier.exe.

Récupérer le fichier Log.exe et l'exécuter :
- Recherchez et exécutez le fichier Log.exe sur la machine virtuelle PC_2.
- Si il y a un soucis au démarrage faire clic droit sur le fichier et Lancer dans la commande.

Si l'exécution échoue avec le fichier .exe :
- Essayez l'exécution avec le fichier .sh.
- Si cela ne fonctionne toujours pas, essayez avec le fichier .py et le fichier requierment.

Si vous utilisez le fichier .sh :
- Ce fichier vérifiera et installera Python version 3.10 et Pillow version 8.4.0, ainsi que le fichier .py.

Autrement, si vous utilisez le fichier .py et le fichier requierment :
- Le fichier .py contient l'application.
- Le fichier requirement contient l'ensemble des versions à installer pour les dépendances.

========================================================================================

PC3 (Fichier Production).
Introduction:
- Le fichier Production comprend les instructions pour installer et exécuter le programme sur PC3.
      - L'identifiant : "Prod"
      - Le moot de passe : "1234"
      - Adresse IP : 172.31.11.13
      - Version python : 3.10 (Utile selon le moyen Utiliser)
      - Version Pillow 8.4.0 (Utile selon le moyen Utiliser)
   
Installation de la Machine Virtuelle PC3 sur VirtualBox :
- Téléchargez et installez VirtualBox sur votre ordinateur.
- Créez une nouvelle machine virtuelle nommée PC3 et démarrez-la.

Connexion au Réseau AFPICFAI_WIFI_GUESTS :
- Assurez-vous que la machine virtuelle est connectée au réseau AFPICFAI_WIFI_GUESTS.

Copie des Fichiers depuis la Clé USB :
- Insérez la clé USB dans votre ordinateur hôte.
- Copiez les fichiers depuis la clé USB vers un emplacement de votre choix sur la machine virtuelle PC3.

Essai du Fichier .exe :
- Essayez d'abord d'exécuter le fichier Prod.exe sur la machine virtuelle PC3.
- Si il y a un soucis dans l'execution du fichier il y a peut être un message qui apparait, il faut developper et appuyer sur "executer quand meme".

En cas d'échec de l'exécution avec le fichier .exe :
- Essayez ensuite d'exécuter le fichier Prod.bash.
- Si cela ne fonctionne toujours pas, essayez avec le fichier Prod.py et le fichier requirements.txt.

Utilisation du Fichier .py et du Fichier Requirements.txt :
- Si vous optez pour l'utilisation du fichier Prod.py et du fichier requirements.txt :
- Le fichier Prod.py contient l'application.
- Le fichier requirements.txt contient la liste des versions requises pour les dépendances à installer.
