import random
import numpy as np

class Troncon():
    def __init__(self, categorie: str, pos_i: tuple, pos_f: tuple, id: int, pitstop: float = None) -> None:
        self._categorie = categorie
        self._pos_i = pos_i
        self._pos_f = pos_f
        self._id = id
        self._pitstop = pitstop
        self._pilotes = []
        self._commissaire = None
        self._alpha = self.get_angle()

    def get_pilotes(self) -> list:
        return self._pilotes
    
    def add_pilote(self, pilote) -> None:
        self._pilotes.append(pilote)

    def remove_pilote(self, pilote) -> None:
        self._pilotes.remove(pilote)

    def get_commissaire(self) -> object:
        return self._commissaire
    
    def set_commissaire(self, commissaire) -> None:
        self._commissaire = commissaire

    def get_pos_f(self) -> tuple:
        return self._pos_f
    
    def get_pos_i(self) -> tuple:
        return self._pos_i

    def get_angle(self) -> float:
        if self._pos_f[0] - self._pos_i[0] == 0:
            return 0
        else:
            return np.arctan((self._pos_f[1] - self._pos_i[1])/(self._pos_f[0] - self._pos_i[0]))

    commissaire = property(get_commissaire, set_commissaire)
    pilotes = property(get_pilotes, add_pilote)

    def update(self, delta_time: float) -> None:
        for pilote in self._pilotes:
            delta_perf = pilote.get_perf(self._id)
            speed = pilote.get_speed(self._categorie)
            pos_x = pilote.position[0] + (1 + delta_perf) * speed * delta_time * np.cos(self._alpha)
            pos_y = pilote.position[1] + (1 + delta_perf) * speed * delta_time * np.sin(self._alpha)

        
                
                
                

