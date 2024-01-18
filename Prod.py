import tkinter as tk
from tkinter import ttk
from tkinter.tix import Tree
import xmlrpc.client

def set_fullscreen(window):
    window.attributes('-fullscreen', True)
    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

def on_closing(window):
    print("Fermeture de la fenêtre demandée...")
    window.attributes('-fullscreen', False)
    window.destroy()

def create_table(data, parent_frame):
    tree = ttk.Treeview(parent_frame)
    tree["columns"] = ("ID", "Référence", "Date prévue", "Nom de l'article", "Quantité produite", "Quantité à produire")

    for column in tree["columns"]:
        tree.column(column, anchor="center", width=100)
        tree.heading(column, text=column)

    for item in data:
        tree.insert("", "end", values=item)

    tree.pack(expand=True, fill="both")

def create_dashboard_page(window, erp_url, erp_db, user_id):
    blue_bar = tk.Frame(window, height=50, bg="blue")
    blue_bar.pack(fill="x")

    dashboard_label = tk.Label(blue_bar, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 12, "bold"))
    dashboard_label.pack(side="left", padx=10)

    close_button = tk.Button(blue_bar, text="Quitter", command=window.destroy, width=10, height=1, bg="red", fg="white")
    close_button.pack(side="right", padx=10)

    production_label = tk.Label(blue_bar, text="Production", fg="white", bg="blue", font=("Arial", 12, "bold"))
    production_label.pack(side="left", padx=10)

    production_ids = models.execute_kw(erp_db, user_id, '1234',
                                       'mrp.production', 'search', [[]])

    data = []
    for production_id in production_ids:
        production_info = models.execute_kw(erp_db, user_id, '1234',
                                            'mrp.production', 'read',
                                            [production_id],
                                            {'fields':['id', 'name', 'date_planned_start', 'product_id', 'qty_produced', 'product_qty']})
        if production_info:
            reference = production_info[0]['name']
            date_planned = production_info[0]['date_planned_start']
            product_name = production_info[0]['product_id'][1] if 'product_id' in production_info[0] else ''
            qty_produced = production_info[0]['qty_produced']
            qty_to_produce = production_info[0]['product_qty']
            data.append((production_id, reference, date_planned, product_name, qty_produced, qty_to_produce))
        else:
            print(f"ID {production_id} : Informations non trouvées.")

    def on_update_quantity():
           selected_item = Tree.selection()
           if selected_item:
        # Récupérer l'ID de l'article sélectionné
            selected_id = int(Tree.item(selected_item, 'values')[0])  # L'ID est le premier élément dans la liste des valeurs

        # Récupérer la nouvelle quantité à produire à partir du champ de texte
            new_quantity = int(entry_quantity.get())

        # Appeler la fonction pour mettre à jour la quantité à produire sur Odoo
           update_quantity_to_produce(erp_url, erp_db, user_id, selected_id, new_quantity)

        # Mettre à jour la table avec les nouvelles données
           Tree.delete(*Tree.get_children())
           create_dashboard_page(main_window, erp_url, erp_db, user_id)


    def update_quantity_to_produce(erp_url, erp_db, user_id, production_id, new_quantity_to_produce):
        try:
            # Mise à jour de la quantité à produire de l'ordre de fabrication
            models.execute_kw(erp_db, user_id, '1234',
                              'mrp.production', 'write',
                              [[production_id], {'product_qty': new_quantity_to_produce}])

            print(f"Quantité à produire de l'ordre de fabrication ID {production_id} mise à jour avec succès!")

            # Vérification de la nouvelle quantité à produire
            updated_production = models.execute_kw(erp_db, user_id, '1234',
                                                  'mrp.production', 'read',
                                                  [[production_id]],
                                                  {'fields': ['product_qty']})

            print(f"Nouvelle quantité à produire de l'ordre de fabrication ID {production_id} : {updated_production[0]['product_qty']}")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la quantité à produire : {e}")

    create_table(data, window)

    # Ajouter des champs de texte et un bouton pour la mise à jour de la quantité à produire
    entry_label_id = tk.Label(window, text="ID de l'article:")
    entry_label_id.pack()

    entry_id = tk.Entry(window)
    entry_id.pack()

    entry_label_quantity = tk.Label(window, text="Nouvelle quantité à produire:")
    entry_label_quantity.pack()

    entry_quantity = tk.Entry(window)
    entry_quantity.pack()

    update_button = tk.Button(window, text="Mettre à jour", command=on_update_quantity)
    update_button.pack()

if __name__ == "__main__":
    erp_ipaddr = "192.168.201.216"
    erp_port = "8069"
    erp_url = f'http://{erp_ipaddr}:{erp_port}'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
    erp_db = "Touch_db"
    erp_user = "admin"
    erp_pwd = "1234"
    user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
    
    main_window = tk.Tk()
    set_fullscreen(main_window)

    create_dashboard_page(main_window, erp_url, erp_db, user_id)

    main_window.mainloop()
