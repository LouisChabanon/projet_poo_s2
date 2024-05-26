import xml.etree.ElementTree as ET
import numpy as np
import ast

from models.acteur import DC, Pilote, Commissaire
from models.troncon import Troncon
from models.voiture import Voiture


class Circuit:
    def __init__(
        self,
        troncons: list,
        nbr_tours: int,
        delta_overtake: dict,
        temps_immobilisation: float,
    ):
        self._troncons = troncons
        self._nbr_tours = int(nbr_tours)
        self._delta_overtake = ast.literal_eval(delta_overtake)
        self._temps_immobilisation = float(temps_immobilisation)
        self._directeur = None
        self._classement = []

    def get_delta_overtake(self, categorie) -> dict:
        return self._delta_overtake[categorie]

    def begin_race(self, voitures, directeur) -> None:
        """
        Commence la course, les pilotes rentre dans leur voiture et
        """
        if isinstance(directeur, DC):
            self._directeur = directeur

        if not self.is_valid():
            raise ValueError("Le circuit n'est pas valide")

        for troncon in self._troncons:
            for pilote in troncon.pilotes:
                self._classement.append(pilote)
                for voiture in voitures:
                    if pilote.get_nom_voiture() == voiture.get_nom():
                        pilote.set_voiture(voiture)
                rang = pilote.get_rang()
                # On place les pilotes sur la grille de départ
                pilote.set_pos(np.array(troncon.get_pos_f()) - 0.06 * troncon.direction/troncon.length)
        # On trie les pilotes par rang
        self._classement.sort(
            key=lambda x: x.get_rang()
        )  
        self.run()

    def get_next_troncon(self, id: int) -> Troncon:
        """
        Renvoie le troncon suivant
        """
        if id == len(self._troncons) - 1:
            return self._troncons[0]
        return self._troncons[id + 1]

    def is_last_lap(self) -> bool:
        if self._classement[0].tour == self._nbr_tours:
            return True
        return False

    def is_valid(self) -> bool:
        """
        Vérifie que les troncons se suivent et forment un circuit
        """
        for i in range(len(self._troncons) - 1):
            if (
                self._troncons[i].get_pos_f()[0] != self._troncons[i + 1].get_pos_i()[0]
                or self._troncons[-1].get_pos_f()[0] != self._troncons[0].get_pos_i()[0]
            ):
                return False
            if (
                self._troncons[i].get_pos_f()[1] != self._troncons[i + 1].get_pos_i()[1]
                or self._troncons[-1].get_pos_f()[1] != self._troncons[1].get_pos_i()[1]
            ):
                return False

        return True

    def run(self, delta_time: float = 0.01) -> None:
        time = 0
        while not self.is_last_lap():
            time = time + delta_time
            for troncon in self._troncons:
                troncon.update(self, delta_time)
                # print(str(troncon._id) + " has " + str(troncon.get_pilotes()))
        return None


def load_data(config: str = "./config.xml") -> tuple:
    tree = ET.parse(config)
    root = tree.getroot()

    directeur = None
    voitures = []
    for i in root:
        if i.tag == "Circuit":
            troncons = []
            for j in i:
                if j.tag == "Troncon":
                    troncons.append(
                        Troncon(
                            j.attrib["type"],
                            j.attrib["pos_i"],
                            j.attrib["pos_f"],
                            int(j.attrib["idx"]),
                        )
                    )
                    for k in j:
                        if k.tag == "Commissaire":
                            troncons[-1].commissaire = Commissaire(
                                str(k.attrib["nom"]), str(k.attrib["prenom"])
                            )
                        elif k.tag == "Pilote":
                            troncons[-1].pilotes = Pilote(
                                str(k.attrib["nom"]),
                                str(k.attrib["prenom"]),
                                str(k.attrib["voiture"]),
                                int(k.attrib["numero"]),
                                int(k.attrib["rang"]),
                                float(k.attrib["d1"]),
                                float(k.attrib["d2"]),
                                float(k.attrib["h_overtake"]),
                                float(k.attrib["h_crash"]),
                            )
            circuit = Circuit(
                troncons,
                i.attrib["nombre_tour"],
                i.attrib["delta_overtake"],
                i.attrib["temps_immobilisation"],
            )
        elif i.tag == "Voiture":
            voitures.append(
                Voiture(
                    i.attrib["type"],
                    i.attrib["vitesse"],
                    i.attrib["equipe"],
                    i.attrib["nom"],
                    int(i.attrib["f1"]),
                    int(i.attrib["f2"]),
                )
            )

    return circuit, voitures, directeur


def main(config: str = "./config.xml"):
    """
    Fonction principale
    """
    circuit, voitures, directeur = load_data(config)

    circuit.begin_race(voitures, directeur)


if __name__ == "__main__":
    main()
