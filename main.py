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
    
    def maior_valor_cartas(mao):
                    maior_valor = -1  # Inicializa com um valor pequeno
                    for jogada in mao:
                        for dicionario in jogada:
                            for carta in dicionario.keys():
                                if carta > maior_valor:
                                    maior_valor = carta
                    return maior_valor
                    
                    
    def verifyLogic(self, dealer, jogador):
        print('JOGADOR 1!!!')
        self.compare_1 = Compare(self.jogador.mao, self.dealer.mao)
        self.compare_1.game()
        self.compare_1.high_cards()
        
        self.compare_1.countEqualValues()
        print('victory',self.compare_1.victory)
        
        print('JOGADOR 2!!!')
        
        self.compare_2 = Compare(self.adversario.mao, self.dealer.mao)
        self.compare_2.game()
        self.compare_2.high_cards()
        
        self.compare_2.countEqualValues()
        
        
        print('victory',self.compare_2.victory)
        print('as maos do cara 1: ',self.compare_1.highest_hand_value)

        player_1_victory = max(self.compare_1.victory)
        player_2_victory = max(self.compare_2.victory)
        
        print('Valor vitoria jogador 1: ',player_1_victory)
        print('Valor vitoria jogador 2: ',player_2_victory)
        print('as maos do cara 2: ',self.compare_2.highest_hand_value)
        
    
        if(player_1_victory == player_2_victory) and (player_1_victory != 0 and player_2_victory!=0):
            print('Possível empate. verificar qual carta maior')

            mao_jogador_1 = self.compare_1.highest_hand_value
            mao_jogador_2 = self.compare_2.highest_hand_value
            # Verificação de empate
            maior_carta_1 = self.maior_valor_cartas(mao_jogador_1)
            maior_carta_2 = self.maior_valor_cartas(mao_jogador_2)
            print(maior_carta_1)
            print(maior_carta_2)
            # Função para encontrar o maior valor de carta em uma mão
            if maior_carta_1 > maior_carta_2:
                print(f"Jogador 1 vence pelo desempate! Carta mais alta: {maior_carta_1}")
            elif maior_carta_2 > maior_carta_1:
                print(f"Jogador 2 vence pelo desempate! Carta mais alta: {maior_carta_2}")
            else:
                print(f"Empate absoluto! Ambos têm a mesma carta mais alta: {maior_carta_1}")
                
        if(player_1_victory == player_2_victory and (player_1_victory == 0 and player_2_victory ==0)):
            if(self.compare_1.high_card > self.compare_2.high_card):
                print('Jogador 1 venceu por carta alta. O valor da carta: ',self.compare_1.high_card)
            elif(self.compare_1.high_card < self.compare_2.high_card):
                print('Jogador 2 venceu por carta alta. O valor da carta: ',self.compare_2.high_card)
            elif(self.compare_1.high_card == self.compare_2.high_card):
                print('Empate com carta alta! Mesmo valor: ',self.compare_1.high_card)

        # Comparação para determinar o vencedor  
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