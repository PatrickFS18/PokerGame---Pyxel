from collections import Counter
class Compare:
    def __init__(self, player_hand, dealer_hand):
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.hand = []
        self.common_naipe = None
        self.victory = [0] # Util para verificar a mao mais forte do jogador
        self.highest_hand_value = [[],[],[],[],[],[],[],[],[],[]] # Útil para ver qual é a mão mais forte para casos de mesma vitória
        self.high_card = 0
        self.jogada = None
        
    def game (self):
        for i in range(len(self.dealer_hand)):
            self.hand.append(self.dealer_hand[i])
        for i in range(len(self.player_hand)):
            self.hand.append(self.player_hand[i])
        print('player',self.hand)
        # print('dealer ',self.dealer_hand)
        # print('mao ',self.hand)
        
    def determinar_jogada(self):
        victory_to_text = {
            9: "Royal Flush",
            8: "Straight Flush",
            7: "Four of a Kind",
            6: "Full House",
            5: "Flush",
            4: "Straight",
            3: "Three of a Kind",
            2: "Two Pairs",
            1: "One Pair",
            0: "High Card"
        }
        melhor_jogada = max(self.victory)        
        self.jogada = victory_to_text[melhor_jogada]

    def maior_valor_cartas(self,hand):
                    maior_valor = -1  # Inicializa com um valor pequeno
                    for jogada in hand:
                        for dicionario in jogada:
                            for carta in dicionario.keys():
                                if carta > maior_valor:
                                    maior_valor = carta
                    return maior_valor
                
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
            print('COMMONNNN NAIPPEEEE ',self.common_naipe)
           
    def verify_straight(self, hand):
        sequencia = 1
        # Obter os valores das cartas
        valores = sorted([carta.valor for carta in hand])

        for i in range(1, len(valores)):
            if valores[i] == valores[i - 1] + 1:
                sequencia += 1
                if sequencia == 5:
                    return True  # Straight encontrado
            else:
                sequencia = 1

        # Caso especial A-2-3-4-5
        if set([1, 2, 3, 4, 5]).issubset(set(valores)):
            return True

        return False

    def flush(self):
        self.order_cards(2)
        if self.common_naipe >= 5:
            # Filtrar cartas pelo naipe comum
            filtered_hand = [carta for carta in self.hand if carta.naipe == self.common_naipe]
            # Ordenar as cartas do mesmo naipe por valor em ordem decrescente
            filtered_hand = sorted(filtered_hand, key=lambda carta: carta.valor, reverse=True)

            valores = [carta.valor for carta in filtered_hand]

            # Royal Flush (A-10-J-Q-K)
            if set([1, 10, 11, 12, 13]).issubset(set(valores)):
                self.victory.append(9)
            elif self.verify_straight(filtered_hand):  # Straight Flush
                self.victory.append(8)
                for carta in filtered_hand[:5]:  # Adicionar as 5 cartas do Straight Flush
                    self.highest_hand_value[8].append(carta.valor)
            else:  # Flush simples
                self.victory.append(5)
                for carta in filtered_hand[:5]:  # Adicionar as 5 cartas do Flush
                    self.highest_hand_value[5].append(carta.valor)

    def straight(self):
        hand = self.order_cards(1)
        if self.verify_straight(hand):  # Straight
            self.victory.append(4)
            for carta in hand[:5]:  # Adicionar as 5 cartas do Straight
                self.highest_hand_value[4].append(carta.valor)
            
    def high_cards(self):
        # Adicionar carta mais alta
        self.victory.append(0)  # High Card
        highest_card = 0
        for i in self.hand:
            if i.valor > highest_card:
                highest_card = i.valor
        self.high_card = highest_card     
           
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
        if len(resultado['Pares']) > 0:
            quantityPairs = len(resultado['Pares'])
            
            # 3 casos: 1 par, 2 pares ou mais de 2 pares
            print('quantity pairs: ', quantityPairs)
            
            if quantityPairs == 1:
                self.victory.append(1)
                print('Um par: ', resultado['Pares'])
                self.highest_hand_value[1].append(resultado['Pares'])  # Adiciona o valor das cartas
            
            elif quantityPairs == 2:
                self.victory.append(2)
                print('Dois pares: ', resultado['Pares'])
                self.highest_hand_value[2].append(resultado['Pares'])  # Adiciona o valor das cartas
            
            else:  # Mais de 2 pares
                self.victory.append(2)
                
                # Ordena os pares em ordem decrescente de valor
                pares_ordenados = dict(sorted(resultado['Pares'].items(), reverse=True))
                print('Pares ordenados: ', pares_ordenados)
                
                # Seleciona apenas os dois maiores pares
                maiores_pares = dict(list(pares_ordenados.items())[:2])
                print('Dois maiores pares selecionados: ', maiores_pares)
                
                self.highest_hand_value[2].append(maiores_pares)  # Adiciona os dois maiores pares

                    
        if len(resultado['Triplas']) > 0:
            triplas = resultado['Triplas']
            
            if len(resultado['Triplas']) > 1:
                print("Antes de remover:", triplas)

                # Encontrar a menor chave
                menor_chave = min(triplas)

                # Remover a chave do dicionário
                del triplas[menor_chave]
                
            self.victory.append(3)
            self.highest_hand_value[3].append(triplas)  # Adiciona o valor das cartas

            print('Triplas: ',resultado['Triplas'])
            
        if len(resultado['Quadruplas']) > 0:
            self.victory.append(7)
            quadruplas = resultado['Quadruplas']
            self.highest_hand_value[7].append(quadruplas)  # Adiciona o valor das cartas

            print('Quadruplas: ',resultado['Quadruplas'])
            
        if resultado['Triplas'] and resultado['Pares']:
            self.victory.append(6)  # Full House
            trinca = max(resultado['Triplas'].keys())  # Maior valor da trinca
            par = max(resultado['Pares'].keys())  # Maior valor do par
            self.highest_hand_value[6] = [trinca, par]
            print(f"Full House: Trinca {trinca} e Par {par}")
            return  # Retorna pois o Full House é mais forte que trincas ou pares isolados
            
            #paramos na  implementacao dos tres tips de flushs nessa def
            