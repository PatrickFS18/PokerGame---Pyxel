import pyxel
from collections import Counter
from utils.servidorSocket import ServidorSocket


class Poker:
    def __init__(self):
        self.cliente_socket = ServidorSocket()
        self.sala_selecionada_index = 0
        self.rodada = 0
        self.sala_id = None
        self.salas_list = None
        self.sala_atual = None
        self.winner = None
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
                                (184, 208, 24, 24, 169, 150, 217,174),
                                (208, 208, 24, 24, 201, 150, 249,174)
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
                            "Sua" : ( 8, 192, 80, 16),
                            "Venceu" : ( 88, 192, 160, 32),
                            "Perdeu" : ( 88, 224, 160,32),
                            "Empate" : (88,152,150,32)
                        }

        self.verificar_ganhador = False
        self.state = "menu"
        self.selected_option = -1 #-1 = neutro



        self.chips = False
        #frontend
        pyxel.init(256,192, title= "Poker Game")


        self.setup_music()
        pyxel.mouse(True)
        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y
        # Detecta se o cursor está sobre uma das opções
        pyxel.load("my_resource.pyxres")
        pyxel.images[0]
        pyxel.images[1]
        pyxel.run(self.update,self.draw)

    ### SONS PRONTOS DA COMUNIDADE DA PYXEL       
    def setup_music(self):
        pyxel.sounds[0].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p",
            "6",
            "vffn fnff vffs vfnn",
            25,
        )
        pyxel.sounds[1].set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2 f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
            "s",
            "6",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            25,
        )
        pyxel.sounds[2].set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1 a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )
        pyxel.sounds[3].set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1 f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )
        pyxel.sounds[4].set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 25
        )
        self.play_music(False, False, False)


    def play_music(self, ch0, ch1, ch2):
        if ch0:
            pyxel.play(0, [0, 1], loop=True)
        else:
            pyxel.stop(0)
        if ch1:
            pyxel.play(1, [2, 3], loop=True)
        else:
            pyxel.stop(1)
        if ch2:
            pyxel.play(2, 4, loop=True)
        else:
            pyxel.stop(2)

    # Parte inicial do frontend 
    def update(self):
        self.salas_list = self.cliente_socket.salas_disponiveis
        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y
        if pyxel.btnp(pyxel.KEY_M):
            self.play_music(False, False, False)

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
                self.state = "rooms"

                #print("Iniciando Jogo Local")

        elif rect_exit[0] <= self.mx <= rect_exit[2] and rect_exit[1] <= self.my <= rect_exit[3]:
            self.selected_option = 2
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.quit()  # Sai do jogo
        else:
            self.selected_option = -1

    def update_rooms(self):

        ########### SALAS ###########
        if pyxel.btnp(pyxel.KEY_C):
            self.cliente_socket.criar_sala()
            self.state = "online"
        if pyxel.btnp(pyxel.KEY_UP):
            self.sala_selecionada_index = max(0, self.sala_selecionada_index - 1)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.sala_selecionada_index = min(len(self.salas_list) - 1, self.sala_selecionada_index + 1)

        if pyxel.btnp(pyxel.KEY_I) and self.salas_list:
            self.sala_id = self.salas_list[self.sala_selecionada_index].get("sala_id")
            sala_len = len(self.salas_list[self.sala_selecionada_index].get("jogadores"))
            if self.sala_id is not None and sala_len < 2:
                self.cliente_socket.ingressar_sala(self.sala_id)
                self.cliente_socket.sala_selecionada = self.sala_id  # Garantir que a sala selecionada é atualizada
                self.state = "online"

    def update_online(self):

        ####### JOGO ###########

        b_apostar = (145,120,185,140) #x1,y1,x2,y2      selected_option = 4
        b_passar = (192,120,232,140) #x1,y1,x2,y2    selected_option = 5

        #OPACIDADE DO BOTAO APOSTAR
        if b_apostar [0] <= self.mx <= b_apostar [2] and b_apostar [1] <= self.my <= b_apostar [3]:
            self.selected_option = 4
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # LOGICA DE UM BOTAO.
                if self.chips:
                    self.chips = False
                else:
                    self.chips = True

        #SE TU APOSTAR TU CAI NISSO
        elif self.chips:
            # BUTOES DAS FICHAS, PS: N MEXE NISSO Q TTA DIREITIN
            for c in self.position_chips:
                if c[4] <= self.mx <= c[5] and c[6] <= self.my <= c[7]:
                    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):

                        self.chips = False
                        sala_id = self.salas_list[self.sala_selecionada_index].get("sala_id")
                        if self.cliente_socket.sala_atual_info is not None and self.cliente_socket.sala_atual_info["rodada"] == 6:

                            self.verificar_ganhador = True
                            self.state = "winner"
                        else:
                            self.cliente_socket.chamar_nova_rodada(sala_id,self.cliente_socket.id_player) # Chama novo turno também. verificação na API por quem solicitou

                    #SE CLICAR NA FICHA MUDA A RODADA


        #OPACIDADE DO BOTAO DE PASSAR
        elif b_passar [0] <= self.mx <= b_passar [2] and b_passar [1] <= self.my <= b_passar [3]:

            self.selected_option = 5
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                sala_id = self.salas_list[self.sala_selecionada_index].get("sala_id")

                self.selected_option = 0
                if self.cliente_socket.sala_atual_info is not None and self.cliente_socket.sala_atual_info["rodada"] == 6:
                    self.verificar_ganhador = True
                    self.state = "winner"
                else:
                    self.cliente_socket.chamar_nova_rodada(sala_id,self.cliente_socket.id_player) # Chama novo turno também. verificação na API por quem solicitou


        elif self.verificar_ganhador != True:
            self.selected_option = -1
        if self.winner is not None:
            self.state = "winner"

    def update_winner(self):

        if self.cliente_socket.winner:
            self.winner = self.cliente_socket.winner

        #talvez jogar novamente


    def draw(self):
        pyxel.cls(0)
        if self.state == "menu":
            self.draw_menu()

        elif self.cliente_socket.sala_selecionada is None and self.state == "rooms":
            self.draw_rooms()

        elif self.cliente_socket.sala_selecionada is not None and self.state == "online":
            self.draw_online()
        elif self.state == "winner":
            self.draw_winner()

    def draw_cartas_dealer_e_jogador(self, sala_atual,rodada):

        if self.cliente_socket.sala_atual_info is not None:
            self.rodada = self.cliente_socket.sala_atual_info["rodada"]
            #print("entrou aqui aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ",self.rodada)
            
            rodada = int(self.rodada)
            if rodada == 6:
                self.state = "winner"
        pyxel.blt(0, 0, 0, 0, 0, 256, 192)
        jogador_mao = None
        dealer_mao = None
        y_offset = 20

        jogadores = []
        for j in sala_atual.get("jogadores", []):
            if isinstance(j, dict):
                jogadores.append(j.get("id"))
            if isinstance(j, dict) and j.get("id") == self.cliente_socket.id_player:
                jogador_mao = j["mao"]
            if "dealer" in sala_atual:
                dealer_mao = sala_atual["dealer"]["mao"]

        if jogador_mao and dealer_mao is not None:
            for i in range(5):
                p_carta = self.position_cards[i]
                #carta
                pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens["Verso"][0], self.position_itens["Verso"][1], 36, 52)

            for i in range(len(dealer_mao)): # Lógica para contar a partir da terceira carta
                if(i <= rodada // 2 + 2):
                    p_valor = self.position_itens[f'{dealer_mao[i]["valor"]}']
                    p_naipe = self.position_itens[dealer_mao[i]["naipe"]]
                    p_carta = self.position_cards[i]
                    #(local x,local y, width, height, topox, topoy, centrox, centroy)

                    #(x plot, y plot, imagem, x imagem, y imagem, comprimento, altura)

                    #carta
                    pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens["Carta"][0], self.position_itens["Carta"][1], 36, 52)
                    #numero topo
                    pyxel.blt(p_carta[4], p_carta[5], 0, p_valor[0], p_valor[1], p_valor[2], p_valor[3])
                    #naipe centro
                    pyxel.blt(p_carta[6], p_carta[7], 0, p_naipe[0], p_naipe[1], p_naipe[2], p_naipe[3])

            for i in range(len(jogador_mao)):
                p_valor = self.position_itens[f'{jogador_mao[i]["valor"]}']
                p_naipe = self.position_itens[jogador_mao[i]["naipe"]]
                p_carta = self.position_cards[i+5]

                #carta
                pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens["Carta"][0], self.position_itens["Carta"][1], 36, 52)
                #numero topo
                pyxel.blt(p_carta[4], p_carta[5], 0, p_valor[0], p_valor[1], p_valor[2], p_valor[3])
                #naipe centro
                pyxel.blt(p_carta[6], p_carta[7], 0, p_naipe[0], p_naipe[1], p_naipe[2], p_naipe[3])

       
        color_apostar = 5 if self.selected_option == 4 else 7
        pyxel.rect(145, 120, 40, 20, color_apostar)
        pyxel.text(151, 127, "Apostar", 0)

        color_passar = 12 if self.selected_option == 5 else 7
        pyxel.rect(192, 120, 40, 20, color_passar)
        pyxel.text(201, 127, "Passar", 0)

        if self.chips:
            for L in self.position_chips:
                # local x, local y, comprimento, altura, x1, y1, x2,y2
                pyxel.blt(L[4], L[5], 0, L[0], L[1], 24,24)
        #print(jogadores)
        if len(jogadores) == 2: 
            p_sua = self.position_itens["Sua"]
            if jogadores[0] == self.cliente_socket.id_player and rodada % 2 != 0 :
                pyxel.blt(16, 100, 1, p_sua[0], p_sua[1], p_sua[2], p_sua[3])
            if jogadores[1] == self.cliente_socket.id_player and rodada % 2 == 0:
                pyxel.blt(16, 100, 1, p_sua[0], p_sua[1], p_sua[2], p_sua[3])

    def draw_menu(self):
        pyxel.cls(0)  # Fundo preto

        # Fundo do menu com gradiente
        for y in range(192):
            pyxel.line(0, y, 256, y, pyxel.COLOR_NAVY if y % 2 == 0 else pyxel.COLOR_DARK_BLUE)

        # Título do jogo com efeito de brilho, centralizado
        pyxel.text(107, 20, "POKER GAME", pyxel.frame_count % 16)

        # Moldura decorativa para o menu, centralizada
        pyxel.rectb(78, 50, 100, 100, pyxel.COLOR_YELLOW)
        pyxel.rectb(76, 48, 104, 104, pyxel.COLOR_RED)

        # Opções do menu com destaque para a selecionada
        self.draw_menu_option("JOGAR", 98, 75, self.selected_option == 1)
        self.draw_menu_option("SAIR", 98, 115, self.selected_option == 2)

    def draw_menu_option(self, text, x, y, is_selected):
        color_box = pyxel.COLOR_ORANGE if is_selected else pyxel.COLOR_GRAY
        color_text = pyxel.COLOR_BLACK if is_selected else pyxel.COLOR_WHITE
        pyxel.rect(x - 10, y - 5, 80, 20, color_box)  # Ajustado para centralizar
        pyxel.text(x, y, text, color_text)

    def draw_rooms(self):
        # Fundo para a seção de salas
        pyxel.rect(20, 10, 216, 150, pyxel.COLOR_NAVY)
        pyxel.rectb(18, 8, 220, 154, pyxel.COLOR_YELLOW)

        # Título centralizado
        title_x = 256 // 2 - len("SALAS DISPONÍVEIS") * 2
        pyxel.text(title_x, 15, "SALAS DISPONÍVEIS", pyxel.COLOR_WHITE)

        # Exibição das salas
        y_offset = 40
        for index, sala in enumerate(self.cliente_socket.salas_disponiveis):
            sala_id = sala.get("sala_id", "N/A")
            jogadores_str = ", ".join([f'Player {j["id"]}' for j in sala.get("jogadores", [])])

            # Destaque para a sala selecionada
            is_selected = index == self.sala_selecionada_index
            color = pyxel.COLOR_YELLOW if is_selected else pyxel.COLOR_WHITE
            bg_color = pyxel.COLOR_DARK_BLUE if is_selected else pyxel.COLOR_DARK_BLUE

            # Fundo do item e texto centralizado
            pyxel.rect(30, y_offset - 2, 196, 14, bg_color)
            text_x = 256 // 2 - len(f'Sala {sala_id}: {jogadores_str}') * 2
            pyxel.text(text_x, y_offset, f'Sala {sala_id}: {jogadores_str}', color)

            y_offset += 18

        # Instruções centralizadas
        instructions = [
            "Pressione 'C' para criar uma sala",
            "Setas: navegar | ENTER: ingressar"
        ]
        for i, text in enumerate(instructions):
            instruction_x = 256 // 2 - len(text) * 2
            pyxel.text(instruction_x, y_offset + (i * 10) + 10, text, pyxel.COLOR_GREEN)

    def draw_online(self):
        pyxel.cls(0)

        if (0 <= self.sala_selecionada_index < len(self.cliente_socket.salas_disponiveis)) and self.cliente_socket.salas_disponiveis[self.sala_selecionada_index] is not None:
            # Sala selecionada disponível e não nula

            # Pega a sala atual
            sala = self.cliente_socket.salas_disponiveis[self.sala_selecionada_index]
            sala_id = sala["sala_id"]
            self.sala_atual = next((s for s in self.cliente_socket.salas_disponiveis if s.get("sala_id") == self.cliente_socket.sala_selecionada), None)

            # Se tiver sala atual
            if self.sala_atual:
                pyxel.text(10, 10, f'Sala {self.cliente_socket.sala_selecionada} - Jogadores:', pyxel.COLOR_WHITE)
                y_offset = 20

                # Exibe o jogador atual
                pyxel.text(10, 70, f'Player {self.cliente_socket.id_player}', pyxel.COLOR_RED)

                # Adiciona os jogadores na sala em uma string
                jogadores_str = ", ".join([f'Player {jogador["id"]}' for jogador in self.sala_atual.get("jogadores", []) if isinstance(jogador, dict)])
                if jogadores_str:
                    pyxel.text(10, y_offset, jogadores_str, pyxel.COLOR_WHITE)

                # Verifica a quantidade de jogadores na sala
                if len(self.sala_atual["jogadores"]) < 2:
                    pyxel.text(10, y_offset + 20, "Aguardando jogadores...", pyxel.COLOR_RED)

                else:

                    sala = self.cliente_socket.salas_disponiveis[self.sala_selecionada_index]

                    # Exibir cartas do dealer e do jogador com o ID atual
                    self.draw_cartas_dealer_e_jogador(self.sala_atual,self.rodada)


    def draw_winner(self):
        pyxel.cls(11)
        p_venceu = self.position_itens["Venceu"]
        p_perdeu = self.position_itens["Perdeu"]
        p_empate = self.position_itens["Empate"]
        jogadores = self.sala_atual.get("jogadores", [])
        jogadas = self.cliente_socket.jogadas

        if self.winner is not None and len(jogadores) == 2:
            id_player = self.cliente_socket.id_player
            adversario_id = next(j["id"] for j in jogadores if j["id"] != id_player)
            jogador_mao = next(j["mao"] for j in jogadores if j["id"] == id_player)
            adversario_mao = next(j["mao"] for j in jogadores if j["id"] == adversario_id)
            dealer_mao = self.sala_atual["dealer"]
            # Converter a mão em texto organizado
            def formatar_mao(mao):
                return ", ".join([f'{carta["valor"]} de {carta["naipe"]}' for carta in mao])

            jogador_mao_formatada = formatar_mao(jogador_mao)
            adversario_mao_formatada = formatar_mao(adversario_mao)
            dealer_mao_formatada =formatar_mao(dealer_mao["mao"])
            # Iterar sobre as jogadas para encontrar as jogadas correspondentes
            jogada_atual = next((j[str(id_player)] for j in jogadas if str(id_player) in j), "Jogada não encontrada")
            jogada_adversario = next((j[str(adversario_id)] for j in jogadas if str(adversario_id) in j), "Jogada não encontrada")
            #print(dealer_mao_formatada)
            # Determina a mensagem de resultado e exibe gráficos e textos
            if self.winner == 0:  # Empate
                #print(self.winner)
                pyxel.blt(53, 80, 1, p_empate[0], p_empate[1], p_empate[2], p_empate[3])
                pyxel.text(52, 100, "Empate!", pyxel.COLOR_WHITE)
                pyxel.text(52, 120, f"Sua mao: {jogador_mao_formatada}", pyxel.COLOR_WHITE)
                pyxel.text(52, 130, f"Mao do adversario: {adversario_mao_formatada}", pyxel.COLOR_RED)
                pyxel.text(52, 150, f"Sua jogada: {jogada_atual}", pyxel.COLOR_DARK_BLUE)
                pyxel.text(52, 160, f"Jogada do adversario: {jogada_adversario}", pyxel.COLOR_RED)

            elif id_player == self.winner:  # Vitória
                pyxel.blt(48, 80, 1, p_venceu[0], p_venceu[1], p_venceu[2], p_venceu[3])
                pyxel.text(52, 120, f"Sua mao era: {jogador_mao_formatada}", pyxel.COLOR_DARK_BLUE)
                pyxel.text(52, 130, f"Do adversario era: {adversario_mao_formatada}", pyxel.COLOR_RED)
                pyxel.text(52, 150, f"Sua jogada: {jogada_atual}", pyxel.COLOR_DARK_BLUE)
                pyxel.text(52, 160, f"Jogada do adversario: {jogada_adversario}", pyxel.COLOR_RED)

            else:  # Derrota
                pyxel.blt(48, 80, 1, p_perdeu[0], p_perdeu[1], p_perdeu[2], p_perdeu[3])
                pyxel.text(52, 120, f"Sua mao era: {jogador_mao_formatada}", pyxel.COLOR_DARK_BLUE)
                pyxel.text(52, 130, f"Do adversario era: {adversario_mao_formatada}", pyxel.COLOR_RED)
                pyxel.text(52, 150, f"Sua jogada: {jogada_atual}", pyxel.COLOR_DARK_BLUE)
                pyxel.text(52, 160, f"Jogada do adversario: {jogada_adversario}", pyxel.COLOR_RED)

Poker()
