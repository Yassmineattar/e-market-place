import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

# initialisation de la base de donnees
def setup_database():
    db = sqlite3.connect('clients.db')
    cursor = db.cursor()
    # Creation des tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Articles (id INTEGER PRIMARY KEY AUTOINCREMENT,produit TEXT, prix_unitaire REAL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Clients (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, code_fidelite TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Achats (id INTEGER PRIMARY KEY AUTOINCREMENT, client_id TEXT, produit TEXT, quantite INTEGER, Total REAL, FOREIGN KEY (client_id) REFERENCES Clients(id))''')
    # verifier si la table d'achats est vide
    cursor.execute("SELECT COUNT(*) FROM Articles")
    if cursor.fetchone()[0] == 0:
        # si vide on  insere la data
        articles_data = [("Pain", 1.5),("Lait", 2.0),("Fromage", 5.0),("Fruits", 3.0),("Légumes", 2.5),("Céréales", 3.5),("Jus d'orange", 2.5),("Pâtes", 1.2),("Riz", 2.0),("Yaourt", 0.8),("Poulet", 4.5),("Boeuf", 5.5),("Poisson", 6.0),("Chocolat", 2.5),("Café", 3.0),("Thé", 2.5),("Biscuits", 2.0),("Sucre", 1.5),("Sel", 1.0),("Huile d'olive", 3.5)]
        cursor.executemany("INSERT INTO Articles (produit, prix_unitaire) VALUES (?, ?)", articles_data)
    db.commit()
    db.close()

# Client Class
class Client:
    def __init__(self, nom, prenom, code_fidelite):
        self.nom = nom
        self.prenom = prenom
        self.code_fidelite = code_fidelite

# ListeCourses Class
class ListeCourses:
    def __init__(self):
        self.produits = {}
