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
        if pyxel.btnp(pyxel.KEY_C):  # Criar sala
            self.cliente_socket.criar_sala()

        if pyxel.btnp(pyxel.KEY_I) and self.cliente_socket.sala_selecionada is not None:  # Ingressar na sala
            self.cliente_socket.ingressar_sala(self.cliente_socket.sala_selecionada)
            self.jogador.sala_selecionada = self.cliente_socket.sala_selecionada
            print('Jogador entrou na sala:', self.jogador.sala_selecionada)

        # Navegação pelas salas disponíveis (usando as teclas de seta)
        if pyxel.btnp(pyxel.KEY_DOWN):  # Descer para a próxima sala
            self.sala_selecionada_index = (self.sala_selecionada_index + 1) % len(self.cliente_socket.salas_disponiveis)
        
        if pyxel.btnp(pyxel.KEY_UP):  # Subir para a sala anterior
            self.sala_selecionada_index = (self.sala_selecionada_index - 1) % len(self.cliente_socket.salas_disponiveis)
    
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "Salas disponíveis:", pyxel.COLOR_WHITE)

        # Exibindo as salas e jogadores
        y_offset = 20
        salas_list = list(self.cliente_socket.salas_disponiveis.items())  # Convertendo o dicionário para lista
        for index, (sala_id, jogadores) in enumerate(salas_list):
            # Exibe apenas o número da sala e o número dos jogadores
            jogadores_str = ', '.join([f"Player {i+1}" for i in range(len(jogadores))])
            color = pyxel.COLOR_WHITE if index != self.sala_selecionada_index else pyxel.COLOR_YELLOW
            pyxel.text(10, y_offset, f"Sala {sala_id}: {jogadores_str}", color)
            y_offset += 10

        # Atualizar o botão de ingresso na sala
        if pyxel.btnp(pyxel.KEY_I) and self.cliente_socket.sala_selecionada is not None:
            self.cliente_socket.sala_selecionada = salas_list[self.sala_selecionada_index][0]
            print(f"Sala {self.cliente_socket.sala_selecionada} selecionada para ingresso.")

        # Exibir o botão de criação de sala
        pyxel.text(10, 110, "Pressione 'C' para criar uma sala", pyxel.COLOR_GREEN)
        pyxel.text(10, 120, "Pressione 'ENTER' para ingressar na sala selecionada", pyxel.COLOR_GREEN)

Poker()