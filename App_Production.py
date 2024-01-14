import tkinter as tk
from tkinter import ttk, messagebox
import xmlrpc.client
import subprocess

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion")
        self.set_fullscreen()

        # Champs pour le nom d'utilisateur et le mot de passe
        self.username_label = tk.Label(self, text="Nom d'utilisateur:")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self, text="Mot de passe:")
        self.password_label.pack(pady=10)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=10)

        # Bouton pour valider la connexion
        self.login_button = tk.Button(self, text="Connexion", command=self.validate_login)
        self.login_button.pack(pady=20)

        # Bouton de fermeture en haut à droite
        self.close_button = tk.Button(self, text="Quit", command=self.on_closing, width=10, height=1, bg="red", fg="white")
        self.close_button.place(relx=0.95, rely=0.01, anchor=tk.NE)

    def set_fullscreen(self):
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))

    def on_closing(self):
        print("Fermeture de la fenêtre demandée...")
        self.attributes('-fullscreen', False)
        self.destroy()

    def validate_login(self):
        # Retrieve the information entered by the user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check the information (you can add your own verification logic here)
        odoo_models, odoo_connection = self.connect_to_odoo(username, password)
        if odoo_models and odoo_connection:
            print("Connexion réussie à Odoo")
            company_id = self.get_company_id(odoo_connection, 2, password, "Touch Tech Solution")
            if company_id:
                print(f"L'identifiant de 'Touch Tech Solution' est : {company_id}")
                self.destroy()  # Fermez la fenêtre de connexion

                # Si l'identification est "Log", lancer Log.py
                if username == "Log":
                    print("Lancement de Log.py")
                    subprocess.Popen(['python', 'Log.py'])
                # Si l'identification est "Prod", lancer Prod.py
                elif username == "Prod":
                    print("Lancement de Prod.py")
                    subprocess.Popen(['python', 'Prod.py'])
                # Vous pouvez ajouter des conditions similaires pour d'autres identifiants si nécessaire
                else:
                    print(f"Identification inconnue : {username}")

                # You can add code to open another window or perform other actions if needed
                # For now, I'm just printing a message
                print(f"Welcome, {username}!")
        else:
            print("Échec de la connexion à Odoo.")

    def connect_to_odoo(self, username, password):
        try:
            url = 'http://192.168.201.216:8069'
            db = 'Touch_db'
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            if uid:
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
                return models, xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            else:
                print("Connexion échouée : Authentification impossible")
                messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect!")
                return None, None
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return None, None

    def get_company_id(self, models, uid, password, company_name):
        try:
            db = 'Touch_db'
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

if __name__ == "__main__":
    app = Application()
    app.mainloop()
