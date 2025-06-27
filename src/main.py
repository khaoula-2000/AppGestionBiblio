import tkinter as tk
from tkinter import ttk, messagebox
from bibliotheque import Bibliotheque, Livre, Membre
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class BibliothequeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion de Bibliothèque")
        self.root.geometry("1200x800")
        self.setup_style()
        
        self.biblio = Bibliotheque()
        try:
            self.biblio.chargerData()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
        
        self.create_widgets()
    
    def setup_style(self):
        """Configure le style visuel de l'application"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'), padding=[10, 5])
        style.configure('TButton', font=('Helvetica', 9), padding=5)
        style.configure('TLabel', font=('Helvetica', 9))
        style.configure('TEntry', font=('Helvetica', 9))
        style.configure('Treeview', rowheight=25, font=('Helvetica', 9))
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Notebook (onglets)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Création des onglets
        self.create_livres_tab()
        self.create_membres_tab()
        self.create_emprunts_tab()
        self.create_stats_tab()
        
        # Bouton de sauvegarde
        ttk.Button(
            self.root, 
            text="Sauvegarder les données", 
            command=self.sauvegarder,
            style='TButton'
        ).pack(pady=10)
    
    def create_livres_tab(self):
        """Onglet de gestion des livres"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Livres')
        
        # Treeview pour afficher les livres
        columns = ('isbn', 'titre', 'auteur', 'annee', 'genre', 'statut')
        self.tree_livres = ttk.Treeview(
            tab, 
            columns=columns, 
            show='headings',
            selectmode='browse'
        )
        
        # Configuration des colonnes
        col_widths = [120, 250, 150, 80, 120, 100]
        for col, width in zip(columns, col_widths):
            self.tree_livres.heading(col, text=col.capitalize())
            self.tree_livres.column(col, width=width, anchor='center')
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=self.tree_livres.yview)
        self.tree_livres.configure(yscrollcommand=scrollbar.set)
        
        # Placement des widgets
        self.tree_livres.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Formulaire d'ajout
        form_frame = ttk.LabelFrame(tab, text="Ajouter un livre", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Champs de formulaire
        fields = ['isbn', 'titre', 'auteur', 'annee', 'genre']
        self.entries_livre = {}
        
        for i, field in enumerate(fields):
            ttk.Label(form_frame, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky='e', padx=5, pady=2)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky='we', padx=5, pady=2)
            self.entries_livre[field] = entry
        
        # Boutons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Ajouter", 
            command=self.ajouter_livre
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Supprimer", 
            command=self.supprimer_livre
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Actualiser", 
            command=self.actualiser_livres
        ).pack(side='right', padx=5)
        
        self.actualiser_livres()
    
    def create_membres_tab(self):
        """Onglet de gestion des membres"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Membres')
        
        # Treeview pour afficher les membres
        columns = ('id', 'nom', 'email', 'livres_empruntes')
        self.tree_membres = ttk.Treeview(
            tab, 
            columns=columns, 
            show='headings',
            selectmode='browse'
        )
        
        # Configuration des colonnes
        col_widths = [100, 200, 200, 300]
        for col, width in zip(columns, col_widths):
            self.tree_membres.heading(col, text=col.replace('_', ' ').title())
            self.tree_membres.column(col, width=width, anchor='w')
        
        # Barre de défilement
        scrollbar = ttk.Scrollbar(tab, orient='vertical', command=self.tree_membres.yview)
        self.tree_membres.configure(yscrollcommand=scrollbar.set)
        
        # Placement des widgets
        self.tree_membres.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y')
        
        # Formulaire d'inscription
        form_frame = ttk.LabelFrame(tab, text="Inscrire un membre", padding=10)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        # Champs de formulaire
        fields = ['id', 'nom', 'email']
        self.entries_membre = {}
        
        for i, field in enumerate(fields):
            ttk.Label(form_frame, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky='e', padx=5, pady=2)
            entry = ttk.Entry(form_frame)
            entry.grid(row=i, column=1, sticky='we', padx=5, pady=2)
            self.entries_membre[field] = entry
        
        # Boutons
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Inscrire", 
            command=self.inscrire_membre
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Actualiser", 
            command=self.actualiser_membres
        ).pack(side='right', padx=5)
        
        self.actualiser_membres()
    
    def create_emprunts_tab(self):
        """Onglet de gestion des emprunts"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Emprunts')
        
        # Frame principale
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Section emprunt
        frame_emprunt = ttk.LabelFrame(main_frame, text="Emprunter un livre", padding=10)
        frame_emprunt.pack(fill='x', pady=5)
        
        # Formulaire emprunt
        ttk.Label(frame_emprunt, text="ID Membre:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_emprunt_id = ttk.Entry(frame_emprunt)
        self.entry_emprunt_id.grid(row=0, column=1, sticky='we', padx=5, pady=5)
        
        ttk.Label(frame_emprunt, text="ISBN Livre:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_emprunt_isbn = ttk.Entry(frame_emprunt)
        self.entry_emprunt_isbn.grid(row=1, column=1, sticky='we', padx=5, pady=5)
        
        ttk.Button(
            frame_emprunt, 
            text="Emprunter", 
            command=self.emprunter_livre
        ).grid(row=2, column=1, pady=10, sticky='e')
        
        # Section retour
        frame_retour = ttk.LabelFrame(main_frame, text="Rendre un livre", padding=10)
        frame_retour.pack(fill='x', pady=5)
        
        # Formulaire retour
        ttk.Label(frame_retour, text="ID Membre:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.entry_retour_id = ttk.Entry(frame_retour)
        self.entry_retour_id.grid(row=0, column=1, sticky='we', padx=5, pady=5)
        
        ttk.Label(frame_retour, text="ISBN Livre:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_retour_isbn = ttk.Entry(frame_retour)
        self.entry_retour_isbn.grid(row=1, column=1, sticky='we', padx=5, pady=5)
        
        ttk.Button(
            frame_retour, 
            text="Rendre", 
            command=self.rendre_livre
        ).grid(row=2, column=1, pady=10, sticky='e')
    
    def create_stats_tab(self):
        """Onglet de statistiques"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Statistiques')
        
        # Frame pour les graphiques
        frame_graphiques = ttk.Frame(tab)
        frame_graphiques.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Graphique 1 : Répartition par genre
        frame_genre = ttk.LabelFrame(frame_graphiques, text="Répartition par genre", padding=10)
        frame_genre.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        fig_genre = self.generer_graphique_genres()
        canvas_genre = FigureCanvasTkAgg(fig_genre, master=frame_genre)
        canvas_genre.draw()
        canvas_genre.get_tk_widget().pack(fill='both', expand=True)
        
        # Graphique 2 : Top auteurs
        frame_auteurs = ttk.LabelFrame(frame_graphiques, text="Top 5 auteurs", padding=10)
        frame_auteurs.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        fig_auteurs = self.generer_graphique_auteurs()
        canvas_auteurs = FigureCanvasTkAgg(fig_auteurs, master=frame_auteurs)
        canvas_auteurs.draw()
        canvas_auteurs.get_tk_widget().pack(fill='both', expand=True)
        
        # Graphique 3 : Emprunts par mois
        frame_emprunts = ttk.LabelFrame(frame_graphiques, text="Emprunts par mois", padding=10)
        frame_emprunts.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')
        
        fig_emprunts = self.generer_graphique_emprunts()
        canvas_emprunts = FigureCanvasTkAgg(fig_emprunts, master=frame_emprunts)
        canvas_emprunts.draw()
        canvas_emprunts.get_tk_widget().pack(fill='both', expand=True)
        
        # Configuration de la grille
        frame_graphiques.columnconfigure(0, weight=1)
        frame_graphiques.columnconfigure(1, weight=1)
        frame_graphiques.rowconfigure(0, weight=1)
        frame_graphiques.rowconfigure(1, weight=1)
    
    def generer_graphique_genres(self):
        """Génère un graphique camembert des genres de livres"""
        genres = {}
        for livre in self.biblio.livres:
            genres[livre.genre] = genres.get(livre.genre, 0) + 1
        
        fig, ax = plt.subplots(figsize=(5, 4))
        if genres:
            ax.pie(genres.values(), labels=genres.keys(), autopct='%1.1f%%')
            ax.set_title('Répartition par genre')
        else:
            ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')
        fig.tight_layout()
        return fig
    
    def generer_graphique_auteurs(self):
        """Génère un graphique des auteurs les plus populaires"""
        auteurs = {}
        for livre in self.biblio.livres:
            auteurs[livre.auteur] = auteurs.get(livre.auteur, 0) + 1
        
        fig, ax = plt.subplots(figsize=(5, 4))
        if auteurs:
            top_auteurs = sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:5]
            noms = [a[0] for a in top_auteurs]
            valeurs = [a[1] for a in top_auteurs]
            
            bars = ax.barh(noms[::-1], valeurs[::-1])  # Inversé pour avoir le plus grand en haut
            ax.bar_label(bars)
            ax.set_title('Top 5 auteurs')
        else:
            ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')
        fig.tight_layout()
        return fig
    
    def generer_graphique_emprunts(self):
        """Génère un graphique des emprunts par mois"""
        # Cette méthode nécessiterait des données de date dans votre système
        # Voici un exemple fictif
        mois = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun']
        emprunts = [12, 15, 9, 14, 18, 22]
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(mois, emprunts, marker='o')
        ax.set_title('Emprunts par mois')
        ax.set_ylabel('Nombre d\'emprunts')
        ax.grid(True)
        fig.tight_layout()
        return fig
    
    def actualiser_livres(self):
        """Met à jour la liste des livres"""
        self.tree_livres.delete(*self.tree_livres.get_children())
        for livre in sorted(self.biblio.livres, key=lambda x: x.titre):
            self.tree_livres.insert('', 'end', values=(
                livre.isbn,
                livre.titre,
                livre.auteur,
                livre.annee,
                livre.genre,
                livre.statut.value
            ))
    
    def actualiser_membres(self):
        """Met à jour la liste des membres"""
        self.tree_membres.delete(*self.tree_membres.get_children())
        for membre in sorted(self.biblio.membres, key=lambda x: x.nom):
            livres = ', '.join([livre.isbn for livre in membre.livreEmprunt])
            self.tree_membres.insert('', 'end', values=(
                membre.id,
                membre.nom,
                membre.email,
                livres if livres else "Aucun"
            ))
    
    def ajouter_livre(self):
        """Ajoute un nouveau livre à la bibliothèque"""
        try:
            isbn = self.entries_livre['isbn'].get().strip()
            titre = self.entries_livre['titre'].get().strip()
            auteur = self.entries_livre['auteur'].get().strip()
            annee = self.entries_livre['annee'].get().strip()
            genre = self.entries_livre['genre'].get().strip()
            
            # Validation
            if not all([isbn, titre, auteur, annee, genre]):
                raise ValueError("Tous les champs doivent être remplis")
            
            if not annee.isdigit():
                raise ValueError("L'année doit être un nombre")
            
            livre = Livre(isbn, titre, auteur, int(annee), genre)
            self.biblio.ajouterLivre(livre)
            
            self.actualiser_livres()
            for entry in self.entries_livre.values():
                entry.delete(0, tk.END)
            
            messagebox.showinfo("Succès", "Livre ajouté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout:\n{str(e)}")
    
    def supprimer_livre(self):
        """Supprime le livre sélectionné"""
        selected = self.tree_livres.selection()
        if not selected:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un livre")
            return
        
        isbn = self.tree_livres.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmation", f"Supprimer le livre {isbn}?"):
            try:
                livre_temp = Livre(isbn, "", "", 0, "")
                self.biblio.supprimerLivre(livre_temp)
                self.actualiser_livres()
                messagebox.showinfo("Succès", "Livre supprimé avec succès!")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la suppression:\n{str(e)}")
    
    def inscrire_membre(self):
        """Inscrit un nouveau membre"""
        try:
            id_membre = self.entries_membre['id'].get().strip()
            nom = self.entries_membre['nom'].get().strip()
            email = self.entries_membre['email'].get().strip()
            
            if not all([id_membre, nom]):
                raise ValueError("ID et Nom sont obligatoires")
            
            membre = Membre(id_membre, nom, email)
            self.biblio.inscrireMembre(membre)
            
            self.actualiser_membres()
            for entry in self.entries_membre.values():
                entry.delete(0, tk.END)
            
            messagebox.showinfo("Succès", "Membre inscrit avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'inscription:\n{str(e)}")
    
    def emprunter_livre(self):
        """Gère l'emprunt d'un livre"""
        try:
            id_membre = self.entry_emprunt_id.get().strip()
            isbn_livre = self.entry_emprunt_isbn.get().strip()
            
            if not id_membre or not isbn_livre:
                raise ValueError("ID Membre et ISBN Livre sont obligatoires")
            
            membre_temp = Membre(id_membre, "")
            livre_temp = Livre(isbn_livre, "", "", 0, "")
            
            self.biblio.emprunterLivre(membre_temp, livre_temp)
            
            self.entry_emprunt_id.delete(0, tk.END)
            self.entry_emprunt_isbn.delete(0, tk.END)
            
            self.actualiser_livres()
            self.actualiser_membres()
            
            messagebox.showinfo("Succès", "Livre emprunté avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'emprunt:\n{str(e)}")
    
    def rendre_livre(self):
        """Gère le retour d'un livre"""
        try:
            id_membre = self.entry_retour_id.get().strip()
            isbn_livre = self.entry_retour_isbn.get().strip()
            
            if not id_membre or not isbn_livre:
                raise ValueError("ID Membre et ISBN Livre sont obligatoires")
            
            membre_temp = Membre(id_membre, "")
            livre_temp = Livre(isbn_livre, "", "", 0, "")
            
            self.biblio.rendreLivre(membre_temp, livre_temp)
            
            self.entry_retour_id.delete(0, tk.END)
            self.entry_retour_isbn.delete(0, tk.END)
            
            self.actualiser_livres()
            self.actualiser_membres()
            
            messagebox.showinfo("Succès", "Livre rendu avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du retour:\n{str(e)}")
    
    def sauvegarder(self):
        """Sauvegarde les données de la bibliothèque"""
        try:
            self.biblio.sauvegarderData()
            messagebox.showinfo("Succès", "Données sauvegardées avec succès!")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliothequeApp(root)
    root.mainloop()