from jogador import Jogador
from baralho import Baralho

class InitGame:
    def __init__(self):
        self.baralhos = []
        
    def init_game(self,sala_id):
        baralho = Baralho()
        baralho.gerarCartas()
        baralho.embaralharCartas()
        if not any(baralho_item['sala_id'] == sala_id for baralho_item in self.baralhos):
            self.baralhos.append({
                'sala_id': sala_id,
                'baralho': baralho.cartas
            })
    
    def get_baralho(self, id_sala):
        # Busca o baralho pelo id_sala
        for baralho_item in self.baralhos:
            if baralho_item['sala_id'] == id_sala:
                return baralho_item['baralho']
        return None

    def distribuir_cartas(self, sala, baralho):
        jogadores = []  # Lista para armazenar os objetos Jogador
        dealer = Jogador()
        for player_id in sala:
            jogador = Jogador()
            jogador.id = player_id

            # Distribuir 2 cartas únicas para o jogador
            for _ in range(2):  # 2 cartas por jogador
                if baralho:  # Verificar se ainda há cartas no baralho
                    jogador.mao.append(baralho.pop(0))  # Remover carta do topo do baralho
            
            jogadores.append(jogador)  # Adicionar o jogador à lista
        dealer.id = 'dealer'
        for _ in range(5):
            if baralho:
                dealer.mao.append(baralho.pop(0))

        return jogadores,dealer  # Retorna a lista de jogadores
                
    #         for i in range (0,5):
    #             self.dealer.mao.append(cartas[i])
    #             cartas.pop(0)