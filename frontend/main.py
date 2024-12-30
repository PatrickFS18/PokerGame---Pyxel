import pyxel
from collections import Counter
from utils.servidorSocket import ServidorSocket
# Conectando ao servidor

class Poker:
    def __init__(self):
        self.cliente_socket = ServidorSocket()
        self.sala_selecionada_index = 0
        self.rodada = 0
        self.sala_id = None
        self.salas_list = None
        self.sala_atual = None
        self.proxima_carta = False
        self.rodada_solicitada = False 
        self.position_cards = [ #(local x,local y, width, height, topox, topoy, centrox, centroy)
                                (30,  38, 36, 52, 33, 41, 41, 60), # posição da carta 1
                                ( 70,  38, 36, 52, 73, 41, 81, 60), # posição da carta 2
                                ( 110,  38, 36, 52, 113, 41, 121, 60), # posição da carta 3
                                ( 150,  38, 36, 52, 153, 41, 161, 60), # posição da carta 4
                                ( 190,  38, 36, 52, 193, 41, 201, 60), # posição da carta 5
                                ( 14,  126, 36, 52, 17, 129, 25, 148), # posição da carta 6
                                ( 54,  126, 36, 52, 57, 129, 65, 148) # posição da carta 7
                                ]
        self.position_chips = [ # local x, local y, comprimento, altura, x1, y1, x2,y2
                                (136, 208, 24, 24, 105, 150, 129,174),
                                (160, 208, 24, 24, 137, 150, 161,174),
                                (184, 208, 24, 24, 193, 150, 217,174),
                                (208, 208, 24, 24, 225, 150, 249,174)
                                ]
        self.position_itens = { 
                            "Mesa" : ( 0,  0, 256, 192),
                            "Carta" : ( 0,  192, 35, 51),
                            "Verso" : ( 36,  192, 35, 51),
                            "Paus" : ( 80,  192, 15, 15),
                            "Copas" : ( 95,  192, 15, 15),
                            "Espada" : ( 110,  192, 15, 15),
                            "Ouro" : ( 125,  192, 15, 15),
                            "1" : ( 246,  192, 9, 15 ),
                            "2" : ( 155,  192, 15, 15),
                            "3" : ( 170,  192, 15, 15),
                            "4" : ( 185,  192, 15, 15),
                            "5" : ( 200,  192, 15, 15),
                            "6" : ( 215,  192, 15, 15),
                            "7" : ( 230,  192, 15, 15),
                            "8" : ( 120,  208, 15, 15),
                            "9" : ( 85,  208, 15, 15),
                            "10" : ( 147,  192, 15, 15),
                            "11" : ( 100,  208, 6, 15),
                            "12" : ( 106,  208, 7, 15),
                            "13" : ( 113,  208, 7, 15),
                        } 
        
        self.state = "menu"
        self.selected_option = -1 #-1 = neutro
        self.chips = False
        #frontend
        pyxel.init(256,192, title= "Poker Game")
        
        pyxel.mouse(True)
        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y
        # Detecta se o cursor está sobre uma das opções
        pyxel.load("my_resource.pyxres")
        pyxel.images[0]
        pyxel.run(self.update,self.draw)
        
    def update(self):
        self.salas_list = self.cliente_socket.salas_disponiveis
        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y
        if self.state == "menu":
            self.update_menu()

        elif self.state == "rooms":
            self.update_rooms()
            
        elif self.state == "online":
            self.update_online()

        elif self.state == "winner":
            self.update_winner()
        self.salas_list = self.cliente_socket.salas_disponiveis

    def update_menu(self):
        start_button = (98, 60, 158, 80)  # (x1, y1, x2, y2) para Jogo 
        
        rect_exit = (98, 100, 158, 120)  # Sair do Jogo

        if start_button[0] <= self.mx <= start_button[2] and start_button[1] <= self.my <= start_button[3]:
            self.selected_option = 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.selected_option = 0
                self.state = "online"
                
                print("Iniciando Jogo Local")

        elif rect_exit[0] <= self.mx <= rect_exit[2] and rect_exit[1] <= self.my <= rect_exit[3]:
            self.selected_option = 2
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.quit()  # Sai do jogo
        else:
            self.selected_option = -1

    def update_rooms(self):
        
        back_button = (243,3, 253, 13)  # (x1, y1, x2, y2) para voltar para o menu
        if back_button[0] <= self.mx <= back_button[2] and back_button[1] <= self.my <= back_button[3]:
            
            self.selected_option = 0
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.state = "menu"  
        else:
            self.selected_option == -1
            
    def update_online(self):

        ########### SALAS ###########
        if pyxel.btnp(pyxel.KEY_C) and self.state == "online":
            self.cliente_socket.criar_sala()
        if pyxel.btnp(pyxel.KEY_UP) and self.state == "online":
            self.sala_selecionada_index = max(0, self.sala_selecionada_index - 1)
        if pyxel.btnp(pyxel.KEY_DOWN) and self.state == "online": 
            self.sala_selecionada_index = min(len(self.salas_list) - 1, self.sala_selecionada_index + 1)
            
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.state == "online":
            sala_id = self.salas_list[self.sala_selecionada_index].get("sala_id")
            print(self.cliente_socket.sala_atual_info)
            if(self.cliente_socket.sala_atual_info is None):
                self.cliente_socket.chamar_nova_rodada(sala_id,self.cliente_socket.id_player) # Chama novo turno também. verificação na API por quem solicitou

            if self.cliente_socket.sala_atual_info is not None:
                print('RODADA ATUAL:  ',self.cliente_socket.sala_atual_info["rodada"])
                self.cliente_socket.chamar_nova_rodada(sala_id,self.cliente_socket.id_player) # Chama novo turno também. verificação na API por quem solicitou
            
        if pyxel.btnp(pyxel.KEY_I) and self.salas_list and self.state == "online":
            self.sala_id = self.salas_list[self.sala_selecionada_index].get("sala_id")
            sala_len = len(self.salas_list[self.sala_selecionada_index].get("jogadores"))
            if self.sala_id is not None and sala_len < 2:
                self.cliente_socket.ingressar_sala(self.sala_id)
                self.cliente_socket.sala_selecionada = self.sala_id  # Garantir que a sala selecionada é atualizada
        



        ####### JOGO ###########

        b_desistir = (98,120,138,140) #x1,y1,x2,y2    selected_option = 3
        b_apostar = (145,120,185,140) #x1,y1,x2,y2      selected_option = 4
        b_passar = (192,120,232,140) #x1,y1,x2,y2    selected_option = 5
        
        ## OPACIDADE DO BOTAO DESISTIR
        if b_desistir[0] <= self.mx <= b_desistir[2] and b_desistir[1] <= self.my <= b_desistir[3]:
            self.selected_option = 3
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.selected_option = 0
                #self.desistiu
                pass

        #OPACIDADE DO BOTAO APOSTAR
        elif b_apostar [0] <= self.mx <= b_apostar [2] and b_apostar [1] <= self.my <= b_apostar [3]:
            self.selected_option = 4
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # LOGICA DE UM BOTAO.
                if self.chips:
                    self.chips = False

                else:
                    self.chips = True
                    pass        
        #SE TU APOSTAR TU CAI NISSO
        elif self.chips: 
            # BUTOES DAS FICHAS, PS: N MEXE NISSO Q TTA DIREITIN
            for c in self.position_chips: 
                if c[4] <= self.mx <= c [5] and c [6] <= self.my <= c [7]:
                    self.chips = False
                    #SE CLICAR NA FICHA MUDA A RODADA
                    #self.cliente_socket.sala_atual_info['rodada'] +=1
                    pass            

        #OPACIDADE DO BOTAO DE PASSAR
        elif b_passar [0] <= self.mx <= b_passar [2] and b_passar [1] <= self.my <= b_passar [3]:
            self.selected_option = 5
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.selected_option = 0
                #self.cliente_socket.sala_atual_info['rodada'] +=1
                pass    

        else:
            self.selected_option = -1
  
    def update_winner(self):
        
        if pyxel.btnp(pyxel.KEY_R):
            if self.cliente_socket.winner:
                self.winner = self.cliente_socket.winner

            # nao faz nada ainda
