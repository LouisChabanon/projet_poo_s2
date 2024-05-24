import xml.etree.ElementTree as ET

class Circuit():
    def __init__(self, troncon: list, voitures: list, pilotes: list, directeur: Directeur):
        self.troncon = troncon
        self.voitures = voitures
        self.pilotes = pilotes
        self.directeur = directeur

    def run(self):
        pass



def load_data(config: str = "./config.xml") -> :
    tree = ET.parse(config)
    root = tree.getroot()

    troncon = []
    for i in root:
        if i.tag == "troncon":
            troncon.append(i)

def main():
    pass

