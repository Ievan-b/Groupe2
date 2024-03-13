import tkinter as tk
from tkinter import ttk, messagebox
import xmlrpc.client
from PIL import Image, ImageTk
import base64
import io
import random

class ProgressWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Chargement en cours...")
        self.geometry("300x100")
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate")
        self.progress_bar.pack(expand=True, padx=20, pady=20)
        self.grab_set()  
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  

    def on_closing(self):
        pass

class ProductPage(tk.Tk):
    def __init__(self, odoo_connection, user_id, password, erp_db):
        super().__init__()
        self.title("Page de Production")
        self.attributes('-fullscreen', True)  
        self.geometry("800x600")  

        self.odoo_connection = odoo_connection
        self.user_id = user_id
        self.password = password
        self.erp_db = erp_db

        self.selected_product_frame = None  
        self.selected_product_ids = []  

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.bande_bleue = tk.Frame(self.main_frame, height=50, bg="#2E006C")
        self.bande_bleue.pack(fill="x")

        dashboard_label = tk.Label(self.bande_bleue, text="DASHBOARD", fg="white", bg="#2E006C", font=("Arial", 18, "bold"))
        dashboard_label.pack(side="left", padx=50)

        close_button = tk.Button(self.bande_bleue, text="Quitter", command=self.on_closing, width=10, height=1, bg="white", fg="black")
        close_button.pack(side="right", padx=20)

        self.notebook = ttk.Notebook(self.main_frame, height=400)  
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.main_frame, bg="white")
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        cadre_inferieur = tk.Frame(self, bg="white", bd=2, relief="solid")
        cadre_inferieur.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        bande_sup = tk.Frame(cadre_inferieur, height=30, bg="#2E006C")
        bande_sup.pack(fill="x")

        label_modification = tk.Label(bande_sup, text="-Modification quantité en stock-", fg="white", bg="#2E006C",font=("Arial", 14, "bold"))
        label_modification.pack(pady=5)

        cadre_contenu_inferieur = tk.Frame(cadre_inferieur, bg="white")
        cadre_contenu_inferieur.pack(padx=20, pady=20)

        cadre_boutons_texte = tk.Frame(cadre_contenu_inferieur, bg="white")
        cadre_boutons_texte.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=10)

        bande_inf = tk.Frame(cadre_inferieur, height=5, bg="#2E006C")
        bande_inf.pack(fill="x")



        label_quantite_sortir = tk.Label(cadre_boutons_texte, text="Quantité à sortir :", bg="white", font=("Arial", 12, "bold", "underline"))
        label_quantite_sortir.grid(row=0, column=1, padx=5, pady=5)

        bouton_moins = tk.Button(cadre_boutons_texte, text="-", command=self.decrementer_valeur)
        bouton_moins.grid(row=1, column=0, padx=5)

        value_frame = tk.Frame(cadre_boutons_texte, bg="white")
        value_frame.grid(row=1, column=1, padx=5)

        self.current_value = tk.IntVar()
        self.current_value.set(0)

        self.value_label = tk.Label(value_frame, textvariable=self.current_value, bg="white")
        self.value_label.pack()

        bouton_plus = tk.Button(cadre_boutons_texte, text="+", command=self.incrementer_valeur)
        bouton_plus.grid(row=1, column=2, padx=5)

        bouton_valider = tk.Button(cadre_boutons_texte, text="Valider", bg="green", fg="white", command=self.on_valider_click)
        bouton_valider.grid(row=1, column=3, padx=5)

        cadre_texte = tk.Frame(cadre_contenu_inferieur, bg="white")
        cadre_texte.grid(row=1, column=0, sticky="nsew", padx=(0, 20), pady=10)

        label_identification_article = tk.Label(cadre_texte, text="Identification de l'article :", bg="white", font=("Arial", 12, "bold", "underline"))
        label_identification_article.pack(padx=5, pady=10)

        self.zone_texte_article = tk.Text(cadre_texte, wrap="word", height=5, width=40, font=("Arial", 12))
        self.zone_texte_article.pack(padx=10, pady=10, fill="both", expand=True)

        cadre_image = tk.Frame(cadre_contenu_inferieur, bg="white", width=200, height=200)  
        cadre_image.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=20, pady=10)
        self.image_label = tk.Label(cadre_image, bg="white")
        self.image_label.pack(padx=5, pady=5)

        self.display_products()

    def on_closing(self):
        print("Fermeture de la fenêtre demandée...")
        self.destroy()

    def decrementer_valeur(self):
        current_value = self.current_value.get()
        if current_value > 0:
            self.current_value.set(current_value - 1)

    def incrementer_valeur(self):
        self.current_value.set(self.current_value.get() + 1)

    def load_product_image(self, article_code, size=(100, 100)):  
        try:
            product_data = self.odoo_connection.execute_kw(self.erp_db, self.user_id, self.password,
                                                             'product.template', 'search_read',
                                                             [[('default_code', '=', article_code)]],
                                                             {'fields': ['image_1920'], 'limit': 1})

            if product_data and product_data[0]['image_1920']:
                image_data = product_data[0]['image_1920']
                image_data_decoded = base64.b64decode(image_data)

                pil_image = Image.open(io.BytesIO(image_data_decoded))
                pil_image = pil_image.resize(size, Image.ANTIALIAS)

                image = ImageTk.PhotoImage(pil_image)

                return image
            else:
                print(f"Image not found for article with code '{article_code}'.")
                return None

        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def display_products(self):
        products = self.get_products()

        if not products:
            messagebox.showerror("Erreur", "Impossible de récupérer les produits depuis Odoo.")
            return

        num_columns = 8  
        num_per_page = 16  
        row_height = 10  

        num_pages = (len(products) - 1) // num_per_page + 1

        for page_num in range(num_pages):
            page_frame = tk.Frame(self.notebook)
            self.notebook.add(page_frame, text=f"Page {page_num + 1}")

            start_index = page_num * num_per_page
            end_index = min(start_index + num_per_page, len(products))

            for i in range(start_index, end_index):
                row = (i - start_index) // num_columns
                col = (i - start_index) % num_columns

                product = products[i]

                product_frame = tk.Frame(page_frame, bd=2, relief=tk.SOLID, width=200, height=row_height, bg='white')  
                product_frame.grid(row=row, column=col, padx=23, pady=5, sticky="nsew")  

                product_info = f"Nom: {product['name']}\nPrix: {product['price']}\nStock: {product['stock']}\nRéférence: {product['reference']}"

                image_data = self.load_product_image(product['reference'])

                if image_data:
                    image_label = tk.Label(product_frame, image=image_data, bg='white')
                    image_label.image = image_data
                    image_label.pack(side=tk.TOP, padx=3, pady=1)
                    image_label.bind("<Button-1>", lambda event, product_info=product_info, product_frame=product_frame: self.on_product_click(product_info, product_frame))

                else:
                    print("Failed to load image for product:", product['reference'])

                product_text = tk.Label(product_frame, text=product_info, wraplength=180)
                product_text.pack(side=tk.TOP, padx=8, pady=3)

                product_frame.columnconfigure(0, weight=1)  
                product_frame.rowconfigure(1, weight=1)  

                self.selected_product_ids.append(product['id'])  

    def get_products(self):
        products = []

        try:
            models = self.odoo_connection
            products_data = models.execute_kw(self.erp_db, self.user_id, self.password,
                                              'product.product', 'search_read',
                                              [[]],
                                              {'fields': ['name', 'list_price', 'qty_available', 'default_code', 'id']})

            for product in products_data:
                product_info = {
                    'name': product['name'],
                    'price': product['list_price'],
                    'stock': product['qty_available'],
                    'reference': product['default_code'],
                    'id': product['id']  
                }
                products.append(product_info)

        except xmlrpc.client.Error as e:
            print("Erreur lors de la récupération des produits depuis Odoo:", e)

        return products

    def on_product_click(self, product_info, product_frame):
        self.zone_texte_article.delete(1.0, tk.END)  
        self.zone_texte_article.insert(tk.END, product_info)

        if self.selected_product_frame:
            self.selected_product_frame.configure(bg='white')

        self.selected_product_frame = product_frame

        random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))

        product_frame.configure(bg=random_color)

        article_code = product_info.split("Référence: ")[1].strip()
        self.display_product_image(article_code)

    def display_product_image(self, article_code, size=(200, 200)):
        image_data = self.load_product_image(article_code, size=size)
        
        if image_data:
            self.image_label.configure(image=image_data, bg="white")
            self.image_label.image = image_data
        else:
            self.image_label.configure(image='', bg="white")

    def update_stock_quantity(self, product_id, new_quantity):
        try:
            self.odoo_connection.execute_kw(self.erp_db, self.user_id, self.password,
                                            'product.product', 'write',
                                            [[product_id], {'qty_available': new_quantity}])
            print(f"Quantité en stock mise à jour pour l'article avec l'ID {product_id}. Nouvelle quantité : {new_quantity}")
        except xmlrpc.client.Error as e:
            print(f"Erreur lors de la mise à jour de la quantité en stock pour l'article avec l'ID {product_id}: {e}")

    def on_valider_click(self):
        current_quantity = self.current_value.get()
        if self.selected_product_frame:
            product_id = self.selected_product_ids[self.notebook.index(self.notebook.select())]
            self.update_stock_quantity(product_id, current_quantity)
        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un produit avant de valider.")