# Variáveis de controle:

    

    def draw(self):
        pyxel.cls(0)
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "online":
            self.draw_online()    
        elif self.state == "winner":
            pass
            #self.draw_winner()
        
    def draw_cartas_dealer_e_jogador(self, sala_atual,rodada):
        
        pyxel.blt(0, 0, 0, 0, 0, 256, 192)
        jogador_mao = None
        dealer_mao = None
        y_offset = 20
        
        for j in sala_atual.get("jogadores", []):
            
            if isinstance(j, dict) and j.get("id") == self.cliente_socket.id_player:
                jogador_mao = j["mao"]
                
            if 'dealer' in sala_atual:
                dealer_mao = sala_atual["dealer"]["mao"]                    
            
        if jogador_mao and dealer_mao is not None:      
            for v in range(5):
                p_carta = self.position_cards[i] 
                #carta
                pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens['Verso'][0], self.position_itens['Verso'][1], 36, 52) 
                
            for i in range(len(dealer_mao)-(3-rodada)): #explico dps
                #if(i+1 <= sala_atual["rodada"] + 2):

                p_valor = self.position_itens[f'{dealer_mao[i]["valor"]}']
                p_naipe = self.position_itens[dealer_mao[i]["naipe"]]
                p_carta = self.position_cards[i]
                #(local x,local y, width, height, topox, topoy, centrox, centroy)
                
                #(x plot, y plot, imagem, x imagem, y imagem, comprimento, altura)

                #carta
                pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens['Carta'][0], self.position_itens['Carta'][1], 36, 52)
                #numero topo
                pyxel.blt(p_carta[4], p_carta[5], 0, p_valor[0], p_valor[1], p_valor[2], p_valor[3])
                #naipe centro
                pyxel.blt(p_carta[6], p_carta[7], 0, p_naipe[0], p_naipe[1], p_naipe[2], p_naipe[3])
                
            for i in range(len(jogador_mao)):
                p_valor = self.position_itens[f'{jogador_mao[i]["valor"]}']
                p_naipe = self.position_itens[jogador_mao[i]["naipe"]]
                p_carta = self.position_cards[i+5]

                #carta
                pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens['Carta'][0], self.position_itens['Carta'][1], 36, 52)
                #numero topo
                pyxel.blt(p_carta[4], p_carta[5], 0, p_valor[0], p_valor[1], p_valor[2], p_valor[3])
                #naipe centro
                pyxel.blt(p_carta[6], p_carta[7], 0, p_naipe[0], p_naipe[1], p_naipe[2], p_naipe[3])
        
        color_desistir = 8 if self.selected_option == 1 else 7
        pyxel.rect(98, 120, 40, 20, color_desistir)
        pyxel.text(110, 132, "Desistir", 0)

        color_apostar = 5 if self.selected_option == 1 else 7
        pyxel.rect(145, 120, 40, 20, color_apostar)
        pyxel.text(154, 132, "Apostar", 0)

        color_passar = 12 if self.selected_option == 1 else 7
        pyxel.rect(192, 120, 40, 20, color_passar)
        pyxel.text(220, 132, "Passar", 0)

        if self.chips:
            for L in range(len(self.position_chips)):
                # local x, local y, comprimento, altura, x1, y1, x2,y2

                pyxel.blt(L[0], L[1], 0, L[4], L[5], 24,24)    
            
            # pyxel.text(10, 70, f"Player {self.cliente_socket.id_player}", pyxel.COLOR_RED)
            
            # pyxel.text(10, 10, f"Sala {self.cliente_socket.sala_selecionada} - Jogadores:", pyxel.COLOR_WHITE)

    def draw_menu(self):
        # Título do Jogo
        pyxel.text(102, 20, "Poker Game", pyxel.frame_count %16)

        # Opção Jogo Online
        color_online = 11 if self.selected_option == 1 else 7
        pyxel.rect(98, 60, 60, 20, color_online)
        pyxel.text(118, 67, "Jogar", 0)

        color_exit = 8 if self.selected_option == 2 else 7
        pyxel.rect(98, 100, 60, 20, color_exit)
        pyxel.text(120, 107, "Sair", 0)

    def draw_online(self):
        
        if self.cliente_socket.sala_selecionada is None:
            
            pyxel.text(10, 10, "Salas disponíveis:", pyxel.COLOR_WHITE)

            y_offset = 20
            for index, sala in enumerate(self.cliente_socket.salas_disponiveis):
                sala_id = sala.get("sala_id", "N/A")
                jogadores_str = ', '.join([f"Player {j['id']}" for j in sala.get("jogadores", [])])
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
                self.sala_atual = next((s for s in self.cliente_socket.salas_disponiveis if s.get("sala_id") == self.cliente_socket.sala_selecionada), None)
                if self.sala_atual:
                    #Aqui deve desenhar 
                    pyxel.text(10, 10, f"Sala {self.cliente_socket.sala_selecionada} - Jogadores:", pyxel.COLOR_WHITE)
                    y_offset = 20
                    pyxel.text(10, 70, f"Player {self.cliente_socket.id_player}", pyxel.COLOR_RED)

                    for j in self.sala_atual.get("jogadores", []):
                        if isinstance(j, dict) and j.get("id") == self.cliente_socket.id_player:
                            jogadores_str = ', '.join([f"Player {jogador['id']}" for jogador in self.sala_atual.get("jogadores", [])])
                            pyxel.text(10, y_offset, jogadores_str, pyxel.COLOR_WHITE)
            
                    if len(self.sala_atual["jogadores"]) < 2:
                        pyxel.text(10, y_offset + 20, "Aguardando jogadores...", pyxel.COLOR_RED)
                    else:
                        if self.cliente_socket.winner is not None:
                            if self.cliente_socket.winner == 0:
                                pyxel.text(20, 60, f"Empate!!", pyxel.COLOR_GREEN)
                            else:
                                pyxel.text(20, 60, f"O ganhador é o jogador {self.cliente_socket.winner}!", pyxel.COLOR_GREEN)
                            

                        sala = self.cliente_socket.salas_disponiveis[self.sala_selecionada_index]
                        
                        # Exibir cartas do dealer e do jogador com o ID atual
                        if self.cliente_socket.sala_atual_info is not None:
                            self.draw_cartas_dealer_e_jogador(self.sala_atual,self.cliente_socket.sala_atual_info['rodada'])
                                                
    pass
    ## def draw_winner(self):                
    #     self.draw_cartas_dealer_e_jogador(self.sala_atual,self.rodada)
                                            

Poker()