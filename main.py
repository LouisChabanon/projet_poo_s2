import xml.etree.ElementTree as ET
from models.acteur import DC, Pilote, Commissaire
from models.troncon import Troncon
from models.voiture import Voiture
class Circuit():
    def __init__(self, troncons: list, nbr_tours: int, delta_overtake: dict, temps_immobilisation: float):
        self._troncons = troncons
        self._nbr_tours = int(nbr_tours)
        self._delta_overtake = delta_overtake
        self._temps_immobilisation = float(temps_immobilisation)
        self._directeur = None

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
                for voiture in voitures:
                    if pilote.get_nom_voiture() == voiture.get_nom():
                        pilote.set_voiture(voiture)            
                rang = pilote.get_rang()
                # On place les pilotes sur la grille de départ
                pilote.set_pos((troncon.get_pos_f()[0] - 6*(rang-1), troncon.get_pos_f()[1] - 6*(rang-1)))

        self.run()



    def is_last_lap(self) -> bool:
        if self._classement[0].get_tour() == self._nbr_tours:
            return True
        return False

    def is_valid(self) -> bool:
        """
        Vérifie que les troncons se suivent et forment un circuit
        """
        for i in range(len(self._troncons)-1):
            if self._troncons[i].get_pos()[1] != self._troncons[i+1].get_pos()[0] or self._troncons[-1].get_pos()[1] != self._troncons[0].get_pos()[0]:
                return False
        return True

    def run(self, delta_time: float = 0.01) -> None:
        time = 0
        while not self.is_last_lap() and self._classement[-1].pos[1]:
            time = time + delta_time
            for troncon in self._troncons:
                troncon.update(time)
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
                    troncons.append(Troncon(j.attrib["type"], j.attrib["pos_i"], j.attrib["pos_f"], j.attrib["idx"]))
                    for k in j:
                        if k.tag == "Commissaire":
                            troncons[-1].commissaire = Commissaire(k.attrib["nom"], k.attrib["prenom"])
                        elif k.tag == "Pilote":
                            troncons[-1].pilotes = Pilote(k.attrib["nom"], k.attrib["prenom"], k.attrib["voiture"], k.attrib["numero"], k.attrib["rang"], k.attrib["d1"], k.attrib["d2"], k.attrib["h_overtake"], k.attrib["h_crash"])
            circuit = Circuit(troncons, i.attrib["nombre_tour"], i.attrib["delta_overtake"], i.attrib["temps_immobilisation"])
        elif i.tag == "Voiture":
            voitures.append(Voiture(i.attrib["type"], i.attrib["vitesse"], i.attrib["equipe"], i.attrib["nom"], i.attrib["f1"], i.attrib["f2"]))


    

    return circuit, voitures, directeur


def main(config: str = "./config.xml"):
    """
    Fonction principale
    """
    circuit, voitures, directeur = load_data(config)

    circuit.begin_race(voitures, directeur)

if __name__ == "__main__":
    main()