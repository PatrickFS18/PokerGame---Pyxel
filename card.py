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
    

class Jogador:
    def __init__(self):
        self.mao = []
        
    def __str__(self):
        return (f'Suas cartas: {self.mao}')

baralho = Baralho()
baralho.gerarCartas()
baralho.embaralharCartas()

cartas = baralho.cartas

jogador = Jogador()
adversario = Jogador()

for i in range (0,4,2):
    jogador.mao.append(cartas[i])
    cartas.pop(i)
for i in range(0,2):
    adversario.mao.append(cartas[i])
    cartas.pop(i)
for i in jogador.mao:
    print(i)
for i in adversario.mao:
    print(i)

