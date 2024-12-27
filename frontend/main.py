import pyxel

from utils.jogador import Jogador
from utils.baralho import Baralho
from collections import Counter
from utils.servidorSocket import ServidorSocket
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

    def update(self):
        self.salas_list = self.cliente_socket.salas_disponiveis

        if pyxel.btnp(pyxel.KEY_C):
            self.cliente_socket.criar_sala()

        if pyxel.btnp(pyxel.KEY_UP):
            self.sala_selecionada_index = max(0, self.sala_selecionada_index - 1)
        if pyxel.btnp(pyxel.KEY_DOWN): 
            self.sala_selecionada_index = min(len(self.salas_list) - 1, self.sala_selecionada_index + 1)

        if pyxel.btnp(pyxel.KEY_I) and self.salas_list:
            sala_id = self.salas_list[self.sala_selecionada_index].get("sala_id")
            if sala_id is not None:
                self.cliente_socket.ingressar_sala(sala_id)
                self.cliente_socket.sala_selecionada = sala_id  # Garantir que a sala selecionada é atualizada

    def draw(self):
        if self.cliente_socket.sala_selecionada is None:
            pyxel.cls(0)
            pyxel.text(10, 10, "Salas disponíveis:", pyxel.COLOR_WHITE)

            y_offset = 20
            for index, sala in enumerate(self.cliente_socket.salas_disponiveis):
                sala_id = sala.get("sala_id", "N/A")
                jogadores_str = ', '.join([f"Player {j}" for j in sala.get("jogadores", [])])
                color = pyxel.COLOR_YELLOW if index == self.sala_selecionada_index else pyxel.COLOR_WHITE
                pyxel.text(10, y_offset, f"Sala {sala_id}: {jogadores_str}", color)
                y_offset += 10

            pyxel.text(10, y_offset + 10, "Pressione 'C' para criar uma sala", pyxel.COLOR_GREEN)
            pyxel.text(10, y_offset + 20, "Setas: navegar | ENTER: ingressar", pyxel.COLOR_GREEN)
        else:
            pyxel.cls(0)
            if (0 <= self.sala_selecionada_index < len(self.cliente_socket.salas_disponiveis)) and self.cliente_socket.salas_disponiveis[self.sala_selecionada_index] is not None:
                sala = self.cliente_socket.salas_disponiveis[self.sala_selecionada_index]
                sala_id = sala["sala_id"]
                sala_atual = next((s for s in self.cliente_socket.salas_disponiveis if s.get("sala_id") == self.cliente_socket.sala_selecionada), None)
                if sala_atual:
                    pyxel.text(10, 10, f"Sala {self.cliente_socket.sala_selecionada} - Jogadores:", pyxel.COLOR_WHITE)
                    y_offset = 20
                    
                    for j in sala_atual.get("jogadores", []):
                        # Verifica se j é um dicionário antes de acessar a chave "id"
                        if isinstance(j, dict) and j.get("id") == self.cliente_socket.id_player:
                            jogadores_str = ', '.join([f"Player {jogador['mao']}" for jogador in sala_atual.get("jogadores", [])])
                            pyxel.text(10, y_offset, jogadores_str, pyxel.COLOR_WHITE)

                    if len(sala_atual["jogadores"]) < 2:
                        pyxel.text(10, y_offset + 20, "Aguardando jogadores...", pyxel.COLOR_RED)
                    else:
                        pyxel.text(10, y_offset + 20, "A partida já vai iniciar!", pyxel.COLOR_GREEN)
                        if(sala["rodada"] == 0):
                            
                            self.cliente_socket.chamar_nova_rodada(sala_id)
                            print('ssala atual é: ',sala_atual)
                            sala["rodada"] = 1
Poker()