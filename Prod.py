import tkinter as tk
from tkinter import ttk

def set_fullscreen(window):
    window.attributes('-fullscreen', True)
    window.bind("<Escape>", lambda event: window.attributes("-fullscreen", False))

def on_closing(window):
    print("Fermeture de la fenêtre demandée...")
    window.attributes('-fullscreen', False)
    window.destroy()

def create_production_page(window):
    # Création de la bande bleue horizontale en haut de la fenêtre
    blue_bar = tk.Frame(window, height=50, bg="blue")
    blue_bar.pack(fill="x")

    # Ajout du texte "DASHBOARD" à gauche de la bande bleue
    dashboard_label = tk.Label(blue_bar, text="DASHBOARD", fg="white", bg="blue", font=("Arial", 12, "bold"))
    dashboard_label.pack(side="left", padx=10)

    # Ajout du bouton "Quitter" à droite de la bande bleue
    close_button = tk.Button(blue_bar, text="Quitter", command=window.destroy, width=10, height=1, bg="red", fg="white")
    close_button.pack(side="right", padx=10)

    # Ajout du texte "Production" au centre de la bande bleue
    production_label = tk.Label(blue_bar, text="Production", fg="white", bg="blue", font=("Arial", 12, "bold"))
    production_label.pack(side="left", padx=10)

if __name__ == "__main__":
    main_window = tk.Tk()
    set_fullscreen(main_window)

    # Création de la page de production
    create_production_page(main_window)

    main_window.mainloop()
