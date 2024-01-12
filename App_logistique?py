import tkinter as tk
import xmlrpc.client
import base64
import io
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import math
import sys
import subprocess
from tkinter import Canvas, PhotoImage
from tkinter import PhotoImage

def restart_script():
    python_executable = sys.executable
    script_path = sys.argv[0]
    subprocess.Popen([python_executable, script_path])
    sys.exit()


class SauvegardeurImageProduitOdoo:
    def __init__(self, url, db, nom_utilisateur, mot_de_passe, nom_societe):
        self.url = url
        self.db = db
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.nom_societe = nom_societe
        self.models = self.configurer_connexion()

    def configurer_connexion(self):
        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            uid = common.authenticate(self.db, self.nom_utilisateur, self.mot_de_passe, {})
            if uid:
                models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object', allow_none=True)
                models.uid = uid
                return models
            else:
                print("Échec de l'authentification.")
                return None
        except Exception as e:
            print(f"Erreur lors de la configuration de la connexion : {e}")
            return None

    def obtenir_ids_produits(self):
        try:
            ids_produits = self.models.execute_kw(
                self.db, self.models.uid, self.mot_de_passe,
                'product.template', 'search', [[]]
            )
            return ids_produits
        except Exception as e:
            print(f"Erreur lors de la récupération des identifiants de produits : {e}")
            return []

    def sauvegarder_image_produit(self, id_produit, nom_image):
        try:
            produit = self.models.execute_kw(
                self.db, self.models.uid, self.mot_de_passe,
                'product.template', 'read',
                [id_produit],
                {'fields': ['image_1920']}
            )

            if produit and produit[0].get('image_1920'):
                bytes_image = base64.b64decode(produit[0]['image_1920'])
                with open(f"{nom_image}_{id_produit}.png", 'wb') as fichier:
                    fichier.write(bytes_image)
                print(f"Image pour l'ID du produit {id_produit} sauvegardée sous {nom_image}_{id_produit}.png")
            else:
                print(f"Aucune image trouvée pour l'ID du produit {id_produit}")

        except Exception as e:
            print(f"Erreur lors de la sauvegarde de l'image du produit : {e}")

if __name__ == "__main__":
    url = 'http://192.168.201.216:8069'
    db = 'Touch_db'
    nom_utilisateur = 'Log'
    mot_de_passe = '1234'
    nom_societe = 'Touch Tech Solution'
    sauvegardeur_image = SauvegardeurImageProduitOdoo(url, db, nom_utilisateur, mot_de_passe, nom_societe)

    if sauvegardeur_image.models:
        print("Connexion réussie à Odoo")
        # Récupérer et afficher les ID des produits
        ids_produits = sauvegardeur_image.obtenir_ids_produits()
        print("ID des produits :", ids_produits)

        # Sauvegarder les images pour chaque produit
        for id_produit in ids_produits:
            sauvegardeur_image.sauvegarder_image_produit(id_produit, "image_produit")
    else:
        print("La connexion n'a pas été établie avec succès.")

global num_var
global Logistique
global Production
global username
global password
global article_code
global article_stock_vars
article_stock_vars = []  # Liste pour stocker les variables du stock pour chaque article
global selected_article_name

shift_button_state = False
NbSouris = 0
NbClavier = 0
NbMoniteur = 0
colonnes_par_ligne = 5

espacement_horizontal = 10
espacement_vertical = 10

url = 'http://192.168.201.216:8069'
db = 'Touch_db'
company_name = 'Touch Tech Solution'

def show_article_page():
    notebook.select(article_page)

def show_stock_page():
    notebook.select(stock_page)

def set_fullscreen(Ecran):
    Ecran.attributes('-fullscreen', True)  # Activer le mode plein écran
    Ecran.bind("<Escape>", lambda event: Ecran.attributes("-fullscreen", False))  # Pour quitter le mode plein écran en appuyant sur la touche "Échap"

def button_click(button_number):
    global shift_button_state
    shift_button_state = not shift_button_state

def on_closing(window_to_close):
    print("Fermeture de la fenêtre demandée...")
    window_to_close.attributes('-fullscreen', False)
    window_to_close.destroy()


def Validate_login():
    # Récupérez les informations saisies par l'utilisateur
    username = username_entry.get()
    password = password_entry.get()
    
    # Vérifiez les informations (vous pouvez ajouter votre propre logique de vérification ici)
    if Connect(url, db, username, password) != None: 
        odoo_models, odoo_connection = Connect(url, db, username, password)
        if odoo_models and odoo_connection:
            print("Connexion réussie à Odoo")
            company_id = Company(odoo_connection, db, 2, password, company_name)
            if company_id:
                print(f"L'identifiant de '{company_name}' est : {company_id}")
        Login.destroy()  # Fermez la fenêtre de connexion
        if username == "Log":
            Logistique(username,password)  # Affichez l'interface principale
        if username == "Prod":
            Production(username,password)  # Affichez l'interface principale

