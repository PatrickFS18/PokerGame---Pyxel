import pyxel
from jogador import Jogador
from baralho import Baralho
from collections import Counter
from compare import Compare

class Poker:
    def __init__(self):
       #backend
        self.selected_option = -1 # -1 = não selecionado, 0 = jogo local, 1 = jogo online
        self.state = "menu"  # Estado inicial do jogo       
        self.jogador = Jogador()
        self.adversario = Jogador()
        self.dealer = Jogador()
        self.baralho = Baralho()
        self.is_initialized = False
        self.verify = True
        self.compare = None

        self.position_cards = [ #(local x,local y, width, height, topox, topoy, centrox, centroy)
                                (30,  38, 36, 52, 33, 41, 41, 60), # posição da carta 1
                                ( 70,  38, 36, 52, 73, 41, 81, 60), # posição da carta 2
                                ( 110,  38, 36, 52, 113, 41, 121, 60), # posição da carta 3
                                ( 150,  38, 36, 52, 153, 41, 161, 60), # posição da carta 4
                                ( 190,  38, 36, 52, 193, 41, 201, 60), # posição da carta 5
                                ( 14,  126, 36, 52, 17, 129, 25, 148), # posição da carta 6
                                ( 54,  126, 36, 52, 57, 129, 65, 148) # posição da carta 7
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
                            "13" : ( 113,  208, 7, 15)    
                        }   
        
        #frontend
        pyxel.init(256,192, title= "Poker Game")
        pyxel.mouse(True)
        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y

        # Detecta se o cursor está sobre uma das opções
        pyxel.load("my_resource.pyxres")
        pyxel.images[0]
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
        print("jogador = ", self.jogador.mao)
        print("dealer = ", self.dealer.mao)
        
        

    def orderByValueAndNaipe(self,cards):
        
        # Ordem dos naipes (Paus, Ouro, Espada, Copas)
        order_naipes = {'Paus': 0, 'Ouro': 1, 'Espada': 2, 'Copas': 3}
        
        # Ordena a mão,  primeiro pelo naipe e depois pelo valor

        cards = cards.sort(key = lambda carta: (order_naipes[carta.naipe], carta.valor))
        print("cards ", cards)
        return cards
        
    def verifyLogic(self, dealer, jogador):
        self.compare = Compare(self.jogador.mao, self.dealer.mao)
        self.compare.game()
        self.compare.countEqualValues() 
        self.verify = False
                
        #self.compare.flush()
        self.compare.countEqualValues()
        #self.orderByValueAndNaipe(mao)
        #self.countEqualValues(mao)
        
 
    def update(self):

        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y

        if self.state == "menu":
            self.update_menu()

        elif self.state == "local":
            self.initializedGame()
            self.update_local()
            

        elif self.state == "online":
            self.update_online()

        elif self.state == "winner":
            self.update_winner()



    def update_menu(self):
        local_game_button = (98, 50, 158, 70)  # (x1, y1, x2, y2) para Jogo Local
        online_game_button = (98, 80, 158, 100)  # (x1, y1, x2, y2) para Jogo Online
        rect_exit = (98, 110, 158, 130)  # Sair do Jogo

        if local_game_button[0] <= self.mx <= local_game_button[2] and local_game_button[1] <= self.my <= local_game_button[3]:
            self.selected_option = 0
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.state = "local"
                self.selected_option = -1
                print("Iniciando Jogo Local")

        elif online_game_button[0] <= self.mx <= online_game_button[2] and online_game_button[1] <= self.my <= online_game_button[3]:
            self.selected_option = 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.state = "online"
                self.selected_option = -1
                print("Iniciando Jogo Online")

        elif rect_exit[0] <= self.mx <= rect_exit[2] and rect_exit[1] <= self.my <= rect_exit[3]:
            self.selected_option = 2
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.quit()  # Sai do jogo

        else:
            self.selected_option = -1  # Nenhuma opção está selecionada

    def update_local(self):
        back_button = (243,3, 253, 13)  # (x1, y1, x2, y2) para voltar para o menu
        if back_button[0] <= self.mx <= back_button[2] and back_button[1] <= self.my <= back_button[3]:
            self.selected_option = 0
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.state = "menu"  
        else:
            self.selected_option == -1

    def update_online(self):
        pass
    def update_winner(self):
        pass

    def draw(self):
        pyxel.cls(0)
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "local":
            self.draw_local()
        elif self.state == "online":
            self.draw_online()    
        elif self.state == "winner":
            self.draw_winner()

    def draw_menu(self):
        # Título do Jogo
        pyxel.text(102, 20, "Poker Game", pyxel.frame_count %16)

        # Opção Jogo Local
        color_local = 11 if self.selected_option == 0 else 7
        pyxel.rect(98, 50, 60, 20, color_local)
        pyxel.text(110, 57, "Jogo Local", 0)

        # Opção Jogo Online
        color_online = 11 if self.selected_option == 1 else 7
        pyxel.rect(98, 80, 60, 20, color_online)
        pyxel.text(110, 87, "Jogo Online", 0)

        color_exit = 8 if self.selected_option == 2 else 7
        pyxel.rect(98, 110, 60, 20, color_exit)
        pyxel.text(118, 117, "Sair", 0)

    def draw_local(self):
        pyxel.blt(0, 0, 0, 0, 0, 256, 192)

        for i in range(len(self.dealer.mao)):
            p_valor = self.position_itens[f'{self.dealer.mao[i].valor}']
            p_naipe = self.position_itens[self.dealer.mao[i].naipe]
            p_carta = self.position_cards[i]
            #(local x,local y, width, height, topox, topoy, centrox, centroy)
            
            #(x plot, y plot, imagem, x imagem, y imagem, comprimento, altura)

            #carta
            pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens['Carta'][0], self.position_itens['Carta'][1], 36, 52)
            #numero topo
            pyxel.blt(p_carta[4], p_carta[5], 0, p_valor[0], p_valor[1], p_valor[2], p_valor[3])
            #naipe centro
            pyxel.blt(p_carta[6], p_carta[7], 0, p_naipe[0], p_naipe[1], p_naipe[2], p_naipe[3])
           
        for i in range(len(self.jogador.mao)):
            p_valor = self.position_itens[f'{self.jogador.mao[i].valor}']
            p_naipe = self.position_itens[self.jogador.mao[i].naipe]
            p_carta = self.position_cards[i+5]
            #(local x,local y, width, height, topox, topoy, centrox, centroy)
            
            #(x plot, y plot, imagem, x imagem, y imagem, comprimento, altura)

            #carta
            pyxel.blt(p_carta[0], p_carta[1], 0, self.position_itens['Carta'][0], self.position_itens['Carta'][1], 36, 52)
            #numero topo
            pyxel.blt(p_carta[4], p_carta[5], 0, p_valor[0], p_valor[1], p_valor[2], p_valor[3])
            #naipe centro
            pyxel.blt(p_carta[6], p_carta[7], 0, p_naipe[0], p_naipe[1], p_naipe[2], p_naipe[3])
           
                 
        
        color_Back = 8 if self.selected_option == 0 else 7
        pyxel.rect(243,3, 10, 10, color_Back)
        pyxel.text(246, 6, "X", 0)


    def draw_online(self):
        pass
    def draw_winner(self):
        pass

Poker()