import tkinter as tk
import xmlrpc.client
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

# Déclaration des variables globales
global odoo_connection
global article_code
article_code = 80001
url = 'http://192.168.201.216:8069'
db = 'Touch_db'
username = "Log"
password = "1234"


def set_fullscreen(window):
    window.attributes('-fullscreen', True)
    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))


def on_closing(window):
    print("Fermeture de la fenêtre demandée...")
    window.attributes('-fullscreen', False)
    window.destroy()


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


def Connect(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            return models
        else:
            print("Connexion échouée : Authentification impossible")
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect!")
            return None
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None


def load_product_image(article_code):
    try:
        adjusted_article_code = article_code - 80000  # Ajustez le numéro du fichier image
        image_path = f"/home/user/Documents/Groupe2-2/image_produit_{adjusted_article_code}.png"

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


def get_total_articles(models, db, uid, password):
    try:
        total_articles = models.execute_kw(db, uid, password,
                                           'product.template', 'search_count',
                                           [[]])
        return total_articles
    except Exception as e:
        print(f"Erreur lors de la récupération du nombre total d'articles : {e}")
        return None


def select_article(index):
    selected_article_code = article_code + index
    selected_article_name = get_article_name(odoo_connection, db, 2, password, selected_article_code)
    selected_article_price = get_article_price(odoo_connection, db, 2, password, selected_article_name)
    selected_article_stock = get_article_stock(odoo_connection, db, 2, password, selected_article_name)

    selected_article_info = (
        f"Article sélectionné : {selected_article_name}\n"
        f"Prix : {selected_article_price['price']}\n"
        f"Stock : {selected_article_stock}"
    )

    # Efface le contenu existant de la zone de texte globale
    zone_texte_globale.delete("1.0", tk.END)

    # Ajoute les nouvelles informations à la zone de texte globale
    zone_texte_globale.insert(tk.END, selected_article_info + "\n\n")


def create_production_page(window):
    global article_code, odoo_connection

    odoo_connection = Connect(url, db, username, password)

    # Obtenez le nombre total d'articles
    total_articles = get_total_articles(odoo_connection, db, 2, password)

    if total_articles is None:
        messagebox.showerror("Erreur", "Impossible de récupérer le nombre total d'articles.")
        return

    nombre_articles = total_articles  # Utilisez le nombre total d'articles

    colonnes_par_ligne = 8
    articles_par_page = 16

    # Cadre principal pour les informations des articles
    cadre_principal = ttk.Frame(window, padding="10")
    cadre_principal.pack(pady=5)

    # Utilisation de Notebook pour paginer les pages d'articles
    notebook = ttk.Notebook(cadre_principal)
    notebook.pack(fill="both", expand=True)

    for page_num in range(0, nombre_articles, articles_par_page):
        # Créer une nouvelle page pour chaque groupe d'articles
        page_frame = ttk.Frame(notebook)
        notebook.add(page_frame, text=f"Page {page_num // articles_par_page + 1}")

        # Utilisation d'une grille pour organiser les articles en colonnes et lignes
        for i in range(page_num, min(page_num + articles_par_page, nombre_articles)):
            # Calcul des coordonnées dans la grille de la page
            row = (i - page_num) // colonnes_par_ligne
            column = (i - page_num) % colonnes_par_ligne

            cadre_texte = ttk.Frame(page_frame)
            cadre_texte.grid(row=row, column=column, padx=10, pady=10)

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

            # Ajout du Label pour afficher l'image
            image_label = tk.Label(cadre_texte)
            product_image = load_product_image(article_code + i)
            if product_image:
                image_label.config(image=product_image)
                image_label.image = product_image
                image_label.pack(side="top", padx=10)

            texte = f"Nom: {article_name}\nPrix: {article_price['price']}\nCode: {article_code + i}\nStock: {article_stock}"
            zone_texte = tk.Text(cadre_texte, wrap="word", height=5, width=22, font=("Arial", 12))
            zone_texte.insert("1.0", texte)
            zone_texte.configure(state="normal")
            zone_texte.pack()

            # Ajout du bouton "Select" centré en bas du cadre
            select_button = tk.Button(cadre_texte, text="Select", command=lambda i=i: select_article(i))
            select_button.pack(side="bottom", pady=5, anchor="s")


# Fonction principale
if __name__ == "__main__":
    main_window = tk.Tk()
    set_fullscreen(main_window)

    # Création de la page de production
    create_production_page(main_window)

    # Création d'une zone de texte en dessous des pages
    zone_texte_globale = tk.Text(main_window, wrap="word", height=5, width=80, font=("Arial", 12))
    zone_texte_globale.pack(pady=10)

    main_window.mainloop()
