from exceptions import LivreInexistantError
from exceptions import LivreIndisponible
from exceptions import MembreInexistantError
from exceptions import QuotaEmpruntDepasseError
import os
import datetime
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
        
    def chercherLivre(self,isbn):
        for livre in self.livres:  
            if livre.isbn == isbn:
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
     
    def supprimerLivre(self,livre):
        livreTrouve = self.chercherLivre(livre.isbn)
        self.livres.remove(livreTrouve)
    
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
    
    def rendreLivre(self,membre,livre):
        membreTrouve = self.chercherMembre(membre.id) 
        livreTrouve = self.chercherLivre(livre.isbn) 

        if livreTrouve.statut != statutLivre.emprunte:
            raise LivreIndisponible("Le livre n'est pas emprunté")
        if livreTrouve not in membreTrouve.livreEmprunt:
            raise Exception("Ce membre n'a pas emprunté ce livre")   
        livreTrouve.rendre()
        membreTrouve.livreEmprunt.remove(livreTrouve)
        self.historique.append({
            'date': datetime.now(),
            'isbn': livre.isbn,
            'id_membre': membre.id,
            'action': 'emprunt'
        })
   
    def inscrireMembre(self, membre):
        try:
            self.chercherMembre(membre.id)
            raise Exception(f"le membre avec l'id{membre.id} existe deja .")
        except MembreInexistantError:
            self.membres.append(membre) 

    def chargerData(self):
        if os.path.exists('data/livres.txt'):
            with open ('data/livres.txt','r') as f:
                for line in f:
                   data = line.strip().split(';')
                   statut = statutLivre.disponible if data[5] == "disponible" else statutLivre.emprunte
                   livre = Livre(data[0], data[1], data[2], int(data[3]), data[4], statut)
                   self.livres.append(livre)
        if os.path.exists('data/membres.txt'):
            with open ('data/membres.txt','r') as f:
                for line in f:
                    data =line.strip().split(';')
                    membre = Membre(data[0],data[1])
                    if len(data)>2 and data[2]:
                        for isbn in data[2].split(','):
                            try:
                                livre = self.chercherLivre(isbn)
                                membre.livreEmprunt.append(livre)
                            except LivreInexistantError:
                                pass
                    self.membres.append(membre)                        

    def sauvegarderData(self):
        with open('data/livres.txt','w') as f:
            for livre in self.livres:
               f.write(f"{livre.isbn};{livre.titre};{livre.auteur};{livre.annee};{livre.genre};{livre.statut.value}\n")
        with open('data/membres.txt','w')as f:
            for membre in self.membres:
                f.write(f"{membre.id};{membre.nom};{membre.livreEmprunt}\n")
        with open('data/historique.csv','w') as f:
            f.write("date;isbn;id_membre;action\n")
            for transaction in self.historique:
                dateStr= transaction['date'].strtime("%Y-%m-%d %H:%M:%S")        
                f.write(f"{dateStr};{transaction['isbn']};{transaction['id_membre']};{transaction['action']}\n")