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
            #print(self.hand)
            carta_naipe = [carta.naipe for carta in self.hand]
            contador =  Counter(carta_naipe)
            self.common_naipe = contador.most_common(1)[0]
           
    def verify_straight(self,hand):
        sequencia = 1
        #print(hand)
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
        hand = self.order_cards(1)
        straight = self.verify_straight(hand) 
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
        
        #print('Count Equal Values ',resultado)
        if (len(resultado['Pares']) > 0):
            quantityPairs = len(resultado['Pares'])
            
            # 3 casos: se tiver 1 par: victory = 1
            # se tiver 2 pares victory = 2
            # se tiver +2 pares, verificar qual a dupla de pares maior e victory = 2
            print('quantity pairs: ',quantityPairs)
            if(quantityPairs == 1):
                self.victory.append(1)
                print('Um par: ',resultado['Pares'])
            elif(quantityPairs == 2):
                self.victory.append(2)
                print('Dois pares: ',resultado['Pares'])

            else:
                self.victory.append(2)
                pares = resultado['Pares']

                # Ordenar o dicionário pelas chaves de forma crescente
                pares_ordenados = dict(sorted(pares.items()))

                # Remover o número (chave) de menor valor
                menor_chave = min(pares_ordenados)
                print('antes de remover os pares: ',pares)
                del pares_ordenados[menor_chave]


                # Verificar se o valor da chave de maior valor é 2, pois é o caso de seus 2 pares serem com a maior carta
                if max(pares_ordenados.values()) == 2:
                    # Se for 2, manter apenas a chave com o maior valor
                    maior_valor = max(pares_ordenados, key=pares_ordenados.get)
                    pares_ordenados = {maior_valor: pares_ordenados[maior_valor]}             
                print('depois de remover os pares: ',pares_ordenados)
                
        if len(resultado['Triplas']) > 0:
            if len(resultado['Triplas']) > 1:
                triplas = resultado['Triplas']
                print("Antes de remover:", triplas)
                
                # Verificar as chaves com valor 3 (as triplas)
                triplas_com_valor_3 = [k for k, v in triplas.items() if v == 3]
                
                # Se houver exatamente duas triplas, remover a tripla com o menor valor
                if len(triplas_com_valor_3) == 2:
                    chave_menor = min(triplas_com_valor_3)
                    del triplas[chave_menor]
            self.victory.append(3)
            print('Triplas: ',resultado['Triplas'])
            
        if len(resultado['Quadruplas']) > 0:
            self.victory.append(7)
            print('Quadras: ',resultado['Quadras'])

            #paramos na  implementacao dos tres tips de flushs nessa def
            