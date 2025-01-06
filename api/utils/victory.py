from utils.compare import Compare

class Victory:
    def __init__(self):
        self.winner = None
        self.jogadas = None
        pass    
    
    def verifyLogic(self, dealer, jogador, adversario):
        
        self.compare_1 = Compare(jogador.mao, dealer["mao"])
        self.compare_1.game()
        self.compare_1.high_cards()
        
        self.compare_1.countEqualValues()
        self.compare_1.determinar_jogada()
        jogada_player_1 = self.compare_1.jogada 
        
        self.compare_2 = Compare(adversario.mao, dealer["mao"])
        self.compare_2.game()
        self.compare_2.high_cards()
        self.compare_2.countEqualValues()
        
        self.compare_2.determinar_jogada()
        jogada_player_2 = self.compare_2.jogada
        
        player_1_victory = max(self.compare_1.victory)
        player_2_victory = max(self.compare_2.victory)
        
        # Na posição 0 o jogador 1,  na posição 1 o jogador 2
        
        self.jogadas = [{jogador.id:jogada_player_1},{adversario.id:jogada_player_2}]

        if(player_1_victory == player_2_victory) and (player_1_victory != 0 and player_2_victory != 0):
            mao_jogador_1 = self.compare_1.highest_hand_value
            mao_jogador_2 = self.compare_2.highest_hand_value
            # Verificação de empate
            maior_carta_1 = self.compare_1.maior_valor_cartas(mao_jogador_1)
            maior_carta_2 = self.compare_2.maior_valor_cartas(mao_jogador_2)
            print(maior_carta_1)
            print(maior_carta_2)
            # Função para encontrar o maior valor de carta em uma mão
            if maior_carta_1 > maior_carta_2:
                print(f"Jogador {jogador.id} vence pelo desempate! Carta mais alta: {maior_carta_1}")
            elif maior_carta_2 > maior_carta_1:
                print(f"Jogador {adversario.id} vence pelo desempate! Carta mais alta: {maior_carta_2}")
            else:
                print(f"Empate absoluto! Ambos têm a mesma carta mais alta: {maior_carta_1}")
                self.winner = 0
                
        if(player_1_victory == player_2_victory and (player_1_victory == 0 and player_2_victory == 0)):
            if(self.compare_1.high_card > self.compare_2.high_card):
                self.winner = jogador.id
                print(f'Jogador {jogador.id} venceu por carta alta. O valor da carta: ',self.compare_1.high_card)

            elif(self.compare_1.high_card < self.compare_2.high_card):
                self.winner = adversario.id
                print(f'Jogador {adversario.id} venceu por carta alta. O valor da carta: ',self.compare_2.high_card)
            elif(self.compare_1.high_card == self.compare_2.high_card):
                self.winner = 0
                print('Empate com carta alta! Mesmo valor: ',self.compare_1.high_card)

        # Comparação para determinar o vencedor  
        elif(player_1_victory > player_2_victory):
            self.winner = jogador.id
            print(f'Jogador {jogador.id} venceu.')
        else:
            self.winner = adversario.id
            print(f'Jogador {adversario.id} venceu')
