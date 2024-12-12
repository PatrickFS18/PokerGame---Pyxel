import pyxel
from jogador import Jogador
from baralho import Baralho
from collections import Counter
from compare import Compare

class Poker:
    def __init__(self):
        self.jogador = Jogador()
        self.adversario = Jogador()
        self.dealer = Jogador()
        self.baralho = Baralho()
        self.is_initialized = False
        self.verify = True
        self.compare_1_1 = None
        self.compare_1_2 = None
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
        
    def verifyLogic(self, dealer, jogador):
        print('JOGADOR 1!!!')
        self.compare_1 = Compare(self.jogador.mao, self.dealer.mao)
        self.compare_1.game()
        self.compare_1.countEqualValues()
        print('victory',self.compare_1.victory)
        
        print('JOGADOR 2!!!')
        
        self.compare_2 = Compare(self.adversario.mao, self.dealer.mao)
        self.compare_2.game()
        self.compare_2.countEqualValues()
        
        print('victory',self.compare_2.victory)
        print('as maos do cara 1: ',self.compare_1.highest_hand_value)

        player_1_victory = max(self.compare_1.victory)
        player_2_victory = max(self.compare_2.victory)
        
        print('Valor vitoria jogador 1: ',player_1_victory)
        print('Valor vitoria jogador 2: ',player_2_victory)
        print('as maos do cara 2: ',self.compare_2.highest_hand_value)

        if(player_1_victory == player_2_victory):
            print('Possível empate. verificar qual carta maior')
            pass
        elif(player_1_victory > player_2_victory):
            print('player 1 venceu. ')
        else:
            print('player 2 venceu')
        #self.orderByValueAndNaipe(mao)
        #self.countEqualValues(mao)
        
        
        self.verify = False

    def update(self):
        self.initializedGame()
        if(self.verify):
            self.verifyLogic(self.dealer,self.jogador)
        pass

    def draw(self):
        pyxel.cls(1)
        

Poker()