from collections import Counter
class Compare:
    def __init__(self, player_hand, dealer_hand):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.hand = []
        self.common_naipe = None
        self.victory = [0] # Util para verificar a mao mais forte do jogador
        self.highest_hand_value = [] # Útil para ver qual é a mão mais forte para casos de mesma vitória
    def game (self):
        for i in range(len(self.dealer_hand)):
            self.hand.append(self.dealer_hand[i])
        for i in range(len(self.player_hand)):
            self.hand.append(self.player_hand[i])
        print('player',self.hand)
        # print('dealer ',self.dealer_hand)
        # print('mao ',self.hand)
    def order_cards (self, case):
        # Ordem dos naipes (Paus, Ouro, Espada, Copas)
        order_naipes = {'Paus': 0, 'Ouro': 1, 'Espada': 2, 'Copas': 3}
        
        # Ordena a mão, primeiro pelo naipe e depois pelo valor
        if case == 1:
            self.hand.sort(key = lambda carta: (carta.valor))
           

        if case == 2:
            self.hand.sort(key = lambda carta: (order_naipes[carta.naipe], carta.valor))
            #self.hand = [{'valor': 7, 'naipe': 'Paus'}, {'valor': 9, 'naipe': 'Paus'}, {'valor': 10, 'naipe': 'Ouro'}, {'valor': 11, 'naipe': 'Ouro'}, {'valor': 12, 'naipe': 'Ouro'}, {'valor': 13, 'naipe': 'Ouro'}, {'valor': 14, 'naipe': 'Ouro'}]
            print(self.hand)
            carta_naipe = [carta.naipe for carta in self.hand]
            contador =  Counter(carta_naipe)
            self.common_naipe = contador.most_common(1)[0]
           
    def verify_straight(self,hand):
        sequencia = 1 
        for i in range(1, len(hand)):
            if hand.valor[i] == hand.valor[i - 1] + 1:
                sequencia += 1
                if sequencia == 5:
                    return True  # Straight flush
            else:
                sequencia = 1 
        
        # Verificar caso especial do Ás baixo (A-2-3-4-5)
        if set([14, 2, 3, 4, 5]).issubset(set(hand.valor)):
            return True
        return False 

    def flush(self):
        self.order_cards(2)
        if self.common_naipe >= 5:
            #filtrar hand ppelo common naipe
            hand = self.hand
            straight = self.verify_straight(hand)
            filtered_hand = list(filter(lambda carta: carta.naipe == self.common_naipe, hand))
            filtered_hand[::-1]

            if filtered_hand[0].valor == 14 and filtered_hand[1].valor == 13 and filtered_hand[2].valor == 12 and filtered_hand[3].valor == 11 and filtered_hand[4].valor == 10: #Royal Flush
                self.victory.append(9) 
            elif straight: # Straight Flush
                self.victory.append(8)
            else: #flush
                self.victory.append(5)
    def straight(self):
        self.order_cards(1)
        straight = self.verify_straight(self.hand) 
        if straight: # Straight
            self.victory.append(4)
            
    
    def countEqualValues(self):
        cards = self.hand
        valores = [card.valor for card in cards]  # Criando uma lista dos valores das cartas
        valores.sort()
        contagem = Counter(valores)  # Conta quantas vezes cada valor aparece

        resultado = {
            'Pares': {valor: count for valor, count in contagem.items() if count == 2},
            'Triplas': {valor: count for valor, count in contagem.items() if count == 3},
            'Quadruplas': {valor: count for valor, count in contagem.items() if count == 4}
        }
        
        print('Count Equal Values ',resultado)
        
            #paramos na  implementacao dos tres tips de flushs nessa def
            
    def high_card(self):
        pass
