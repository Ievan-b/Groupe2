import xmlrpc.client
import tkinter
import tkinter as tk
from tkinter import ttk  # Importer le module ttk pour des styles améliorés

# Variable pour suivre l'état du bouton SHIFT
shift_button_state = False

# Paramètres de connexion à Odoo
url = "http://<VOTRE_ADRESSE_ODOO>:8069"
db = "<NOM_DE_VOTRE_BASE_DE_DONNÉES>"
username = "<VOTRE_NOM_UTILISATEUR>"
password = "<VOTRE_MOT_DE_PASSE>"

# Connexion au serveur Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Vérification si l'authentification est réussie
if uid:
    print("Authentification réussie. UID:", uid)
else:
    print("Échec de l'authentification.")


# Fonction appelée lorsqu'un bouton est cliqué
def button_click(button_number):
    global shift_button_state

    if button_number == 1:
        print("Bouton 1 cliqué. Message personnalisé pour le bouton 1.")
    elif button_number == 2:
        print("Bouton 2 cliqué. Message personnalisé pour le bouton 2.")
    elif button_number == 3:
        print("Bouton 3 cliqué. Message personnalisé pour le bouton 3.")
    elif button_number == 4:
        print("Bouton 4 cliqué. Message personnalisé pour le bouton 4.")
    elif button_number == 5:
        print("Bouton 5 cliqué. Message personnalisé pour le bouton 5.")
    elif button_number == 6:
        print("Bouton 6 cliqué. Message personnalisé pour le bouton 6.")
    elif button_number == 7:
        print("Bouton 7 cliqué. Message personnalisé pour le bouton 7.")
    elif button_number == 8:
        print("Bouton 8 cliqué. Message personnalisé pour le bouton 8.")
    elif button_number == 9:
        print("Bouton 9 cliqué. Message personnalisé pour le bouton 9.")
    elif button_number == 10:
        print("Bouton 10 cliqué. Message personnalisé pour le bouton 10.")
    elif button_number == 11:
        # Changer l'état du bouton SHIFT
        shift_button_state = not shift_button_state

        if shift_button_state:
            print("Bouton SHIFT activé.")
            button11.config(bg="green")
        else:
            print("Bouton SHIFT désactivé.")
            button11.config(bg="black")

# Fonction appelée lors de la fermeture de la fenêtre
def on_closing():
    # Retirer la configuration de la fenêtre en plein écran
    window.attributes('-fullscreen', False)
    window.destroy()

# Fonction pour fermer la fenêtre
def close_window():
    on_closing()

# Fonction pour créer un cercle
def create_circle(canvas):
    # Coordonnées du centre du cercle et de son rayon
    circle_coords = 50, 457
    circle_radius = 250

    # Coordonnées du rectangle englobant le cercle
    bbox = (circle_coords[0] - circle_radius, circle_coords[1] - circle_radius,
            circle_coords[0] + circle_radius, circle_coords[1] + circle_radius)

    # Création du cercle
    canvas.create_oval(bbox, fill="grey", outline="black")

# Fonction pour créer le deuxième cercle
def create_circle2(canvas):
    # Coordonnées du centre du deuxième cercle et de son rayon
    circle2_coords = 1500, 457
    circle_radius = 250

    # Coordonnées du rectangle englobant le deuxième cercle
    bbox = (circle2_coords[0] - circle_radius, circle2_coords[1] - circle_radius,
            circle2_coords[0] + circle_radius, circle2_coords[1] + circle_radius)

    # Création du deuxième cercle
    canvas.create_oval(bbox, fill="grey", outline="black")

# Fonction appelée lorsqu'on change la valeur du curseur
def scale_changed(value):
    formatted_value = f"{float(value):.1f}"  # Formater la valeur avec une décimale
    print(f"SPEED : {formatted_value}%")
    scale_label.config(text=f"SPEED: {formatted_value}%")

# Création de la fenêtre principale
window = tk.Tk()
window.title("Interface de Base")

# Définir la fenêtre en plein écran
window.attributes('-fullscreen', True)

# Création d'un canevas pour les formes
canvas = tk.Canvas(window, width=window.winfo_reqwidth(), height=window.winfo_reqheight())
canvas.pack(fill=tk.BOTH, expand=True)

