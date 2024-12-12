import pyxel
from jogador import Jogador
from baralho import Baralho
from collections import Counter
from compare import Compare

class Poker:
    def __init__(self):
        #frontend
        pyxel.init(256,144, title= "Poker Game")
        pyxel.mouse(True)

        # Detecta se o cursor está sobre uma das opções
        pyxel.image(0).load(0, 0, "menu_background.png")  # Fundo do menu
        pyxel.image(1).load(0, 0, "game_background.png")  # Fundo do jogo
        self.mx = pyxel.mouse_x
        self.my = pyxel.mouse_y
        self.selected_option = -1 # -1 = não selecionado, 0 = jogo local, 1 = jogo online
        self.state = "menu"  # Estado inicial do jogo
        pyxel.run(self.update,self.draw)

        #backend
        self.jogador = Jogador()
        self.adversario = Jogador()
        self.dealer = Jogador()
        self.baralho = Baralho()
        self.is_initialized = False
        self.verify = True
        self.compare = None

        
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

            if(self.verify):#verifica uma vez a logica do jogo
                self.verifyLogic(self.dealer,self.jogador)
                self.state = "winner"
        
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
                self.state == "local"
                print("Iniciando Jogo Local")

        elif online_game_button[0] <= self.mx <= online_game_button[2] and online_game_button[1] <= self.my <= online_game_button[3]:
            self.selected_option = 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.state == "online"
                print("Iniciando Jogo Online")

        elif rect_exit[0] <= self.mx <= rect_exit[2] and rect_exit[1] <= self.my <= rect_exit[3]:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.quit()  # Sai do jogo

        else:
            self.selected_option = -1  # Nenhuma opção está selecionada

    def update_local(self):
        back_button = (230,15, 250, 35)  # (x1, y1, x2, y2) para voltar para o menu
        pass
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
        pyxel.text(102, 20, "Poker Game", pyxel.frame_count % 5)

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
        pass

    def draw_online(self):
        pass
    def draw_winner(self):
        pass

Poker()