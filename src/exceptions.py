
class LivreIndisponible(Exception):
    def __init__(self,message="le Livre n'est pas disponible"):
        super().__init__(message)
class QuotaEmpruntDepasseError(Exception):
    def __init__(self,message="Vous avez dépassé votre quota d'emprunts"):
        super().__init__(message)    
class MembreInexistantError(Exception):
    def __init__(self,message="Ce membre  n'existe pas"):
        super().__init__(message)   
class LivreInexistantError(Exception):
    def __init__(self,message="Ce livre n'existe pas"):
        super().__init__(message)
