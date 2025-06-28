from exceptions import LivreInexistantError
from exceptions import LivreIndisponible
from exceptions import MembreInexistantError
from exceptions import QuotaEmpruntDepasseError
from datetime import datetime
import os
import csv
from enum import Enum 
class statutLivre(Enum):
     disponible ="disponible"
     emprunte = "emprunte"
class Livre:
    def __init__(self,isbn,titre,auteur,annee,genre,statut=statutLivre.disponible):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.statut = statut
    def changerStatut( self,stat):
        if not isinstance(stat,statutLivre):
            raise ValueError("Statut invalide")
        self.statut = stat
    def emprunter(self):
        if self.statut == statutLivre.emprunte:
            raise LivreIndisponible()
        self.statut = statutLivre.emprunte    
    def rendre(self):
        if self.statut==statutLivre.disponible:
            raise ValueError("Le livre est deja disponible.")
        self.statut = statutLivre.disponible          
class Membre:
    def __init__(self,id,nom):
      self.id=id
      self.nom=nom
      self.livreEmprunt=[]
class Bibliotheque:
    def __init__(self):
        self.livres=[]
        self.membres=[]
        self.historique=[]
       
    def chercherLivre(self, isbn):
        isbn_recherche = str(isbn).strip()
        for livre in self.livres:
           if str(livre.isbn).strip() == isbn_recherche:
               return livre 
        raise LivreInexistantError()
  
    def chercherMembre(self,id):
        for membre in self.membres:
            if membre.id==id:
                return membre
        raise MembreInexistantError() 
            
    def ajouterLivre(self,livre):
        try:
            self.chercherLivre(livre.isbn)
            raise Exception(f"Le livre avec l'ISBN {livre.isbn} existe déjà.")
        except LivreInexistantError:
            self.livres.append(livre)
     
    def supprimerLivre(self, isbn):
       livre = self.chercherLivre(isbn)
       for membre in self.membres:
            if livre in membre.livreEmprunt:
                raise Exception("Le livre est actuellement emprunte")    
       self.livres.remove(livre)
       return True
      
    
    def emprunterLivre(self,membre,livre):
        membreTrouve = self.chercherMembre(membre.id) 
        livreTrouve = self.chercherLivre(livre.isbn) 

        if livreTrouve.statut != statutLivre.disponible:
            raise LivreIndisponible()

        if len(membreTrouve.livreEmprunt) >= 5:
             raise QuotaEmpruntDepasseError()
        livreTrouve.changerStatut(statutLivre.emprunte)
        membreTrouve.livreEmprunt.append(livreTrouve)
        self.historique.append({
            'date': datetime.now(),
            'isbn': livre.isbn,
            'id_membre': membre.id,
            'action': 'emprunt'
        })
    def getMembresList(self):
        membres = []
        for m in self.membres:
             membres.append((m.id, m.nom))
        return sorted(membres, key=lambda x: x[1])  
    def getLivresDisponiblesList(self):
        livres = []
        for l in self.livres:
           if l.statut == statutLivre.disponible:
              livres.append((l.isbn, f"{l.titre} (ISBN: {l.isbn})"))
        return sorted(livres, key=lambda x: x[1])  
           
    def rendreLivre(self,membre,livre):
        membreTrouve = self.chercherMembre(membre.id) 
        livreTrouve = self.chercherLivre(livre.isbn) 

        if livreTrouve.statut != statutLivre.emprunte:
            raise LivreIndisponible()
        if livreTrouve not in membreTrouve.livreEmprunt:
            raise Exception("Ce membre n'a pas emprunté ce livre")   
        livreTrouve.rendre()
        membreTrouve.livreEmprunt.remove(livreTrouve)
        self.historique.append({
            'date': datetime.now(),
            'isbn': livre.isbn,
            'id_membre': membre.id,
            'action': 'retour'
        })
    def inscrireMembre(self, membre):
       if any(m.id == membre.id for m in self.membres):
           raise Exception(f"Le membre avec l'ID {membre.id} existe déjà")
       self.membres.append(membre)
      

    def ChargerData(self):
        if os.path.exists('data/livres.txt'):
            with open ('data/livres.txt','r') as f:
                for line in f:
                   data = line.strip().split(';')
                   statut = statutLivre.disponible if data[5] == "disponible" else statutLivre.emprunte
                   livre = Livre(data[0], data[1], data[2], int(data[3]), data[4], statut)
                   self.livres.append(livre)
        if os.path.exists('data/membres.txt'):
            with open ('data/membres.txt','r',encoding='utf-8') as f:
                for line in f:
                    data =line.strip().split(';')
                    if len(data) >= 2: 
                       membre = Membre(data[0],data[1])
                       if len(data)>2 and data[2]:
                          for isbn in data[2].split(','):
                             try:
                                livre = self.chercherLivre(isbn)
                                if livre.statut == statutLivre.disponible:
                                    livre.changerStatut(statutLivre.emprunte)
                                membre.livreEmprunt.append(livre)
                             except LivreInexistantError:
                                 print(f"Livre {isbn} non trouvé pour {membre.nom}")
                       self.membres.append(membre)    
        if os.path.exists('data/historique.csv'):
           with open('data/historique.csv', 'r', encoding='utf-8') as f:
               reader = csv.DictReader(f, delimiter=';')
               for row in reader:
                 try:
                    date_emprunt = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                    self.historique.append({
                        'date': date_emprunt,
                        'isbn': row['isbn'],
                        'id_membre': row['id_membre'],
                        'action': row['action']
                    })     
                 except Exception as e:
                    print(f"Erreur lecture ligne historique: {str(e)}")                                  
    
    def sauvegarderData(self):
    
        with open('data/livres.txt', 'w') as f:
           for livre in self.livres:
            f.write(f"{livre.isbn};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.statut.value}\n")
     
        with open('data/membres.txt', 'w') as f:
           for membre in self.membres:
              livres = ",".join(l.isbn for l in membre.livreEmprunt)
              f.write(f"{membre.id};{membre.nom};{livres}\n")

        with open('data/historique.csv', 'w',encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['date', 'isbn', 'id_membre', 'action'])  
            for h in self.historique:
                writer.writerow([
                h['date'].strftime('%Y-%m-%d %H:%M:%S'), 
                h['isbn'],
                h['id_membre'],
                h['action']
            ])
        return True