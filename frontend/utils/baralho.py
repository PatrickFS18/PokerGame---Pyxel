import random
from utils.carta import Carta

class Baralho:
    def __init__(self):
        self.cartas = []

    def gerarCartas(self):
        for i in range(2, 15):  # 2 a 14 (de 2 a Rei, e Ás como 14)
            if len(self.cartas) < 53:
                self.cartas.append(Carta({'valor':i, 'naipe': 'Paus'}))
                self.cartas.append(Carta({'valor':i, 'naipe': 'Ouro'}))
                self.cartas.append(Carta({'valor':i, 'naipe':'Espada'}))
                self.cartas.append(Carta({'valor':i, 'naipe':'Copas'}))
            
    
    def embaralharCartas(self):
        random.shuffle(self.cartas) 