class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion à Odoo")
        self.geometry("800x500")

        # Obtenez les dimensions de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = (screen_width - 800) // 2
        y_position = (screen_height - 500) // 2

        self.geometry(f"800x500+{x_position}+{y_position}")

        bande_bleue = tk.Frame(self, height=50, bg="#2E006C")
        bande_bleue.pack(fill="x", side="top")

        dashboard_label = tk.Label(bande_bleue, text="DASHBOARD", fg="white", bg="#2E006C", font=("Arial", 18, "bold"))
        dashboard_label.pack(side="left", padx=50)

        close_button = tk.Button(bande_bleue, text="Quitter", command=self.on_closing, width=10, height=1, bg="white", fg="black")
        close_button.pack(side="right", padx=20)

        bande_grise = tk.Frame(self, width=150, bg="gray")
        bande_grise.pack(side="left", fill="y")

        username_label = tk.Label(bande_grise, text="Sélectionnez l'identifiant:", fg="white", bg="gray")
        username_label.pack(pady=10)
        self.username_combobox = ttk.Combobox(bande_grise, values=["Log"])
        self.username_combobox.pack(pady=10)

        password_label = tk.Label(bande_grise, text="Mot de passe:", fg="white", bg="gray")
        password_label.pack(pady=10)
        self.password_entry = tk.Entry(bande_grise, show="*")
        self.password_entry.pack(pady=10)

        login_button = tk.Button(bande_grise, text="Connexion", command=self.validate_login, fg="white", bg="gray")
        login_button.pack(pady=10)

        image_path = "/home/user/Documents/Groupe2/Images/Logo_TouchTech_Solutions.png"

        try:
            image = Image.open(image_path)
            # Augmenter la taille de l'image
            image = image.resize((600, 400), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self, image=photo, bg="white")
            self.image_label.image = photo
            self.image_label.pack(pady=20, padx=20, side="right")
            self.image_label.pack_propagate(False)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Impossible de charger l'image.")





    def validate_login(self):
        selected_username = self.username_combobox.get()
        password = self.password_entry.get()

        if selected_username != "Log":
            messagebox.showerror("Erreur", "Nom d'utilisateur incorrect!")
            return

        self.progress_window = ProgressWindow(self)
        self.progress_window.transient(self)  

        self.odoo_connection, self.user_id, self.password, self.erp_db = self.get_models_and_user_id(selected_username, password)

        if self.user_id and self.odoo_connection:
            self.progress_window.destroy()  
            self.destroy()  
            product_page = ProductPage(self.odoo_connection, self.user_id, password, self.erp_db)
            product_page.mainloop()
        else:
            self.progress_window.destroy()  
            messagebox.showerror("Erreur", "Mot de passe incorrect!")

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
        except xmlrpc.client.Error as e:
            print("Erreur lors de la connexion à Odoo:", e)
            return None, None, None, None

    def on_closing(self):
        print("Fermeture de la fenêtre demandée...")
        self.destroy()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()