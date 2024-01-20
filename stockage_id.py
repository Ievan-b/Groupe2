import tkinter as tk
from tkinter import ttk, messagebox
import xmlrpc.client
from PIL import Image, ImageTk
import os

class StockUpdateApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mise à jour de stock")

        # ... (autres éléments d'initialisation)

        # Ajout du champ de saisie et du bouton de mise à jour du stock
        self.label_product_id = ttk.Label(root, text="ID de l'article:")
        self.entry_product_id = ttk.Entry(root)
        self.label_quantity = ttk.Label(root, text="Nouvelle quantité:")
        self.entry_quantity = ttk.Entry(root)
        self.update_stock_button = ttk.Button(root, text="Mettre à jour le stock", command=self.update_stock)

        self.label_product_id.grid(row=3, column=0, padx=5, pady=5)
        self.entry_product_id.grid(row=3, column=1, padx=5, pady=5)
        self.label_quantity.grid(row=4, column=0, padx=5, pady=5)
        self.entry_quantity.grid(row=4, column=1, padx=5, pady=5)
        self.update_stock_button.grid(row=5, column=0, columnspan=2, pady=10)

    def validate_update(self):
        try:
            product_id = int(self.entry_product_id.get())
            new_quantity = int(self.entry_quantity.get())

            update_stock_quantity(product_id, new_quantity)
        except ValueError:
            print("Veuillez saisir des valeurs valides pour l'ID de l'article et la nouvelle quantité.")

    def update_stock(self):
        try:
            product_id = int(self.entry_product_id.get())
            current_quantity = int(self.entry_quantity.get())

            update_stock_quantity(product_id, current_quantity)
        except ValueError:
            print("Veuillez saisir des valeurs valides pour l'ID de l'article et la nouvelle quantité.")

def get_product_name_by_id(product_id, models, erp_db, user_id, erp_pwd):
    # Récupérer le nom de l'article en fonction de l'ID
    product_name = models.execute_kw(erp_db, user_id, erp_pwd,
                                     'stock.quant', 'read',
                                     [[product_id]],
                                     {'fields': ['display_name']})
    return product_name[0]['display_name'] if product_name else None

def update_stock_quantity(product_id, new_quantity):
    erp_ipaddr = "172.20.10.7"
    erp_port = "8069"
    erp_url = f'http://{erp_ipaddr}:{erp_port}'

    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(erp_url))
    version = common.version()

    erp_db = "Touch_db"
    erp_user = "admin"
    erp_pwd = "1234"
    user_id = common.authenticate(erp_db, erp_user, erp_pwd, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(erp_url))

    product_name = get_product_name_by_id(product_id, models, erp_db, user_id, erp_pwd)

    if product_name:
        article_before_update = models.execute_kw(erp_db, user_id, erp_pwd,
                                                  'stock.quant', 'read',
                                                  [[product_id]],
                                                  {'fields': ['quantity']})

        print(f"Ancienne quantité de l'article {product_name} (ID={product_id}): {article_before_update[0]['quantity']}")

        models.execute_kw(erp_db, user_id, erp_pwd,
                          'stock.quant', 'write',
                          [[product_id], {'quantity': new_quantity}])

        print(f"Quantité de l'article {product_name} (ID={product_id}) mise à jour avec succès!")

        article_after_update = models.execute_kw(erp_db, user_id, erp_pwd,
                                                 'stock.quant', 'read',
                                                 [[product_id]],
                                                 {'fields': ['quantity']})
        print(f"Nouvelle quantité de l'article {product_name} (ID={product_id}): {article_after_update[0]['quantity']}")
    else:
        print(f"L'article avec l'ID={product_id} n'a pas été trouvé.")

# Fonction principale
if __name__ == "__main__":
    root = tk.Tk()
    app = StockUpdateApp(root)
    root.mainloop()
