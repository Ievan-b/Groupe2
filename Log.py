import tkinter as tk
from tkinter import ttk
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
global current_value
current_value = 0
user_id = 0
models = None

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
        print(f"uid after authenticate: {uid}")  # Ajout de cette ligne pour le débogage
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

def load_product_image(article_code):
    try:
        adjusted_article_code = article_code - 80000
        image_path = f"/home/user/Documents/Groupe2-2/image_produit_{adjusted_article_code}.png"

        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, image_path)

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

def update_value(change):
    global current_value
    current_value += change
    value_label.config(text=f"{current_value}")
    print(f"Valeur actuelle mise à jour: {current_value}")

def select_article(index):
    selected_article_code = article_code + index
    selected_article_name = get_article_name(models, db, user_id, password, selected_article_code)
    selected_article_price = get_article_price(models, db, user_id, password, selected_article_name)
    selected_article_stock = get_article_stock(models, db, user_id, password, selected_article_name)

    selected_article_info = (
        f"Nom : {selected_article_name}\n"
        f"Prix : {selected_article_price['price']}\n"
        f"Stock : {selected_article_stock}\n"
        f"Code : {selected_article_code}"
    )

    zone_texte_globale.delete("1.0", tk.END)
    zone_texte_globale.insert(tk.END, selected_article_info + "\n\n")

def valider_action():
    print("Action de validation!")
    # Ajoutez ici le code que vous souhaitez exécuter lors de l'appui sur le bouton "Valider"

def update_stock():
    try:
        product_id = int(product_id_var.get())
        selected_item = ttk.Treeview.selection()[0]
        current_quantity = int(ttk.Treeview.item(selected_item, 'values')[5])
        new_quantity = int(quantity_var.get())

        updated_quantity = current_quantity - new_quantity

        models.execute_kw(db, user_id, password,
                           'stock.quant', 'write',
                           [[product_id], {'quantity': updated_quantity}])

        ttk.Treeview.set(selected_item, 'Stock', updated_quantity)

        messagebox.showinfo("Succès", "Quantité mise à jour avec succès!")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la mise à jour du stock : {e}")



def create_production_page(window):
    global article_code, odoo_connection, user_id, models, db

    odoo_connection, user_id = Connect(url, db, username, password)

    total_articles = get_total_articles(models, db, user_id, password)

    bande_bleue = tk.Frame(window, height=250, bg="blue")
    bande_bleue.pack(fill="x")

    dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 18, "bold"))
    dashboard_label.pack(side="left", padx=50)

    logistique_label = tk.Label(bande_bleue, text="-Logistique-", fg="white", bg="blue", font=("Arial", 14, "bold"))
    logistique_label.pack(side="left", padx=600)

    close_button = tk.Button(bande_bleue, text="Quitter", command=lambda: on_closing(window), width=10, height=1, bg="red", fg="white")
    close_button.pack(side="right", padx=20)

    if total_articles is None:
        messagebox.showerror("Erreur", "Impossible de récupérer le nombre total d'articles.")
        return

    nombre_articles = total_articles

    colonnes_par_ligne = 8
    articles_par_page = 16

    cadre_principal = ttk.Frame(window, padding="10")
    cadre_principal.pack(pady=5)

    notebook = ttk.Notebook(cadre_principal)
    notebook.pack(fill="both", expand=True)

    for page_num in range(0, nombre_articles, articles_par_page):
        page_frame = ttk.Frame(notebook)
        notebook.add(page_frame, text=f"Page {page_num // articles_par_page + 1}")

        for i in range(page_num, min(page_num + articles_par_page, nombre_articles)):
            row = (i - page_num) // colonnes_par_ligne
            column = (i - page_num) % colonnes_par_ligne

            cadre_texte = ttk.Frame(page_frame)
            cadre_texte.grid(row=row, column=column, padx=10, pady=10)

            article_name = get_article_name(models, db, user_id, password, article_code + i)

            if not article_name:
                print(f"Article avec le code '{article_code + i}' non trouvé.")
                break

            article_price = get_article_price(models, db, user_id, password, article_name)
            article_stock = get_article_stock(models, db, user_id, password, article_name)

            if article_name:
                print(f"Le nom de l'article avec le code '{article_code + i}' est : {article_name}")
                print(f"Le prix de l'article avec le code '{article_code + i}' est : {article_price}")
                print(f"Le stock de l'article avec le code '{article_code + i}' est : {article_stock}")

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

            select_button = tk.Button(cadre_texte, text="Select", command=lambda i=i: select_article(i))
            select_button.pack(side="bottom", pady=5, anchor="s")

# Fonction principale
if __name__ == "__main__":
    main_window = tk.Tk()
    set_fullscreen(main_window)

    odoo_connection, user_id = Connect(url, db, username, password)

    if odoo_connection:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        create_production_page(main_window)

        zone_texte_globale = tk.Text(main_window, wrap="word", height=7, width=30, font=("Arial", 12))
        zone_texte_globale.pack(pady=10)

        cadre_boutons = tk.Frame(main_window)
        cadre_boutons.pack(side="top", pady=10, padx=10)

        boutonplus = tk.Button(cadre_boutons, text="+", command=lambda: update_value(1))
        boutonplus.pack(side="right", padx=5)

        value_frame = tk.Frame(cadre_boutons, bd=2, relief="solid")
        value_frame.pack(side="right", padx=5)

        value_label = tk.Label(value_frame, text=f"{current_value}")
        value_label.pack()

        boutonmoin = tk.Button(cadre_boutons, text="-", command=lambda: update_value(-1))
        boutonmoin.pack(side="right", padx=5)

        bouton_valider = tk.Button(cadre_boutons, text="Valider", command=lambda: valider_action())
        bouton_valider.configure(bg="green", fg="white")
        bouton_valider.pack(side="right", padx=5)

        # Ajout du champ de saisie et du bouton de mise à jour du stock
        product_id_var = tk.StringVar()
        quantity_var = tk.StringVar()

        label_product_id = tk.Label(main_window, text="ID de l'article:")
        entry_product_id = tk.Entry(main_window, textvariable=product_id_var)

        label_quantity = tk.Label(main_window, text="Quantité à retirer:")
        entry_quantity = tk.Entry(main_window, textvariable=quantity_var)

        label_product_id.pack()
        entry_product_id.pack()

        label_quantity.pack()
        entry_quantity.pack()

        update_stock_button = tk.Button(main_window, text='Mettre à jour le stock', command=update_stock)
        update_stock_button.pack()

        main_window.mainloop()
