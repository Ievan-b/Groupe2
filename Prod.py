import tkinter as tk
from tkinter import ttk
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
    tree["columns"] = ("ID", "Référence", "Date prévue", "Nom de l'article", "Quantité produite", "Quantité à produire", "État")

    for column in tree["columns"]:
        tree.column(column, anchor="center", width=100)
        tree.heading(column, text=column)

    for item in data:
        tree.insert("", "end", values=item)

    tree.pack(expand=True, fill="both")

def create_dashboard_page(window):
    blue_bar = tk.Frame(window, height=50, bg="blue")
    blue_bar.pack(fill="x")

    dashboard_label = tk.Label(blue_bar, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 12, "bold"))
    dashboard_label.pack(side="left", padx=10)

    close_button = tk.Button(blue_bar, text="Quitter", command=window.destroy, width=10, height=1, bg="red", fg="white")
    close_button.pack(side="right", padx=10)

    production_label = tk.Label(blue_bar, text="Production", fg="white", bg="blue", font=("Arial", 12, "bold"))
    production_label.pack(side="left", padx=10)

    # Connexion à Odoo
    erp_ipaddr = "192.168.201.216"
    erp_port = "8069"
    erp_url = f'http://{erp_ipaddr}:{erp_port}'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
    erp_db = "Touch_db"
    erp_user = "admin"
    erp_pwd = "1234"
    user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))
    access = models.execute_kw(erp_db, user_id, erp_pwd,
                               'mrp.production', 'check_access_rights',
                               ['read'], {'raise_exception': False})

    production_ids = models.execute_kw(erp_db, user_id, erp_pwd,
                                       'mrp.production', 'search', [[]])

    data = []
    for production_id in production_ids:
        production_info = models.execute_kw(erp_db, user_id, erp_pwd,
                                            'mrp.production', 'read',
                                            [production_id],
                                            {'fields': ['id', 'name', 'date_planned_start', 'product_id', 'qty_produced', 'product_qty', 'state']})
        if production_info:
            reference = production_info[0]['name']
            date_planned = production_info[0]['date_planned_start']
            product_name = production_info[0]['product_id'][1] if 'product_id' in production_info[0] else ''
            qty_produced = production_info[0]['qty_produced']
            qty_to_produce = production_info[0]['product_qty']
            state = production_info[0]['state']
            data.append((production_id, reference, date_planned, product_name, qty_produced, qty_to_produce, state))
        else:
            print(f"ID {production_id} : Informations non trouvées.")

    create_table(data, window)

if __name__ == "__main__":
    main_window = tk.Tk()
    set_fullscreen(main_window)

    create_dashboard_page(main_window)

    main_window.mainloop()