def Connect(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/objects'.format(url))
            return models,xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        else:
            print("Connexion échouée : Authentification impossible")
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect!")
            return None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

def Company(models, db, uid, password, company_name):
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

def get_article_name(models, db, uid, password, article_code):
    try:
        article_ids = models.execute_kw(db, uid, password,
                                        'product.template', 'search',
                                        [[('default_code', '=', article_code)]],
                                        {'limit': 1})
        if article_ids:
            article_data = models.execute_kw(db, uid, password,
                                             'product.template', 'read',
                                             [article_ids], {'fields': ['name']})
            if article_data:
                return article_data[0]['name']
            else:
                print(f"Article avec le code '{article_code}' trouvé mais impossible de récupérer le nom.")
                return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'article : {e}")
        return None

def get_article_price(models, db, uid, password, article_name):
    try:
        article_data = models.execute_kw(db, uid, password,
                                         'product.template', 'search_read',
                                         [[('name', '=', article_name)]],
                                         {'fields': ['list_price'], 'limit': 1})
        if article_data:
            return {
                'price': article_data[0]['list_price'],
            }
        else:
            print(f"Article '{article_name}' trouvé mais impossible de récupérer les informations.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'article : {e}")
        return None

def load_product_image(article_code):
    try:
        adjusted_article_code = article_code - 80000  # Ajustez le numéro du fichier image
        image_path = f"/home/user/Documents/Groupe2/image_produit_{adjusted_article_code}.png"

        # Utilisez le chemin relatif au répertoire actuel du script
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, image_path)

        # Vérifiez si le fichier image existe
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((100, 100), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(image)
            return tk_image
        else:
            print(f"Fichier image non trouvé : {image_path}")
            return None

    except Exception as e:
        print(f"Erreur lors du chargement de l'image : {e}")
        return None


def get_article_stock(models, db, uid, password, article_name):
    try:
        article_data = models.execute_kw(db, uid, password,
                                         'product.template', 'search_read',
                                         [[('name', '=', article_name)]],
                                         {'fields': ['qty_available'], 'limit': 1})
        if article_data:
            return article_data[0]['qty_available']
        else:
            print(f"Article '{article_name}' trouvé mais impossible de récupérer la quantité.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de la quantité de l'article : {e}")
        return None

def get_ordre_de_fab(models, db, uid, password, article_id):
    try:
        manufacturing_orders = models.execute_kw(
            db, uid, password,
            'mrp.production', 'search_read',
            [[('product_id', '=', article_id)]],
            {'fields': ['date_planned_start', 'qty_producing', 'product_qty', 'product_id'], 'limit': 1}
        )
        if manufacturing_orders:
            return {
                'date_planned_start': manufacturing_orders[0]['date_planned_start'],
                'quantity_produced': manufacturing_orders[0]['qty_producing'],
                'quantity_to_produce': manufacturing_orders[0]['product_qty'],
                'product_id': manufacturing_orders[0]['product_id']
            }
        else:
            print(f"Aucun ordre de fabrication trouvé pour l'article avec l'ID '{article_id}'.")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des détails de l'ordre de fabrication : {e}")
        return None
    
    except Exception as e:
        print(f"Erreur générale lors de la récupération de l'image : {e}")
        return None
    
label_stock_widgets = []



def create_product_page(notebook, page_number):
    page = ttk.Frame(notebook)
    notebook.add(page, text=f"Page {page_number + 1}")
    return page

def modifier_stock(article_index, increment, label_stock_value):
    current_value = int(label_stock_value.get())
    new_value = current_value + increment
    if new_value >= 0:  # Assurez-vous que la quantité reste positive
        label_stock_value.set(new_value)
    else:
        print("La quantité ne peut pas être négative.")

def init_stock_page(stock_page):
    # Création de la barre bleue horizontale en haut pour la page Stock
    bande_bleue_stock = tk.Frame(stock_page, height=250, bg="blue")  # Ajustez la hauteur selon vos besoins
    bande_bleue_stock.pack(fill="x")

    # Ajoutez d'autres éléments spécifiques à la page de stock ici
    label_stock = tk.Label(stock_page, text="Page Stock - Ajoutez vos éléments ici")
    label_stock.pack(pady=20)


def Logistique(username, password):
    Logistique = tk.Tk()
    Logistique.title("Logistique")
    set_fullscreen(Logistique)

    # Création de la barre bleue horizontale en haut
    bande_bleue = tk.Frame(Logistique, height=250, bg="blue")  # Adjust the height as needed
    bande_bleue.pack(fill="x")

    # Ajout du texte "DASHBOARD" dans la bande bleue
    dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 18, "bold"))
    dashboard_label.pack(side="left", padx=50)

    # Ajout du texte "DASHBOARD" dans la bande bleue
    dashboard_label = tk.Label(bande_bleue, text="-Logistique-", fg="white", bg="blue", font=("Arial", 14, "bold"))
    dashboard_label.pack(side="left", padx=600)

    # Ajout du bouton "Quitter" dans la bande bleue
    close_button = tk.Button(bande_bleue, text="Quitter", command=lambda: on_closing(Logistique), width=10, height=1, bg="red", fg="white")
    close_button.pack(side="right", padx=20)

    # Ajout du bouton "Recommencer" dans la bande bleue
    restart_button = tk.Button(bande_bleue, text="LOGIN", command=restart_script, width=10, height=1, bg="green", fg="white")
    restart_button.pack(side="right", padx=5)

    bande_grise_verticale = tk.Frame(Logistique, width=100, bg="gray")
    bande_grise_verticale.pack(side="left", fill="y")

    # Permet au cadre de contrôler sa propre taille
    bande_grise_verticale.pack_propagate(0)

    # Cadre principal pour les informations des articles
    cadre_principal = ttk.Frame(Logistique, padding="10")
    cadre_principal.pack(pady=5)  # Espacement par rapport à la barre latérale

    # Utilisation de Notebook pour paginer les articles
    notebook = ttk.Notebook(cadre_principal)
    notebook.pack(fill="both", expand=True)
    
    
    article_code = 80001
    colonnes_par_ligne = 5  # Définissez cette valeur si elle n'est pas définie ailleurs
    articles_par_page = 15  # Choisissez le nombre d'articles par page
    nombre_articles = 10000  # Vous pouvez obtenir cela dynamiquement si nécessaire
    nombre_pages = (nombre_articles + articles_par_page - 1) // articles_par_page
    
    for i in range(10000):
        if i == 0:
            odoo_models, odoo_connection = Connect(url, db, username, password)

        article_name = get_article_name(odoo_connection, db, 2, password, article_code + i)

        if not article_name:
            print(f"Article avec le code '{article_code + i}' non trouvé.")
            break

        article_price = get_article_price(odoo_connection, db, 2, password, article_name)
        article_stock = get_article_stock(odoo_connection, db, 2, password, article_name)

        if article_name:
            print(f"Le nom de l'article avec le code '{article_code + i}' est : {article_name}")
            print(f"Le prix de l'article avec le code '{article_code + i}' est : {article_price}")
            print(f"Le stock de l'article avec le code '{article_code + i}' est : {article_stock}")

        cadre_texte = ttk.Frame(notebook)
        cadre_texte.grid(row=i // colonnes_par_ligne, column=i % colonnes_par_ligne, padx=espacement_horizontal, pady=espacement_vertical)

        # Ajout du Label pour afficher l'image
        image_label = tk.Label(cadre_texte)
        product_image = load_product_image(article_code + i)
        if product_image:
            image_label.config(image=product_image)
            image_label.image = product_image  # Gardez une référence à l'image pour éviter la suppression par le ramasse-miettes
            image_label.pack(side="right", padx=10)

        texte = f"Nom: {article_name}\nPrix: {article_price['price']}\nCode: {article_code + i}\nStock: {article_stock}"
        zone_texte = tk.Text(cadre_texte, wrap="word", height=5, width=19, font=("Arial", 12))
        zone_texte.insert("1.0", texte)
        zone_texte.configure(state="normal")
        zone_texte.pack()
        bouton_article = tk.Button(cadre_texte, text="Select", command=lambda idx=i: action_article(idx))
        bouton_article.pack(pady=5)

    # Ajout d'une zone de texte en dessous des articles
    global entry_zone
    entry_zone = tk.Text(Logistique, wrap="word", height=5, width=50, font=("Arial", 12))
    entry_zone.pack(pady=10)

# Fonction appelée lorsque le bouton "Select" est cliqué
def action_article(index_article):
    global selected_article_name
    # Exemple : Affichez un message avec l'index de l'article sélectionné
    print(f"Bouton cliqué pour l'article avec l'index {index_article}")

    # Récupérez le nom de la machine en fonction de l'index
    selected_article_name = get_article_name(odoo_connection, db, 2, password, article_code + index_article)

    if selected_article_name:
        # Mettez à jour la zone de texte avec le nom de la machine
        entry_zone.delete("1.0", tk.END)  # Effacez le contenu existant
        entry_zone.insert(tk.END, f"Machine sélectionnée : {selected_article_name}")
    else:
        entry_zone.delete("1.0", tk.END)  # Effacez le contenu existant
        entry_zone.insert(tk.END, "Erreur : Machine non trouvée.")


    Logistique.mainloop()



def Production(username, password):
    Production = tk.Tk()
    Production.title("Production")
    set_fullscreen(Production)

    # Création de la barre bleue horizontale en haut
    bande_bleue = tk.Frame(Production, height=250, bg="blue")  # Adjust the height as needed
    bande_bleue.pack(fill="x")

    # Ajout du texte "DASHBOARD" dans la bande bleue
    dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 18, "bold"))
    dashboard_label.pack(side="left", padx=50)

    # Ajout du texte "DASHBOARD" dans la bande bleue
    dashboard_label = tk.Label(bande_bleue, text="-Production-", fg="white", bg="blue", font=("Arial", 14, "bold"))
    dashboard_label.pack(side="left", padx=550)

    # Ajout du bouton "Quitter" dans la bande bleue
    close_button = tk.Button(bande_bleue, text="Quitter", command=lambda: on_closing(Production), width=10, height=1,
                             bg="red", fg="white")
    close_button.pack(side="right", padx=20)

    # Ajout du bouton "Recommencer" dans la bande bleue
    restart_button = tk.Button(bande_bleue, text="LOGIN", command=restart_script, width=10, height=1, bg="green",
                               fg="white")
    restart_button.pack(side="right", padx=5)

    # Création du Treeview pour afficher les données
    tree = ttk.Treeview(Production, columns=("ID", "Date de début prévue", "Quantité produite", "Quantité à produire"),
                        show="headings")
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    # Définir les en-têtes de colonne
    tree.heading("ID", text="ID")
    tree.heading("Date de début prévue", text="Date de début prévue")
    tree.heading("Quantité produite", text="Quantité produite")
    tree.heading("Quantité à produire", text="Quantité à produire")

    # Définir la largeur des colonnes
    tree.column("ID", width=100)
    tree.column("Date de début prévue", width=200)
    tree.column("Quantité produite", width=150)
    tree.column("Quantité à produire", width=150)

    for i in range(10000):
        if i == 0:
            odoo_models, odoo_connection = Connect(url, db, username, password)

        manufacturing_order_details = get_ordre_de_fab(odoo_connection, db, 2, password, i + 1)

        if manufacturing_order_details:
            # Ajouter les détails à Treeview
            tree.insert("", "end", values=(
                i + 1,
                manufacturing_order_details['date_planned_start'],
                manufacturing_order_details['quantity_produced'],
                manufacturing_order_details['quantity_to_produce'],
            ))
            print(f"Détails de l'ordre de fabrication pour l'article avec l'ID '{i + 1}':")
            print(f"Date de début prévue: {manufacturing_order_details['date_planned_start']}")
            print(f"Quantité produite: {manufacturing_order_details['quantity_produced']}")
            print(f"Quantité à produire: {manufacturing_order_details['quantity_to_produce']}")
        else:
            print(f"Aucun détail d'ordre de fabrication trouvé pour l'article avec l'ID '{i + 1}'.")
            break

    Production.mainloop()


