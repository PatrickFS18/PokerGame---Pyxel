import pyxel

from api.utils.jogador import Jogador
from api.utils.baralho import Baralho
from collections import Counter
from api.utils.compare import Compare
from servidorSocket import ServidorSocket
# Conectando ao servidor


class Poker:
    def __init__(self):
        self.cliente_socket = ServidorSocket()
        
        self.jogador = Jogador()
        self.adversario = Jogador()
        self.dealer = Jogador()
        self.baralho = Baralho()
        self.is_initialized = False
        self.verify = True
        self.compare_1_1 = None
        self.compare_1_2 = None        
        self.compare = None
        self.sala_selecionada_index = 0 
        self.salas_list = None
        pyxel.init(160,120)
        pyxel.run(self.update,self.draw)
        
        
    def initializedGame(self):
        if(self.is_initialized == False):
            # Instância de Initialização dos jogadores e Mesa e embaralhamento de cartas
            
            # self.baralho.gerarCartas()
            # self.baralho.embaralharCartas()
            # cartas = self.baralho.cartas
            
            # # Distribuição de cartas 
            # for i in range (0,4,2):
            #     self.jogador.mao.append(cartas[i])
            #     cartas.pop(0)
                
            # for i in range(0,2):
            #     self.adversario.mao.append(cartas[i])
            #     cartas.pop(0)
                
            # for i in range (0,5):
            #     self.dealer.mao.append(cartas[i])
            #     cartas.pop(0)
            
            # CHAMAR FUNÇÃO DO BACKEND PARA PEGAR ESSA INFORMAÇÃO
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
                maior_carta_1 = self.compare_1.maior_valor_cartas(mao_jogador_1)
                maior_carta_2 = self.compare_2.maior_valor_cartas(mao_jogador_2)
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
    # Criação de sala
        salas_list = list(self.cliente_socket.salas_disponiveis.items())

        if pyxel.btnp(pyxel.KEY_C):
            self.cliente_socket.criar_sala()

    # Navegar pelas salas disponíveis
        if pyxel.btnp(pyxel.KEY_UP):
            self.sala_selecionada_index = max(0, self.sala_selecionada_index - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.sala_selecionada_index = min(len(salas_list) - 1, self.sala_selecionada_index + 1)

        # Ingressar na sala selecionada
        if pyxel.btnp(pyxel.KEY_I) and salas_list is not None:
            sala_id = salas_list[self.sala_selecionada_index][0]
            self.cliente_socket.ingressar_sala(sala_id)
            self.cliente_socket.sala_selecionada = sala_id

        if pyxel.btnp(pyxel.KEY_L) and salas_list is not None:
            print(salas_list)
            
    def draw(self):
       
        pyxel.cls(0)
        if self.cliente_socket.sala_selecionada is None:
            pyxel.text(10, 10, "Salas disponíveis:", pyxel.COLOR_WHITE)

            # Exibindo as salas disponíveis
            y_offset = 20
            salas_list = list(self.cliente_socket.salas_disponiveis.items())
            for index, (sala_id, jogadores) in enumerate(salas_list):
                jogadores_str = ', '.join([f"Player {j}" for j in jogadores])
                color = pyxel.COLOR_YELLOW if index == self.sala_selecionada_index else pyxel.COLOR_WHITE
                pyxel.text(10, y_offset, f"Sala {sala_id}: {jogadores_str}", color)
                y_offset += 10

            # Mostrar controles
            pyxel.text(10, 110, "Pressione 'C' para criar uma sala", pyxel.COLOR_GREEN)
            pyxel.text(10, 120, "Setas: navegar | ENTER: ingressar", pyxel.COLOR_GREEN)
        else:
            salas_list = list(self.cliente_socket.salas_disponiveis.items())
            y_offset = 20
                
            for index, (sala_id, jogadores) in enumerate(salas_list):
                jogadores_str = ', '.join([f"Player {j}" for j in jogadores])
                color = pyxel.COLOR_YELLOW if index == self.sala_selecionada_index else pyxel.COLOR_WHITE
                pyxel.text(10, y_offset, f"{jogadores_str}", color)
                y_offset += 10
            if(len(jogadores) < 2 ):
                pyxel.text(10, 10,f"Aguardando Jogadores para a sala: {self.cliente_socket.sala_selecionada} ", pyxel.COLOR_RED)
            else:
                
                pyxel.text(10, 10,f"A partida ja vai iniciar!!", pyxel.COLOR_GREEN)

                
Poker()