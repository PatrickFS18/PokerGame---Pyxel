import pyxel

from jogador import Jogador
from baralho import Baralho
from collections import Counter
from compare import Compare
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
        self.compare = None
        self.sala_selecionada_index = 0 
        self.salas_list = None
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
        self.compare = Compare(self.jogador.mao, self.dealer.mao)
        self.compare.game()
        
        #self.compare.flush()
        self.compare.countEqualValues()
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