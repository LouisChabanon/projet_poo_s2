import random
import ast
import numpy as np


class Troncon:
    def __init__(
        self, categorie: str, pos_i: tuple, pos_f: tuple, id: int, pitstop: float = None
    ) -> None:
        self._categorie = categorie
        self._pos_i = ast.literal_eval(pos_i)
        self._pos_f = ast.literal_eval(pos_f)
        self._id = id
        self._pitstop = pitstop
        self._pilotes = []
        self._commissaire = None
        self._alpha = 0
        self._direction = np.array(self._pos_f) - np.array(self._pos_i)
        self._length = np.linalg.norm(self._direction)

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
    
    direction = property(lambda self: self._direction)
    length = property(lambda self: self._length)
    commissaire = property(get_commissaire, set_commissaire)
    pilotes = property(get_pilotes, add_pilote)

    def update(self, circuit, delta_time: float) -> None:
        for pilote in self._pilotes:
            if pilote.get_tour() > circuit.get_nbr_tours():
                continue
            self.update_pilot_position(circuit, pilote, delta_time)
        
        if not self._commissaire.drapeau_bleu:
            self.depassement(circuit)


    def update_pilot_position(self, circuit, pilote, delta_time: float) -> None:
        """
        Met à jour la position du pilote sur le tronçon
        """   
        delta_perf = pilote.get_perf(self._id)
        speed = pilote.get_speed(self._categorie)
        distance_to_travel = (1 + delta_perf) * speed * delta_time

        distance_to_end = np.linalg.norm(np.array(pilote.position) - np.array(self._pos_f))
            

        delta = distance_to_travel - distance_to_end
        direction_unit = self._direction / self._length
        # Si on dépasse la fin du tronçon
        if delta > 0:
            self.remove_pilote(pilote)
            next_troncon = circuit.get_next_troncon(self._id)
            next_troncon.add_pilote(pilote)
            pilote.position = tuple(np.array(next_troncon.get_pos_i()) + delta * (next_troncon.direction / next_troncon.length))

            if next_troncon._id == 0:
                pilote.set_tour(pilote.get_tour() + 1)
                print(str(pilote) + " a commencer un nouveau tour (" + str(pilote.get_tour()) + " / " + str(circuit.get_nbr_tours()) + ")")

        else:
            pilote.position = tuple(np.array(pilote.position) + distance_to_travel * direction_unit)

    def depassement(self, circuit) -> None:
        """
        Gère les dépassements entre pilotes sur le tronçon
        """
        if len(self._pilotes) < 2:
            return None
            
        self._pilotes.sort(key=lambda x: x.rang)
    
        for i in range(1, len(self._pilotes)-1):
            pilote_i, pilote_i1 = self._pilotes[i-1], self._pilotes[i]
            
            time_diff = np.linalg.norm(np.array(pilote_i1.position) - np.array(pilote_i.position))**2 / pilote_i1.get_speed(self._categorie)
            
            if time_diff < circuit.get_delta_overtake(self._categorie) and pilote_i1.get_overtake_perf() < random.uniform(0, 1):

                # Gestion des accidents
                if pilote_i.get_crash_chance() < random.uniform(0, 1):
                    print(str(pilote_i) + " a eu un accident")
                    circuit.handle_crash(pilote_i, self)
                    if len(self._pilotes) < 2:
                        return None
                    continue

                if pilote_i1.get_crash_chance() < random.uniform(0, 1):
                    print(str(pilote_i1) + " a eu un accident")
                    circuit.handle_crash(pilote_i1, self)
                    if len(self._pilotes) < 2:
                        return None
                    continue

                print(str(pilote_i1) + " a dépassé " + str(pilote_i))
                pilote_i.rang, pilote_i1.rang = pilote_i1.rang, pilote_i.rang