# Bouton de fermeture en haut à droite
    close_button = tk.Button(Production, text="Quit", command=lambda: on_closing(Production), width=10, height=1, bg="red", fg="white")
    close_button.place(relx=0.95, rely=0.01, anchor=tk.NE)

Login = tk.Tk()
Login.title("Connexion")
set_fullscreen(Login)

bande_bleue_login = tk.Frame(Login, height=50, bg="blue")
bande_bleue_login.pack(fill="x")

# Ajout du texte "DASHBOARD" à gauche de la bande bleue
dashboard_label = tk.Label(bande_bleue_login, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 12, "bold"))
dashboard_label.pack(side="left", padx=10)

# Champs pour le nom d'utilisateur et le mot de passe
username_label = tk.Label(Login, text="Nom d'utilisateur:")
username_label.pack(pady=10)
username_entry = tk.Entry(Login)
username_entry.pack(pady=10)

password_label = tk.Label(Login, text="Mot de passe:")
password_label.pack(pady=10)
password_entry = tk.Entry(Login, show="*")
password_entry.pack(pady=10)

# Bouton pour valider la connexion
login_button = tk.Button(Login, text="Connexion", command=Validate_login)
login_button.pack(pady=20)

close_button = tk.Button(Login, text="Quit", command=lambda: on_closing(Login), width=10, height=1, bg="red", fg="white")
close_button.place(relx=0.95, rely=0.01, anchor=tk.NE)


Login.mainloop()