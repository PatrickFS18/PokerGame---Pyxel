import random 
class Carta:
    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe

    def __str__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = []

    def gerarCartas(self):
        for i in range(1, 14):  # 1 a 13 (de Ás a Rei)
            self.cartas.append(Carta(i, 'Paus'))
            self.cartas.append(Carta(i, 'Ouro'))
            self.cartas.append(Carta(i, 'Espada'))
            self.cartas.append(Carta(i, 'Copas'))
            
    
    def embaralharCartas(self):
        random.shuffle(self.cartas) 
    
baralho = Baralho()
baralho.gerarCartas()
baralho.embaralharCartas()

for carta in baralho.cartas:
    print(carta)
