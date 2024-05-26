from models.troncon import Troncon
from models.voiture import Voiture
import random


class Acteur:
    def __init__(self, nom: str, prenom: int) -> None:
        self._nom = str(nom)
        self._prenom = str(prenom)

    def __str__(self) -> str:
        return f"{self._nom} {self._prenom}"

    def __repr__(self) -> str:
        return f"{self._nom} {self._prenom}"

    def get_prenom(self) -> str:
        return self._prenom

    def get_nom(self) -> str:
        return self._nom


class Pilote(Acteur):
    def __init__(
        self,
        nom: str,
        prenom: str,
        voiture: str,
        numero: int,
        rang: int,
        d1: float,
        d2: float,
        h_overtake: float,
        h_crash: float,
        pos: list = [None, None],
    ) -> None:
        super().__init__(nom, prenom)
        self._voiture = None
        self._nom_voiture = str(voiture)
        self._numero = numero
        self._rang = int(rang)
        self._d1 = float(d1)
        self._d2 = float(d2)
        self._h_overtake = float(h_overtake)
        self._h_crash = float(h_crash)
        self._pos = pos
        self._perf = 0
        self._troncon_id = None
        self._tour = 0

    def __str__(self) -> str:
        return f"{self._nom} {self._prenom}"

    def get_nom_voiture(self):
        return self._nom_voiture

    def get_voiture(self) -> Voiture:
        return self._voiture

    def set_voiture(self, voiture: Voiture) -> None:
        self._voiture = voiture

    def get_pos(self) -> list:
        return self._pos

    def set_pos(self, pos: list) -> None:
        self._pos = pos

    def get_rang(self) -> int:
        return self._rang
    
    def set_rang(self, rang: int) -> None:
        self._rang = int(rang)

    def get_tour(self) -> int:
        return self._tour

    def set_tour(self, tour: int) -> None:
        self._tour = tour

    def get_overtake_perf(self) -> float:
        return self._h_overtake
    
    def get_crash_chance(self) -> float:
        return self._h_crash

    voiture = property(get_voiture, set_voiture)
    position = property(get_pos, set_pos)
    tour = property(get_tour, set_tour)
    rang = property(get_rang, set_rang)

    def get_perf(self, troncon) -> float:
        if troncon != self._troncon_id:
            self._troncon_id = troncon
            self._perf = random.uniform(self._d1, self._d2)
            return self._perf
        else:
            return self._perf

    def get_speed(self, categorie: str) -> float:
        return self._voiture.get_speed(categorie)


class DC(Acteur):
    def __init__(self, nom: str, prenom: str, h_sc: float, t1: int, t2: int) -> None:
        super().__init__(nom, prenom)
        self._h_sc = float(h_sc)
        self._t1 = int(t1)
        self._t2 = int(t2)


class Commissaire(Acteur):
    def __init__(self, nom: str, prenom: str) -> None:
        super().__init__(nom, prenom)
        self._drapeau_bleu = False
        self._drapeau_jaune = False
        self._drapeau_damier = False

        def __str__(self) -> str:
            return f"{self._nom} {self._prenom}"

        def get_drapeau_bleu(self) -> bool:
            return self._drapeau_bleu
        
        def set_drapeau_bleu(self, drapeau: bool) -> None:
            self._drapeau_bleu = drapeau

        def get_drapeau_jaune(self) -> bool:
            return self._drapeau_jaune
        
        def set_drapeau_jaune(self, drapeau: bool) -> None:
            self._drapeau_jaune = drapeau

        def get_drapeau_damier(self) -> bool:
            return self._drapeau_damier
        
        def set_drapeau_damier(self, drapeau: bool) -> None:
            self._drapeau_damier = drapeau

        drapeau_bleu = property(get_drapeau_bleu, set_drapeau_bleu)
        drapeau_jaune = property(get_drapeau_jaune, set_drapeau_jaune)
        drapeau_damier = property(get_drapeau_damier, set_drapeau_damier)
