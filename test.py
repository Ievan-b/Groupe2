import tkinter as tk
from tkinter import ttk
import xmlrpc.client

def initialize_odoo_connection():
    url = 'http://localhost:8069'
    db = 'Touch_db'
    username = 'Log'
    password = '1234'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    print("Common:", common)
    uid = common.authenticate(db, username, password, {})
    print("UID:", uid)
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    print("Models:", models)

    return models, db, uid, password

def restart_script():
    # Ajoutez le code nécessaire pour redémarrer le script si nécessaire
    pass

def set_fullscreen(window):
    window.attributes('-fullscreen', True)
    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

def on_closing(window):
    print("Fermeture de la fenêtre demandée...")
    window.attributes('-fullscreen', False)
    window.destroy()

def get_article_name(models, db, uid, password, article_code):
    try:
        search_result = models.execute_kw(
            db, uid, password,
            'product.template', 'search',
            [[('default_code', '=', article_code)]],
            {'limit': 1}
        )
        print("Search Result:", search_result)

        article_ids = models.execute_kw(
            db, uid, password,
            'product.template', 'search',
            [[('default_code', '=', article_code)]],
            {'limit': 1}
        )
        print("Article IDs:", article_ids)

        if article_ids:
            article_data = models.execute_kw(
                db, uid, password,
                'product.template', 'read',
                [article_ids[0]], {'fields': ['name']}
            )
            print("Article Data:", article_data)

            if article_data:
                return article_data[0]['name']
            else:
                print(f"Article avec le code '{article_code}' trouvé mais impossible de récupérer le nom.")
                return None
        else:
            print(f"Aucun article trouvé avec le code '{article_code}'.")
            return None
    except Exception as e:
        print(f"Erreur lors de la recherche de l'article avec le code '{article_code}': {e}")
        return None

def get_article_price(models, db, uid, password, article_name):
    try:
        article_data = models.execute_kw(db, uid, password,
                                         'product.template', 'search_read',
                                         [[('name', '=', article_name)]],
                                         {'fields': ['list_price'], 'limit': 1})
        if article_data:
            return {'price': article_data[0]['list_price']}
        else:
            print(f"Article '{article_name}' trouvé mais impossible de récupérer les informations.")
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
    
def create_production_page(window, odoo_connection, db, password):
    bande_bleue = tk.Frame(window, height=250, bg="blue")
    bande_bleue.pack(fill="x")

    dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 18, "bold"))
    dashboard_label.pack(side="left", padx=50)

    logistique_label = tk.Label(bande_bleue, text="-Logistique-", fg="white", bg="blue", font=("Arial", 14, "bold"))
    logistique_label.pack(side="left", padx=600)

    close_button = tk.Button(bande_bleue, text="Quitter", command=lambda: on_closing(window), width=10, height=1, bg="red", fg="white")
    close_button.pack(side="right", padx=20)

    restart_button = tk.Button(bande_bleue, text="LOGIN", command=restart_script, width=10, height=1, bg="green", fg="white")
    restart_button.pack(side="right", padx=5)

    cadre_principal = ttk.Frame(window, padding="10")
    cadre_principal.pack(pady=5)

    article_code = 80001
    colonnes_par_ligne = 5

    for i in range(10000):
        article_name = get_article_name(odoo_connection, db, 2, password, article_code + i)

        if not article_name:
            print(f"Article avec le code '{article_code + i}' non trouvé.")
            break

        article_price = get_article_price(odoo_connection, db, 2, password, article_name)
        article_stock = get_article_stock(odoo_connection, db, 2, password, article_name)

        cadre_texte = ttk.Frame(cadre_principal)
        cadre_texte.grid(row=i // colonnes_par_ligne, column=i % colonnes_par_ligne, padx=10, pady=10)

        texte = f"Nom: {article_name}\n" \
                f"Prix: {article_price['price']}\n" \
                f"Code: {article_code + i}\n" \
                f"Stock: {article_stock}"
        zone_texte = tk.Text(cadre_texte, wrap="word", height=5, width=30, font=("Arial", 12))
        zone_texte.insert("1.0", texte)
        zone_texte.configure(state="normal")
        zone_texte.pack()

if __name__ == "__main__":
    main_window = tk.Tk()
    set_fullscreen(main_window)

    odoo_connection = initialize_odoo_connection()  # Remplacez cela par votre logique d'initialisation
    db = "Log"
    password = "1234"

    # Création de la page de production
    create_production_page(main_window, odoo_connection, db, password)

    main_window.mainloop()
