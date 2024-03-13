import tkinter as tk
from tkinter import ttk
import xmlrpc.client
import subprocess

def on_closing(window):
    print("Fermeture de la fenêtre demandée...")
    window.attributes('-fullscreen', False)
    window.destroy()

def Relogin(window):
    print("Fermeture de la fenêtre demandée...")
    window.attributes('-fullscreen', False)
    window.destroy()
    subprocess.Popen(['python3', 'Identification.py'])

def connect_to_odoo(erp_ipaddr, erp_port, erp_db, erp_user, erp_pwd):
    erp_url = f'http://{erp_ipaddr}:{erp_port}'
    common = xmlrpc.client.ServerProxy(f'{erp_url}/xmlrpc/2/common')
    version = common.version()
    user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})
    models = xmlrpc.client.ServerProxy(f'{erp_url}/xmlrpc/2/object')
    return models, user_id, erp_db, erp_pwd

def get_production_data(models, user_id, erp_db, erp_pwd):
    production_ids = models.execute_kw(erp_db, user_id, erp_pwd,
                                       'mrp.production', 'search',
                                       [[]])
    production_data = []

    for production_id in production_ids:
        production_info = models.execute_kw(erp_db, user_id, erp_pwd,
                                            'mrp.production', 'read',
                                            [production_id],
                                            {'fields': ['name', 'product_id', 'state', 'date_planned_start', 'qty_produced', 'product_qty']})

        if production_info:
            reference = production_info[0]['name']
            date_planned = production_info[0]['date_planned_start']
            product_name = production_info[0]['product_id'][1]
            qty_produced = production_info[0]['qty_produced']
            qty_to_produce = production_info[0]['product_qty']
            state = production_info[0]['state']
            production_data.append(
                (production_id, reference, date_planned, product_name, qty_produced, qty_to_produce, state))

    return production_data

def update_quantity_to_produce(models, user_id, erp_db, erp_pwd, production_id, new_quantity_to_produce):
    try:
        models.execute_kw(erp_db, user_id, erp_pwd,
                          'mrp.production', 'write',
                          [[production_id], {'product_qty': new_quantity_to_produce}])
        print(f"Quantité à produire de l'ordre de fabrication ID {production_id} mise à jour avec succès!")
    except xmlrpc.client.Error as e:
        print(f"Erreur lors de la mise à jour de la quantité à produire : {e}")

class OdooApp:
    def __init__(self, root, models, user_id, erp_db, erp_pwd):
        self.root = root
        self.root.title("Odoo Production Data")
        self.root.attributes('-fullscreen', True)  # Mettre en plein écran

        # Création de la bande bleue horizontale en haut
        bande_bleue = tk.Frame(root, height=50, bg="blue")  # Ajustez la hauteur selon les besoins
        bande_bleue.pack(fill="x")

        # Ajout du texte "DASHBOARD" dans la bande bleue
        dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 18, "bold"))
        dashboard_label.pack(side="left", padx=50)

        # Ajout du texte "-Logistique-" dans la bande bleue
        logistique_label = tk.Label(bande_bleue, text="-Logistique-", fg="white", bg="blue", font=("Arial", 14, "bold"))
        logistique_label.pack(side="left", padx=600)

        # Ajout du bouton "Quitter" dans la bande bleue
        close_button = tk.Button(bande_bleue, text="Quitter", command=lambda: on_closing(root), width=10, height=1, bg="red", fg="white")
        close_button.pack(side="right", padx=20)

        login_button = tk.Button(bande_bleue, text="Login", command=lambda: Relogin(root), width=10, height=1, bg="blue", fg="white")
        login_button.pack(side="right", padx=40)

        self.tree = ttk.Treeview(self.root)
        self.tree["columns"] = ("ID", "Référence", "Date prévue", "Nom de l'article", "Quantité produite", "Quantité à produire", "État")
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", anchor="w", width=0)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=100)

        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)

        self.tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)  # Expand et fill pour remplir tout l'écran

        self.quantity_label = ttk.Label(self.root, text="Nouvelle quantité à produire:")
        self.quantity_label.pack(pady=5)

        self.quantity_entry = ttk.Entry(self.root)
        self.quantity_entry.pack(pady=5)

        self.update_button = ttk.Button(self.root, text="Mettre à jour la quantité", command=self.update_quantity)
        self.update_button.pack(pady=10)

        self.models = models
        self.user_id = user_id
        self.erp_db = erp_db
        self.erp_pwd = erp_pwd

        self.load_data()

    def load_data(self):
        data = get_production_data(self.models, self.user_id, self.erp_db, self.erp_pwd)
        for item in data:
            self.tree.insert("", "end", values=item)

    def on_item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            quantity_to_produce = self.tree.item(selected_item)["values"][5]
            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, quantity_to_produce)

    def update_quantity(self):
        selected_item = self.tree.selection()
        if selected_item:
            production_id = self.tree.item(selected_item)["values"][0]
            new_quantity_to_produce = self.quantity_entry.get()
            update_quantity_to_produce(self.models, self.user_id, self.erp_db, self.erp_pwd, production_id, new_quantity_to_produce)
            # Actualiser l'affichage après la mise à jour
            self.tree.delete(*self.tree.get_children())
            self.load_data()

if __name__ == "__main__":
    erp_ipaddr = "192.168.201.216"
    erp_port = "8069"
    erp_db = "Touch_db"
    erp_user = "admin"
    erp_pwd = "1234"

    models, user_id, erp_db, erp_pwd = connect_to_odoo(erp_ipaddr, erp_port, erp_db, erp_user, erp_pwd)

    root = tk.Tk()
    app = OdooApp(root, models, user_id, erp_db, erp_pwd)
    root.mainloop()
