import random 

class Carta:
    def __init__(self,dictCard):
        self.valor = dictCard['value']
        self.naipe = dictCard['naipe']

    def __str__(self):
        return f"{self.valor} de {self.naipe}"

class Baralho:
    def __init__(self):
        self.cartas = []

    def gerarCartas(self):
        for i in range(1, 14):  # 1 a 13 (de Ás a Rei)
            self.cartas.append(Carta({'value':i, 'naipe': 'Paus'}))
            self.cartas.append(Carta({'value':i, 'naipe': 'Ouro'}))
            self.cartas.append(Carta({'value':i, 'naipe':'Espada'}))
            self.cartas.append(Carta({'value':i, 'naipe':'Copas'}))
            
    
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
for i in cartas:
    print(i)

jogador = Jogador()
adversario = Jogador()
dealer = Jogador()
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
 for i in range (0,5):
     dealer.mao.append(cartas[i])
 for i in dealer.mao:
     print(i)
