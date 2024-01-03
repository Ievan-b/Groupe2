import xmlrpc.client
import tkinter
import tkinter as tk
from tkinter import ttk  # Importer le module ttk pour des styles améliorés

try:
    url = "http://172.18.0.3:8069"
    db = "odoo70_mydb_1"
    username = "odoo"
    password = "myodoo"
    print ("Connexion a ODOO")
    print (f"URL = {url}")

    # Connexion au serveur Odoo
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    version = common.version()
    print(f"Odoo version={version}")
    uid = common.authenticate(db, username, password, {})

    # Vérification si l'authentification est réussie
    if uid:
        print("Authentification réussie. UID:", uid)
    else:
        print("Échec de l'authentification.")

except Exception as e:
    print(f"Une erreur s'est produite lors de la connexion : {e}")
    