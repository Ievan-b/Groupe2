import tkinter as tk
import xmlrpc.client
from tkinter import ttk, messagebox
import subprocess
import base64



# Global variables
url = 'http://192.168.201.216:8069'
db = 'Touch_db'
company_name = 'Touch Tech Solution'

def on_closing(window):
    print("Fermeture de la fenêtre demandée...")
    window.destroy()

def connect_to_odoo(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            return models, uid
        else:
            print("Connexion échouée : Authentification impossible")
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect!")
            return None, None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None, None

def validate_login():
    # Retrieve the information entered by the user
    username = username_entry.get()
    password = password_entry.get()

    # Check the information (you can add your own verification logic here)
    odoo_models, uid = connect_to_odoo(url, db, username, password)
    if odoo_models and uid:
        print("Connexion réussie à Odoo")
        company_id = get_company_id(odoo_models, db, uid, password, company_name)
        if company_id:
            print(f"L'identifiant de '{company_name}' est : {company_id}")

            # Si l'identification est "Log", lancer Log.py
            if username == "Log":
                subprocess.Popen(['python3', 'Log.py'])

            # Si l'identification est "Prod", lancer Prod.py
            elif username == "Prod":
                subprocess.Popen(['python3', 'Prod.py'])


            # Vous pouvez ajouter des conditions similaires pour d'autres identifiants si nécessaire

            # You can add code to open another window or perform other actions if needed
            # For now, I'm just printing a message
            print(f"Welcome, {username}!")

            # Fermer la fenêtre de connexion
            login_window.destroy()
    else:
        print("Échec de la connexion à Odoo.")

def get_company_id(models, db, uid, password, company_name):
    try:
        company_id = models.execute_kw(db, uid, password,
                                       'res.company', 'search',
                                       [[('name', '=', company_name)]],
                                       {'limit': 1})
        if company_id:
            return company_id[0]
        else:
            print(f"Entreprise '{company_name}' non trouvée.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'entreprise : {e}")
        return None

# Create the login window
login_window = tk.Tk()
login_window.title("Connexion")

# Set window size
login_window.geometry("400x300")

# Fields for username and password
username_label = tk.Label(login_window, text="Nom d'utilisateur:")
username_label.pack(pady=10)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=10)

password_label = tk.Label(login_window, text="Mot de passe:")
password_label.pack(pady=10)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=10)

# Button to validate the login
login_button = tk.Button(login_window, text="Connexion", command=validate_login)
login_button.pack(pady=20)

# Close button in the top right corner
close_button = tk.Button(login_window, text="Quit", command=lambda: on_closing(login_window), width=10, height=1, bg="red", fg="white")
close_button.place(relx=0.95, rely=0.01, anchor=tk.NE)



# Start the main loop for the login window
login_window.mainloop()
