import tkinter as tk
from tkinter import ttk, messagebox
import xmlrpc.client
import subprocess
from PIL import Image, ImageTk

# Global variables
url = 'http://172.20.10.7:8069'
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
    selected_username = username_combobox.get()
    password = password_entry.get()

    # Check the information (you can add your own verification logic here)
    odoo_models, uid = connect_to_odoo(url, db, selected_username, password)
    if odoo_models and uid:
        print("Connexion réussie à Odoo")
        company_id = get_company_id(odoo_models, db, uid, password, company_name)
        if company_id:
            print(f"L'identifiant de '{company_name}' est : {company_id}")

            # Lancer le fichier correspondant en fonction de l'identifiant
            if selected_username == "Log":
                subprocess.Popen(['python3', 'Log.py'])

            elif selected_username == "Prod":
                subprocess.Popen(['python3', 'Prod.py'])

            # Vous pouvez ajouter des conditions similaires pour d'autres identifiants si nécessaire

            # You can add code to open another window or perform other actions if needed
            # For now, I'm just printing a message
            print(f"Welcome, {selected_username}!")

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
login_window.geometry("800x500")  # Ajustez la taille de la fenêtre en fonction de vos besoins

# Obtenez les dimensions de l'écran
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()

# Calculez la position x et y pour centrer la fenêtre
x_position = int((screen_width - 800) / 2)
y_position = int((screen_height - 500) / 2)

# Placez la fenêtre au centre de l'écran
login_window.geometry(f"600x400+{x_position}+{y_position}")

# Création de la barre bleue horizontale en haut
bande_bleue = tk.Frame(login_window, height=50, bg="blue", pady=10)  # Ajustez la hauteur selon les besoins
bande_bleue.pack(fill="x", side="top")

# Ajout du texte "DASHBOARD" dans la bande bleue
dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 18, "bold"))
dashboard_label.pack(side="left", padx=10)

# Ajout du bouton "Quitter" dans la bande bleue
close_button = tk.Button(bande_bleue, text="Quitter", command=lambda: on_closing(login_window), width=10, height=1, bg="red", fg="white")
close_button.pack(side="right", padx=20)

# Création de la bande grise à gauche
bande_grise = tk.Frame(login_window, width=150, bg="gray")
bande_grise.pack(side="left", fill="y")

# Combobox for username
username_label = tk.Label(bande_grise, text="Sélectionnez l'identifiant:", fg="white", bg="gray")
username_label.pack(pady=2)
username_combobox = ttk.Combobox(bande_grise, values=["Prod", "Log"])
username_combobox.pack(pady=20)

# Fields for password
password_label = tk.Label(bande_grise, text="Mot de passe:", fg="white", bg="gray")
password_label.pack(pady=2)
password_entry = tk.Entry(bande_grise, show="*")
password_entry.pack(pady=20)

# Button to validate the login
login_button = tk.Button(bande_grise, text="Connexion", command=validate_login, fg="white", bg="gray")
login_button.pack(pady=20)

# Load and display the image on the right side
image_path = f"/home/user/Documents/Groupe2/Images/Logo_TouchTech_Solutions.png"
image = Image.open(image_path)
image = image.resize((400, 260), Image.ANTIALIAS)  # Ajustez la taille de l'image en fonction de vos besoins
photo = ImageTk.PhotoImage(image)

# Calcul de la position pour centrer l'image verticalement
y_image_position = int((400 - image.size[1]) / 2)

image_label = tk.Label(login_window, image=photo)
image_label.image = photo
image_label.place(x=210, y=y_image_position)  # Ajustez la valeur de x en fonction de vos besoins

# Start the main loop for the login window
login_window.mainloop()
