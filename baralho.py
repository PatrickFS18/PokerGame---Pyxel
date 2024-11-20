import random
from carta import Carta

class Baralho:
    def __init__(self):
        self.cartas = []

    def gerarCartas(self):
        for i in range(1, 14):  # 1 a 13 (de Ás a Rei)
            if len(self.cartas) < 53:
                self.cartas.append(Carta({'value':i, 'naipe': 'Paus'}))
                self.cartas.append(Carta({'value':i, 'naipe': 'Ouro'}))
                self.cartas.append(Carta({'value':i, 'naipe':'Espada'}))
                self.cartas.append(Carta({'value':i, 'naipe':'Copas'}))
            
    
    def embaralharCartas(self):
        random.shuffle(self.cartas) 
