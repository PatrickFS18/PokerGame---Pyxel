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
        # Criar sala
        if pyxel.btnp(pyxel.KEY_C):
            self.cliente_socket.criar_sala()

        # Ingressar na sala
        if pyxel.btnp(pyxel.KEY_I) and self.cliente_socket.sala_selecionada is not None:
            if self.cliente_socket.sala_selecionada in self.cliente_socket.salas_disponiveis:
                sala = self.cliente_socket.salas_disponiveis[self.cliente_socket.sala_selecionada]
                if len(sala) < 2:  # Verifica se a sala tem espaço
                    self.cliente_socket.ingressar_sala(self.cliente_socket.sala_selecionada)
                    self.jogador.sala_selecionada = self.cliente_socket.sala_selecionada
                    print('testando o jogador: ', self.jogador.sala_selecionada)
                else:
                    print("A sala está cheia!")
            else:
                print("Sala selecionada não existe!")

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "Salas disponíveis:", pyxel.COLOR_WHITE)

        # Exibindo as salas e jogadores
        y_offset = 20
        for sala_id, jogadores in self.cliente_socket.salas_disponiveis.items():
            jogadores_str = ', '.join(jogadores)
            pyxel.text(10, y_offset, f"Sala {sala_id}: {jogadores_str}", pyxel.COLOR_WHITE)
            y_offset += 10

        # Exibir o botão de criação de sala
        pyxel.text(10, 110, "Pressione 'C' para criar uma sala", pyxel.COLOR_GREEN)
        pyxel.text(10, 120, "Pressione 'ENTER' para ingressar na sala selecionada", pyxel.COLOR_GREEN)

Poker()