# Ajuster les coordonnées du rectangle pour le centrer et le rendre plus grand
rectangle_width = window.winfo_reqwidth() * 2
rectangle_height = 100
rectangle_coords = (window.winfo_reqwidth() - rectangle_width) / 2, (window.winfo_reqheight() - rectangle_height) / 2, (window.winfo_reqwidth() + rectangle_width) / 2, (window.winfo_reqheight() + rectangle_height) / 2
canvas.create_rectangle(rectangle_coords, fill="blue", outline="black")
canvas.create_text(window.winfo_reqwidth() / 2, window.winfo_reqheight() / 2, text="TEACH ROBOT 5 AXES", font=("Helvetica", 24), fill="white")

# Appel de la fonction pour créer le premier cercle
create_circle(canvas)

# Appel de la fonction pour créer le deuxième cercle
create_circle2(canvas)

# Création de boutons avec place
button1 = tk.Button(window, text="-", command=lambda: button_click(1), width=10, height=3, bg="#999999", fg="white")
button1.place(relx=0.87, rely=0.35, anchor=tk.W)  # ancrage à gauche

button2 = tk.Button(window, text="+", command=lambda: button_click(2), width=10, height=3, bg="#999999", fg="white")
button2.place(relx=0.94, rely=0.35, anchor=tk.W)  # ancrage à gauche

button3 = tk.Button(window, text="-", command=lambda: button_click(3), width=10, height=3, bg="#999999", fg="white")
button3.place(relx=0.87, rely=0.44, anchor=tk.W)  # ancrage à gauche

button4= tk.Button(window, text="+", command=lambda: button_click(4), width=10, height=3, bg="#999999", fg="white")
button4.place(relx=0.94, rely=0.44, anchor=tk.W)  # ancrage à gauche

button5 = tk.Button(window, text="-", command=lambda: button_click(5), width=10, height=3, bg="#999999", fg="white")
button5.place(relx=0.87, rely=0.53, anchor=tk.W)  # ancrage à gauche

button6 = tk.Button(window, text="+", command=lambda: button_click(6), width=10, height=3, bg="#999999", fg="white")
button6.place(relx=0.94, rely=0.53, anchor=tk.W)  # ancrage à gauche

button7 = tk.Button(window, text="-", command=lambda: button_click(7), width=10, height=3, bg="#999999", fg="white")
button7.place(relx=0.87, rely=0.62, anchor=tk.W)  # ancrage à gauche

button8 = tk.Button(window, text="+", command=lambda: button_click(8), width=10, height=3, bg="#999999", fg="white")
button8.place(relx=0.94, rely=0.62, anchor=tk.W)  # ancrage à gauche

button9 = tk.Button(window, text="-", command=lambda: button_click(9), width=10, height=3, bg="#999999", fg="white")
button9.place(relx=0.87, rely=0.71, anchor=tk.W)  # ancrage à gauche

button10 = tk.Button(window, text="+", command=lambda: button_click(10), width=10, height=3, bg="#999999", fg="white")
button10.place(relx=0.94, rely=0.71, anchor=tk.W)  # ancrage à gauche

# Bouton SHIFT initial avec la couleur noire
button11 = tk.Button(window, text="SHIFT", command=lambda: button_click(11), width=10, height=3, bg="black", fg="white")
button11.place(relx=0.02, rely=0.35, anchor=tk.W)  # ancrage à gauche

# Ajout d'un curseur (scale) avec un style personnalisé
style = ttk.Style()
style.configure("TScale", background="#999999", troughcolor="#666666", sliderthickness=15)

scale_label = tk.Label(window, text="SPEED:  ")
scale_label.place(relx=0.065, rely=0.42, anchor=tk.W)
scale = ttk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=scale_changed, length=200, style="TScale")
scale.set(50)  # Valeur initiale
scale.place(relx=0.025, rely=0.45, anchor=tk.W)

# Bouton de fermeture en haut à droite
close_button = tk.Button(window, text="Quit", command=close_window, width=10, height=2, bg="red", fg="white")
close_button.place(relx=0.95, rely=0.05, anchor=tk.NE)  # ancrage à droite en haut

# Associer la fonction on_closing à la fermeture de la fenêtre
window.protocol("WM_DELETE_WINDOW", on_closing)

# Lancer la boucle principale de l'interface utilisateur
window.mainloop()
