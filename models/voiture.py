import ast


class Voiture:
    def __init__(
        self, car_type: str, vitesse: dict, equipe: str, nom, f1: int, f2: int
    ) -> None:
        self._car_type = car_type
        self._vitesse = ast.literal_eval(vitesse)
        self._equipe = str(equipe)
        self._nom = str(nom)
        self._f1 = int(f1)
        self._f2 = int(f2)
        self._pilote = None

    def get_nom(self) -> str:
        return self._nom

    def get_speed(self, categorie: str) -> float:
        return self._vitesse[categorie] / 3600
