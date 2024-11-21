from collections import Counter
class Compare:
    def __init__(self, player_hand, dealer_hand):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.hand = []
        self.common_naipe = None

    def game (self):
        for i in range(len(self.dealer_hand)):
            self.hand.append(self.dealer_hand[i])
        for i in range(len(self.player_hand)):
            self.hand.append(self.player_hand[i])
    
    def order_cards (self, case):
        # Ordem dos naipes (Paus, Ouro, Espada, Copas)
        order_naipes = {'Paus': 0, 'Ouro': 1, 'Espada': 2, 'Copas': 3}
        
        # Ordena a mão, primeiro pelo naipe e depois pelo valor
        if case == 1:
            self.hand.sort(key = lambda carta: ( carta.valor))
        if case == 2:
            self.hand.sort(key = lambda carta: (order_naipes[carta.naipe], carta.valor))
            carta_naipe = [carta["naipe"] for carta in self.hand]
            contador =  counter(carta_naipe)
            self.common_naipe = contador.most_common(1)[0]
       

    def flush(self):
        if self.common_naipe[1] == 5:
            #paramos na  implementacao dos tres tips de flushs nessa def
            pass
    def high_card(self):
        pass
