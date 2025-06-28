import tkinter as tk
from tkinter import ttk, messagebox
from bibliotheque import Bibliotheque, Livre, Membre,statutLivre
from exceptions import LivreInexistantError

import matplotlib.pyplot as plt
from style import configureStyles 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class BibliothequeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion de Bibliothèque")
        self.root.geometry("1200x800")
        self.style = configureStyles(root)
        
        self.biblio = Bibliotheque()
        try:
            self.biblio.ChargerData()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur de chargement: {e}")
        
        self.CreateWidgets()
    
    def SetupStyle(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'), padding=[10, 5])
        style.configure('TButton', font=('Helvetica', 9), padding=5)
        style.configure('TLabel', font=('Helvetica', 9))
        style.configure('TEntry', font=('Helvetica', 9))
        style.configure('Treeview', rowheight=25, font=('Helvetica', 9))
        style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
    
    def CreateWidgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.CreateLivresTab()
        self.CreateMembresTab()
        self.CreateEmpruntsTab()
        self.CreateStatsTab()
        
        ttk.Button(
            self.root, 
            text="Sauvegarder les données", 
            command=self.Sauvegarder,
            style='TButton'
        ).pack(pady=10)
    
    def CreateLivresTab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Livres')   
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1) 
        formFrame = ttk.LabelFrame(tab, text="Ajouter un livre", padding=10)
        formFrame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        formFrame.grid_columnconfigure(1, weight=1) 
        fields = ['isbn', 'titre', 'auteur', 'annee', 'genre']
        self.entriesLivre = {}
        for i, field in enumerate(fields):
           ttk.Label(formFrame, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky='e', padx=5, pady=2)
           entry = ttk.Entry(formFrame)
           entry.grid(row=i, column=1, sticky='we', padx=5, pady=2)
           self.entriesLivre[field] = entry
        btnFrame = ttk.Frame(formFrame)
        btnFrame.grid(row=len(fields), column=0, columnspan=2, pady=5)
        ttk.Button(btnFrame, text="Ajouter", command=self.AjouterLivre).pack(side='left', padx=5)
        ttk.Button(btnFrame, text="Supprimer", command=self.SupprimerLivre).pack(side='right', padx=5)
        treeFrame = ttk.Frame(tab)
        treeFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        treeFrame.grid_columnconfigure(0, weight=1)
        treeFrame.grid_rowconfigure(0, weight=1)
        columns = ('isbn', 'titre', 'auteur', 'annee', 'genre', 'statut')
        self.treeLivres = ttk.Treeview(treeFrame, columns=columns, show='headings')
        colWidths = [120, 250, 150, 80, 120, 100]
        for col, width in zip(columns, colWidths):
           self.treeLivres.heading(col, text=col.capitalize())
           self.treeLivres.column(col, width=width, anchor='center')
        scrollbar = ttk.Scrollbar(treeFrame, orient='vertical', command=self.treeLivres.yview)
        self.treeLivres.configure(yscrollcommand=scrollbar.set)
        self.treeLivres.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
       
        self.ActualiserLivres()
    def CreateMembresTab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Membres')
    
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)
        formFrame = ttk.LabelFrame(tab, text="Inscrire un membre", padding=10)
        formFrame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        formFrame.grid_columnconfigure(1, weight=1)
        fields = ['id', 'nom']
        self.entriesMembre = {}

        for i, field in enumerate(fields):
            ttk.Label(formFrame, text=f"{field.capitalize()}:").grid(row=i, column=0, sticky='e', padx=5, pady=2)
            entry = ttk.Entry(formFrame)
            entry.grid(row=i, column=1, sticky='we', padx=5, pady=2)
            self.entriesMembre[field] = entry
    
        ttk.Button(formFrame, text="Inscrire", command=self.InscrireMembre)\
            .grid(row=len(fields), column=0, columnspan=2, pady=5)
    
   
        treeFrame = ttk.Frame(tab)
        treeFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        treeFrame.grid_columnconfigure(0, weight=1)
        treeFrame.grid_rowconfigure(0, weight=1)
    
        columns = ('id', 'nom', 'livresEmpruntes')
        self.treeMembres = ttk.Treeview(treeFrame, columns=columns, show='headings')
    
        colWidths = [100, 200, 300]
        for col, width in zip(columns, colWidths):
            self.treeMembres.heading(col, text=col.replace('_', ' ').title())
            self.treeMembres.column(col, width=width, anchor='w')
    
        scrollbar = ttk.Scrollbar(treeFrame, orient='vertical', command=self.treeMembres.yview)
        self.treeMembres.configure(yscrollcommand=scrollbar.set)
    
        self.treeMembres.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
    
        self.ActualiserMembres()
        
    
    def CreateEmpruntsTab(self):
       tab = ttk.Frame(self.notebook)
       self.notebook.add(tab, text='Emprunts')
       mainFrame = ttk.Frame(tab)
       mainFrame.pack(fill='both', expand=True, padx=10, pady=10)
       frameEmprunt = ttk.LabelFrame(mainFrame, text="Emprunter un livre", padding=10)
       frameEmprunt.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
       ttk.Label(frameEmprunt, text="ID Membre:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
       self.entryEmpruntId = ttk.Combobox(frameEmprunt, state='readonly')
       self.entryEmpruntId.grid(row=0, column=1, sticky='we', padx=5)
       ttk.Label(frameEmprunt, text="ISBN Livre:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
       self.entryEmpruntIsbn = ttk.Combobox(frameEmprunt, state='readonly')
       self.entryEmpruntIsbn.grid(row=1, column=1, sticky='we', padx=5)
       ttk.Button(frameEmprunt, text="Emprunter", command=self.EmprunterLivre).grid(
        row=2, column=1, pady=10, sticky='e')
       frameRetour = ttk.LabelFrame(mainFrame, text="Rendre un livre", padding=10)
       frameRetour.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
       ttk.Label(frameRetour, text="ID Membre:").grid(row=0, column=0, sticky='e')
       self.entryRetourId =  ttk.Combobox(frameRetour,state='readonly')
       self.entryRetourId.grid(row=0, column=1, sticky='we', padx=5, pady=5)
       self.entryRetourId.bind("<<ComboboxSelected>>", self.membreRetour)
       ttk.Label(frameRetour, text="ISBN Livre:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
       self.entryRetourIsbn = ttk.Combobox(frameRetour,state='readonly')
       self.entryRetourIsbn.grid(row=1, column=1, sticky='we', padx=5, pady=5)
       ttk.Button(frameRetour, text="Rendre", command=self.RendreLivre).grid(
          row=2, column=1, pady=10, sticky='e')
    
       self.remplir_comboboxes()
       mainFrame.columnconfigure(0, weight=1)
       mainFrame.columnconfigure(1, weight=1)
       mainFrame.rowconfigure(0, weight=1)

    def remplir_comboboxes(self):
      try:
       
        membres = [f"{m.id} - {m.nom}" for m in sorted(self.biblio.membres, key=lambda x: x.nom)]
        self.entryEmpruntId['values'] = membres
        livres_dispo = [f"{l.isbn} - {l.titre}" 
                      for l in sorted(self.biblio.livres, key=lambda x: x.titre)
                      if l.statut == statutLivre.disponible]
        self.entryEmpruntIsbn['values'] = livres_dispo
        membres_avec_emprunts = [f"{m.id} - {m.nom}" 
                               for m in sorted(self.biblio.membres, key=lambda x: x.nom)
                               if m.livreEmprunt]
        self.entryRetourId['values'] = membres_avec_emprunts
        self.entryEmpruntId.set('')
        self.entryEmpruntIsbn.set('')
        self.entryRetourId.set('')
        self.entryRetourIsbn.set('')
      except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du remplissage des listes :\n{str(e)}")
    def membreRetour(self, event):
      try:
        selected = self.entryRetourId.get()
        if not selected:
            return
        membre_id = selected.split(" - ")[0].strip()
        membre = self.biblio.chercherMembre(membre_id)
        livres_empruntes = [f"{l.isbn} - {l.titre}" for l in membre.livreEmprunt]
        self.entryRetourIsbn['values'] = livres_empruntes
        self.entryRetourIsbn.set('')
      except Exception as e:
        messagebox.showerror("Erreur", f"Erreur sélection membre:\n{str(e)}")    
    def CreateStatsTab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text='Statistiques')
        
        frameGraphiques = ttk.Frame(tab)
        frameGraphiques.pack(fill='both', expand=True, padx=10, pady=10)
        
        frameGenre = ttk.LabelFrame(frameGraphiques, text="Répartition par genre", padding=10)
        frameGenre.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        figGenre = self.GenererGraphiqueGenres()
        canvasGenre = FigureCanvasTkAgg(figGenre, master=frameGenre)
        canvasGenre.draw()
        canvasGenre.get_tk_widget().pack(fill='both', expand=True)
        
        frameAuteurs = ttk.LabelFrame(frameGraphiques, text="Top 5 auteurs", padding=10)
        frameAuteurs.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        figAuteurs = self.GenererGraphiqueAuteurs()
        canvasAuteurs = FigureCanvasTkAgg(figAuteurs, master=frameAuteurs)
        canvasAuteurs.draw()
        canvasAuteurs.get_tk_widget().pack(fill='both', expand=True)
        
        frameGraphiques.columnconfigure(0, weight=1)
        frameGraphiques.columnconfigure(1, weight=1)
        frameGraphiques.rowconfigure(0, weight=1)
    
    def GenererGraphiqueGenres(self):
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
    
    def GenererGraphiqueAuteurs(self):
        auteurs = {}
        for livre in self.biblio.livres:
            auteurs[livre.auteur] = auteurs.get(livre.auteur, 0) + 1
        
        fig, ax = plt.subplots(figsize=(5, 4))
        if auteurs:
            topAuteurs = sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:5]
            noms = [a[0] for a in topAuteurs]
            valeurs = [a[1] for a in topAuteurs]
            
            bars = ax.barh(noms[::-1], valeurs[::-1])
            ax.bar_label(bars)
            ax.set_title('Top 5 auteurs')
        else:
            ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')
        fig.tight_layout()
        return fig
    
    def ActualiserLivres(self):
        self.treeLivres.delete(*self.treeLivres.get_children())
        for livre in sorted(self.biblio.livres, key=lambda x: x.titre):
            self.treeLivres.insert('', 'end', values=(
                livre.isbn,
                livre.titre,
                livre.auteur,
                livre.annee,
                livre.genre,
                livre.statut.value
            ))
    
    def ActualiserMembres(self):
        self.treeMembres.delete(*self.treeMembres.get_children())
        for membre in sorted(self.biblio.membres, key=lambda x: x.nom):
            livres = ', '.join([livre.isbn for livre in membre.livreEmprunt])
            self.treeMembres.insert('', 'end', values=(
                membre.id,
                membre.nom,
                livres if livres else "Aucun"
            ))
    
    def AjouterLivre(self):
        try:
            isbn = self.entriesLivre['isbn'].get().strip()
            titre = self.entriesLivre['titre'].get().strip()
            auteur = self.entriesLivre['auteur'].get().strip()
            annee = self.entriesLivre['annee'].get().strip()
            genre = self.entriesLivre['genre'].get().strip()
            if not all([isbn, titre, auteur, annee, genre]):
                raise ValueError("Tous les champs doivent être remplis")
            
            if not annee.isdigit():
                raise ValueError("L'année doit être un nombre")
            
            livre = Livre(isbn, titre, auteur, int(annee), genre)
            self.biblio.ajouterLivre(livre)
            self.ActualiserLivres()
            for entry in self.entriesLivre.values():
                entry.delete(0, tk.END)
            self.remplir_comboboxes()
            if self.biblio.sauvegarderData():
                 messagebox.showinfo("Succès", "Livre ajouté et données sauvegardées avec succès!")
            else:
                  messagebox.showwarning("Avertissement", "Livre ajouté mais échec de la sauvegarde")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout:\n{str(e)}")
    def SupprimerLivre(self):
        selected = self.treeLivres.selection()
        if not selected:
             messagebox.showwarning("Avertissement", "Veuillez sélectionner un livre")
             return
        isbn = self.treeLivres.item(selected[0])['values'][0]
    
        try:
           livre = self.biblio.chercherLivre(Livre(isbn, "", "", 0, ""))
        
           if messagebox.askyesno("Confirmation", f"Supprimer le livre ISBN: {isbn}?"):
          
               self.biblio.supprimerLivre(isbn)
               self.ActualiserLivres()
               self.remplir_comboboxes()
               self.biblio.sauvegarderData()
               messagebox.showinfo("Succès", "Livre supprimé avec succès")      
        except Exception as e:
              messagebox.showerror("Erreur", f"Impossible de supprimer le livre: {str(e)}")
    def InscrireMembre(self):
        try:
            idMembre = self.entriesMembre['id'].get().strip()
            nom = self.entriesMembre['nom'].get().strip()
            if not all([idMembre, nom]):
                raise ValueError("ID et Nom sont obligatoires")
            membre = Membre(idMembre, nom)
            self.biblio.inscrireMembre(membre)
            self.ActualiserMembres()
            for entry in self.entriesMembre.values():
                entry.delete(0, tk.END)
            if self.biblio.sauvegarderData():
                messagebox.showinfo("Succès", "Membre inscrit avec succès!")
            else: 
                messagebox.showwarning("Avertissement", "Membre inscrit mais échec de la sauvegarde")   
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'inscription:\n{str(e)}")
    def EmprunterLivre(self):
      try:
        selection_membre = self.entryEmpruntId.get()
        selection_livre = self.entryEmpruntIsbn.get()
        if not selection_membre or not selection_livre:
            raise ValueError("Veuillez sélectionner un membre et un livre")
        membre_id = selection_membre.split(" - ")[0].strip()
        livre_isbn = selection_livre.split(" - ")[0].strip()
        membre_temp = Membre(membre_id, "")
        livre_temp = Livre(livre_isbn, "", "", 0, "")
        
        self.biblio.emprunterLivre(membre_temp, livre_temp)
        
        self.entryEmpruntId.set('')
        self.entryEmpruntIsbn.set('')
        self.ActualiserLivres()
        self.ActualiserMembres()
        self.remplir_comboboxes()  
        
        messagebox.showinfo("Succès", "Livre emprunté avec succès!")
      except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'emprunt:\n{str(e)}")
    def RendreLivre(self):
     try:
        selection_membre = self.entryRetourId.get()
        selection_livre = self.entryRetourIsbn.get()
        
        if not selection_membre or not selection_livre:
            raise ValueError("Veuillez sélectionner un membre et un livre")
        
        membre_id = selection_membre.split(" - ")[0].strip()
        livre_isbn = selection_livre.split(" - ")[0].strip()
        
        membreTemp = Membre(membre_id, "")  
        livreTemp = Livre(livre_isbn, "", "", 0, "")  
        
        self.biblio.rendreLivre(membreTemp, livreTemp)
        
        self.entryRetourId.set('')
        self.entryRetourIsbn.set('')
        self.ActualiserLivres()
        self.ActualiserMembres()
        self.remplir_comboboxes() 
        
        messagebox.showinfo("Succès", "Livre rendu avec succès!")
     except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du retour:\n{str(e)}")
    
    def Sauvegarder(self):
        try:
           if self.biblio.sauvegarderData():
               messagebox.showinfo("Succès", "Données sauvegardées avec succès!")
               self.ActualiserLivres()
               self.ActualiserMembres()
               self.remplir_comboboxes()
           else:
            messagebox.showerror("Erreur", "La sauvegarde a échoué")    
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{str(e)}")
   
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliothequeApp(root)
    root.mainloop()