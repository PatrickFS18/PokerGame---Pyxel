import pyxel
from jogador import Jogador
from baralho import Baralho
from collections import Counter

class Poker:
    def __init__(self):
        self.jogador = Jogador()
        self.adversario = Jogador()
        self.dealer = Jogador()
        self.baralho = Baralho()
        self.is_initialized = False
        self.verify = True
        
        pyxel.init(160,120)
        pyxel.run(self.update,self.draw)
        
    def initializedGame(self):
        if(self.is_initialized == False):
            # Instância de Initialização dos jogadores e Mesa e embaralhamento de cartas
            
            self.baralho.gerarCartas()
            self.baralho.embaralharCartas()
            cartas = self.baralho.cartas
            
            # Distribuição de cartas 
            for i in range (0,4,2):
                self.jogador.mao.append(cartas[i])
                cartas.pop(0)
                
            for i in range(0,2):
                self.adversario.mao.append(cartas[i])
                cartas.pop(0)
                
            for i in range (0,5):
                self.dealer.mao.append(cartas[i])
                cartas.pop(0)
            self.is_initialized = True
    
    def orderByValueAndNaipe(self,cards):
        
        # Ordem dos naipes (Paus, Ouro, Espada, Copas)
        order_naipes = {'Paus': 0, 'Ouro': 1, 'Espada': 2, 'Copas': 3}
        
        # Ordena a mão,  primeiro pelo naipe e depois pelo valor

        cards = cards.sort(key = lambda carta: (order_naipes[carta.naipe], carta.valor))
        return cards
    
    def countEqualValues(self,cards):
        valores = [card.valor for card in cards]  # Criando uma lista dos valores das cartas
        valores.sort()
        contagem = Counter(valores)  # Conta quantas vezes cada valor aparece
        print(valores,'valores')
        resultado = {
            'Pares': {valor: count for valor, count in contagem.items() if count == 2},
            'Triplas': {valor: count for valor, count in contagem.items() if count == 3},
            'Quadruplas': {valor: count for valor, count in contagem.items() if count == 4}
        }
        
        for i in resultado['Pares']:
            print(i)
        for i in resultado['Triplas']:
            print(i)
        for i in resultado['Quadruplas']:
            print(i)
        
        
    def verifyLogic(self, dealer, jogador):
        
        mao = []
        
        for i in range(len(dealer.mao)):
            mao.append(dealer.mao[i])
        for i in range(len(jogador.mao)):
            mao.append(jogador.mao[i])
        
        self.orderByValueAndNaipe(mao)
        self.countEqualValues(mao)
        
        
        self.verify = False
        
    def update(self):
        self.initializedGame()
        if(self.verify):
            self.verifyLogic(self.dealer,self.jogador)
        pass

    def draw(self):
        pyxel.cls(1)
        

Poker()