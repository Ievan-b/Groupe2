import tkinter as tk
from tkinter import ttk, messagebox
import xmlrpc.client
from PIL import Image, ImageTk


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion à Odoo")
        self.geometry("600x400")
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = (screen_width - 600) // 2
        y_position = (screen_height - 400) // 2

        self.geometry(f"600x400+{x_position}+{y_position}")

        bande_bleue = tk.Frame(self, height=50, bg="#2E006C")
        bande_bleue.pack(fill="x", side="top")

        dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="#2E006C", font=("Arial", 18, "bold"))
        dashboard_label.pack(side="left", padx=10)

        close_button = tk.Button(bande_bleue, text="Quitter", command=self.on_closing, width=10, height=1, bg="white", fg="black")
        close_button.pack(side="right", padx=20)

        bande_grise = tk.Frame(self, width=150, bg="gray")
        bande_grise.pack(side="left", fill="y")

        username_label = tk.Label(bande_grise, text="Sélectionnez l'identifiant:", fg="white", bg="gray")
        username_label.pack(pady=2)
        self.username_combobox = ttk.Combobox(bande_grise, values=["Prod"])
        self.username_combobox.pack(pady=20)

        password_label = tk.Label(bande_grise, text="Mot de passe:", fg="white", bg="gray")
        password_label.pack(pady=2)
        self.password_entry = tk.Entry(bande_grise, show="*")
        self.password_entry.pack(pady=20)

        login_button = tk.Button(bande_grise, text="Connexion", command=self.validate_login, fg="white", bg="gray")
        login_button.pack(pady=20)

        image_path = "/home/user/Documents/Groupe2/Images/Logo_TouchTech_Solutions.png"
        image = Image.open(image_path)
        image = image.resize((400, 260), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)

        y_image_position = int((400 - image.size[1]) / 2)

        image_label = tk.Label(self, image=photo)
        image_label.image = photo
        image_label.place(x=210, y=y_image_position)

    def validate_login(self):
        selected_username = self.username_combobox.get()
        password = self.password_entry.get()

        if selected_username != "Prod":
            print("Seul l'identifiant 'Prod' est autorisé.")
            return

        odoo_models, uid, erp_pwd, erp_db = self.get_models_and_user_id(selected_username, password)

        if uid and odoo_models:
            self.destroy()
            app = OdooApp(odoo_models, uid, erp_pwd, erp_db)
            app.mainloop()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect!")


    def get_models_and_user_id(self, username, password):
        erp_ipaddr = "172.31.11.13"
        erp_port = "8069"
        erp_db = "Touch_db"

        try:
            erp_url = f'http://{erp_ipaddr}:{erp_port}'
            common = xmlrpc.client.ServerProxy(f'{erp_url}/xmlrpc/2/common')
            user_id = common.authenticate(erp_db, username, password, {})
            models = xmlrpc.client.ServerProxy(f'{erp_url}/xmlrpc/2/object')

            return models, user_id, password, erp_db
        except xmlrpc.client.Error:
            return None, None, None, None

    def on_closing(self):
        print("Fermeture de la fenêtre demandée...")
        self.destroy()


class OdooApp(tk.Tk):
    def __init__(self, models, user_id, erp_pwd, erp_db):
        super().__init__()
        self.title("Odoo Production Data")
        self.attributes('-fullscreen', True)
        self.models = models
        self.user_id = user_id
        self.erp_pwd = erp_pwd
        self.erp_db = erp_db

        bande_bleue = tk.Frame(self, height=50, bg="#2E006C")  
        bande_bleue.pack(fill="x")

        dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="#2E006C", font=("Arial", 18, "bold"))
        dashboard_label.pack(side="left", padx=50)

        logistique_label = tk.Label(bande_bleue, text="-Production-", fg="white", bg="#2E006C", font=("Arial", 14, "bold"))
        logistique_label.pack(side="left", padx=600)

        close_button = tk.Button(bande_bleue, text="Quitter", command=self.on_closing, width=10, height=1,
                                  bg="white", fg="black")
        close_button.pack(side="right", padx=20)

        self.tree = ttk.Treeview(self)
        self.tree["columns"] = ("ID", "Référence", "Date prévue", "Nom de l'article", "Quantité produite",
                                "Quantité à produire", "État")
        self.tree.heading("#0", text="", anchor="w")
        self.tree.column("#0", anchor="w", width=0)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, anchor="w", width=100)

        self.tree.bind("<ButtonRelease-1>", self.on_item_selected)

        self.tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)  # Expand et fill pour remplir tout l'écran

        self.quantity_label = ttk.Label(self, text="Nouvelle quantité à produire:")
        self.quantity_label.pack(pady=5)

        self.quantity_entry = ttk.Entry(self)
        self.quantity_entry.pack(pady=5)

        self.update_button = ttk.Button(self, text="Mettre à jour la quantité", command=self.update_quantity)
        self.update_button.pack(pady=10)

        self.load_data()

    def load_data(self):
        data = self.get_production_data()
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
            self.update_quantity_to_produce(production_id, new_quantity_to_produce)
            self.tree.delete(*self.tree.get_children())
            self.load_data()

    def get_production_data(self):
        try:
            production_ids = self.models.execute_kw(self.erp_db, self.user_id, self.erp_pwd,
                                                     'mrp.production', 'search', [[]])
            production_data = []

            for production_id in production_ids:
                production_info = self.models.execute_kw(self.erp_db, self.user_id, self.erp_pwd,
                                                          'mrp.production', 'read',
                                                          [production_id],
                                                          {'fields': ['name', 'product_id', 'state', 'date_planned_start',
                                                                      'qty_produced', 'product_qty']})

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
        except xmlrpc.client.Error:
            return []

    def update_quantity_to_produce(self, production_id, new_quantity_to_produce):
        try:
            self.models.execute_kw(self.erp_db, self.user_id, self.erp_pwd,
                                    'mrp.production', 'write',
                                    [[production_id], {'product_qty': new_quantity_to_produce}])
            print(f"Quantité à produire de l'ordre de fabrication ID {production_id} mise à jour avec succès!")
        except xmlrpc.client.Error as e:
            print(f"Erreur lors de la mise à jour de la quantité à produire : {e}")

    def on_closing(self):
        print("Fermeture de la fenêtre demandée...")
        self.attributes('-fullscreen', False)
        self.destroy()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