# GUI Class
class GUI:
    bg_photo = None
    def __init__(self, master):
        self.master = master
        self.master.title("Gestion de Courses")
        self.master.geometry("1200x700")
        self.title_label = tk.Label(self.master, text="E-marketplace", font=("Helvetica", 24, 'bold'), bg="#0C2D48", fg="white")
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        self.setup_ui()

    def setup_ui(self):
        # Initialiser la connection et le cursor pour les operations du database
        self.conn = sqlite3.connect('clients.db')
        self.cursor = self.conn.cursor()
        if GUI.bg_photo is None:
            bg_image = Image.open('bg2.png')
            GUI.bg_photo = ImageTk.PhotoImage(bg_image)
        # Creation du frame pour l'organization
        self.frame = tk.Frame()
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.bg_label = tk.Label(self.frame, image=GUI.bg_photo)
        #ajouter un titre
        self.title_label = tk.Label(self.master, text="E-marketplace", font=("Helvetica", 24, 'bold'), bg="#0C2D48", fg="white")
        self.title_label.place(relx=0.5, rely=0.2, anchor='center')
        self.bg_label.place(relwidth=1, relheight=1)
        self.center_frame = tk.Frame(self.frame, bg="#0C2D48")
        self.center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.5)

        # Client Section
        self.client_frame = tk.LabelFrame(self.center_frame, text="Gestion des Clients", bg="#0C2D48", fg="white",font=("Helvetica", 14, 'bold'))
        self.client_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        label_width = 15
        entry_width = 20
        label_anchor = 'w'
        entry_anchor = 'w'

        # Creer un dictionaire pour faciliter la tache des labels et entrées
        client_entries = {
            "Nom :": "entry_nom_client",
            "Prénom :": "entry_prenom_client",
            "Code fidélité:": "entry_carte_client"
        }
        for i, (label_text, entry_attr) in enumerate(client_entries.items()):
            label = tk.Label(self.client_frame, text=label_text, anchor=label_anchor, width=label_width, bg="#0C2D48",fg="white", font=('Helvetica', 12, 'bold'))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            setattr(self, entry_attr, tk.Entry(self.client_frame))
            entry = getattr(self, entry_attr)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        # Boutton pour ajouter client
        tk.Button(self.client_frame, text="Ajouter Client", command=self.ajouter_client, bg="#E0E0E0", fg="black",font=("Helvetica", 12, 'bold')).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        self.shopping_list_frame = tk.LabelFrame(self.center_frame, text="Liste de Courses", bg="#0C2D48", fg="white",font=("Helvetica", 14, 'bold'))
        self.shopping_list_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        label_padx = 10
        entry_padx = 10
        button_padx = 10
        label_pady = 5
        entry_pady = 5
        button_pady = 10

        #section Article
        tk.Label(self.shopping_list_frame, text="Article:", bg="#0C2D48", fg="white",font=('Helvetica', 12, 'bold')).grid(row=0, column=0, padx=label_padx, pady=label_pady, sticky="e")
        self.articles = ["Pain", "Lait", "Fromage", "Fruits", "Légumes", "Céréales", "Jus d'orange", "Pâtes", "Riz","Yaourt", "Poulet", "Boeuf", "Poisson", "Chocolat", "Café", "Thé", "Biscuits", "Sucre", "Sel","Huile d'olive"]
        self.selected_article = tk.StringVar()
        self.selected_article.set(self.articles[0])
        article_menu = tk.OptionMenu(self.shopping_list_frame, self.selected_article, *self.articles)
        article_menu.grid(row=0, column=1, padx=entry_padx, pady=entry_pady, sticky="ew")

        # label de l'entree de la quantite
        tk.Label(self.shopping_list_frame, text="Quantité:", bg="#0C2D48", fg="white",font=('Helvetica', 12, 'bold')).grid(row=0, column=2, padx=label_padx, pady=label_pady, sticky="e")
        self.quantite_entry = tk.Entry(self.shopping_list_frame)
        self.quantite_entry.grid(row=0, column=3, padx=entry_padx, pady=entry_pady, sticky="ew")

        # Bouttons pour ajouter article
        ajouter_article_button = tk.Button(self.shopping_list_frame, text="Ajouter Article",command=self.ajouter_produit, bg="#E0E0E0", fg="black",font=("Helvetica", 12, 'bold'))
        ajouter_article_button.grid(row=1, column=0, columnspan=2, padx=button_padx, pady=button_pady, sticky="ew")

        afficher_prix_button = tk.Button(self.shopping_list_frame, text="Afficher prix", command=self.afficher_liste,bg="#E0E0E0", fg="black", font=("Helvetica", 12, 'bold'))
        afficher_prix_button.grid(row=1, column=2, columnspan=2, padx=button_padx, pady=button_pady, sticky="ew")
        # Prix total label
        tk.Label(self.shopping_list_frame, text="Prix Total:", bg="#0C2D48", fg="white",font=('Helvetica', 12, 'bold')).grid(row=2, column=0, padx=label_padx, pady=label_pady, sticky="e")
        self.label_prix_total = tk.Label(self.shopping_list_frame, text="", bg="#0C2D48", fg="white",font=("Helvetica", 16, 'bold'))
        self.label_prix_total.grid(row=2, column=1, padx=entry_padx, pady=entry_pady, sticky="ew")
        # Configurer grid column
        self.shopping_list_frame.grid_columnconfigure(1, weight=1)
        self.shopping_list_frame.grid_columnconfigure(3, weight=1)
        self.search_frame = tk.Frame(self.client_frame, bg="#0C2D48")
        self.search_frame.grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.search_frame.grid_columnconfigure(0, weight=1)  # Allow the search entry to expand
        # entree pour la recherche d'article
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        # boutton de recherche
        search_button_width = 15
        self.search_button = tk.Button(self.search_frame, text="Rechercher", command=self.search_product,width=search_button_width)
        self.search_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.search_result_label = tk.Label(self.client_frame, text="", bg="#0C2D48", fg="white", anchor='w')
        self.search_result_label.grid(row=6, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.client_frame.grid_rowconfigure(5, weight=0)  # The search frame should not expand vertically
        self.client_frame.grid_rowconfigure(6, weight=1)  # Allow the search results to expand vertically
        self.client_frame.grid_columnconfigure(1, weight=1)

        self.caisse_button = tk.Button(self.shopping_list_frame, text="Passer à la caisse", bg="#E0E0E0", fg="black",font=("Helvetica", 12, 'bold'), command=self.passer_a_la_caisse)
        self.caisse_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.shopping_list_frame.grid_columnconfigure(0, weight=1)
        self.shopping_list_frame.grid_columnconfigure(1, weight=1)
        self.shopping_list_frame.grid_columnconfigure(2, weight=1)
        self.shopping_list_frame.grid_columnconfigure(3, weight=1)
    #Partie fonctions
    def ajouter_client(self):
        nom_client = self.entry_nom_client.get()
        prenom_client = self.entry_prenom_client.get()
        carte_client = self.entry_carte_client.get()
        # verifier si la carte de fidélité existe déjà
        self.cursor.execute("SELECT id FROM Clients WHERE code_fidelite=?", (carte_client,))
        existing_client_id = self.cursor.fetchone()

        if existing_client_id:
            messagebox.showerror("Erreur", f"Le client avec la carte de fidélité '{carte_client}' existe déjà.")
        else:
            # Inserer le client dans la base de donnees
            self.cursor.execute("INSERT INTO Clients (nom, prenom, code_fidelite) VALUES (?, ?, ?)",
                                (nom_client, prenom_client, carte_client))
            self.conn.commit()
            messagebox.showinfo("Client ajouté",
                                f"Client ajouté :\nNom: {nom_client}\nPrénom: {prenom_client}\nCarte de fidélité: {carte_client}")

    def ajouter_produit(self):
        selected_article = self.selected_article.get()
        quantite = int(self.quantite_entry.get())

        # trouver le prix unitaire de la tables des Articles
        self.cursor.execute("SELECT prix_unitaire FROM Articles WHERE produit=?", (selected_article,))
        result = self.cursor.fetchone()

        if result:
            prix_unitaire = result[0]
            total_price = quantite * prix_unitaire

            # chercher le client ID avec le code_fidelite
            code_fidelite = self.entry_carte_client.get()
            self.cursor.execute("SELECT id FROM Clients WHERE code_fidelite=?", (code_fidelite,))
            client_id_result = self.cursor.fetchone()

            if client_id_result:
                client_id = client_id_result[0]

                # Inserer le produit avec le prix total dans Achats table
                self.cursor.execute("INSERT INTO Achats (client_id, produit, quantite, Total) VALUES (?, ?, ?, ?)",
                                    (client_id, selected_article, quantite, total_price))
                self.conn.commit()
                messagebox.showinfo("Produit ajouté", f"Produit ajouté à la liste :\nClient ID: {client_id}\nProduit: {selected_article}\nQuantité: {quantite}\nPrix Total: {total_price}€")
            else:
                messagebox.showerror("Erreur", "Client non trouvé avec le code de fidélité fourni.")
        else:
            messagebox.showwarning("Prix non trouvé", f"Le prix unitaire pour '{selected_article}'n'a pas été trouvé dans la base de données.")

    def afficher_liste(self):
        code_fidelite = self.entry_carte_client.get()
        self.cursor.execute("SELECT id FROM Clients WHERE code_fidelite=?", (code_fidelite,))
        client_id_result = self.cursor.fetchone()
        if client_id_result:
            client_id = client_id_result[0]
            self.cursor.execute("SELECT SUM(Total) FROM Achats WHERE client_id=?", (client_id,))
            total_result = self.cursor.fetchone()

            if total_result and total_result[0] is not None:
                total_achats = total_result[0]
                self.label_prix_total.config(text=f"{total_achats} €")
            else:
                self.label_prix_total.config(text="0 €")
                messagebox.showinfo("Liste de Courses", "La liste de courses est vide pour ce client.")
        else:
            self.label_prix_total.config(text="0 €")
            messagebox.showwarning("Erreur", "Client non trouvé avec le code de fidélité fourni.")
    def search_product(self):
        # Récupérer le terme de recherche
        search_term = self.search_entry.get().strip()  # strip() pour enlever les espaces blancs
        # Effectuer la recherche avec une correspondance insensible à la casse
        self.cursor.execute("SELECT produit, prix_unitaire FROM Articles WHERE produit LIKE ?", ('%' + search_term + '%',))
        result = self.cursor.fetchone()
        # Afficher le résultat
        if result:
            product_name, product_price = result
            self.search_result_label.config(text=f"{product_name}: {product_price}€")
        else:
            self.search_result_label.config(text="Article non trouvé.")

    def update_product_display(self):
        # supprimer les anciennes recherches
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        search_term = self.search_entry.get()
        products = self.search_articles(search_term)
        # Mettre à jour le cadre avec les produits trouvés
        for product in products:
            product_name = product[1]
            product_price = product[2]
            tk.Label(self.results_frame, text=f"{product_name} - {product_price}€").pack()

    def passer_a_la_caisse(self):
        # Functionality for the checkout process
        messagebox.showinfo("Checkout", "Vous allez maintenant passer à la caisse.")

    def __del__(self):
        self.conn.close()
# Main Application
if __name__ == "__main__":
    setup_database()
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
