from utils.jogador import Jogador
from utils.baralho import Baralho
from utils.carta import Carta

class InitGame:
    def __init__(self):
        self.baralhos = []
        
    def init_game(self, sala_id):
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
         
        # Lista para armazenar os objetos Jogador 
        jogadores = [] 
        dealer = Jogador('dealer')
        
        for player_id in sala:
            jogador = Jogador(player_id)

            # Distribuir 2 cartas únicas para o jogador
            for _ in range(2):
                # Verificar se ainda há cartas no baralho
                if baralho:  
                    carta_info = baralho.pop(0)
                    jogador.mao.append(carta_info if isinstance(carta_info, Carta) else Carta(carta_info))
            
            jogadores.append(jogador)  
        
        # Distribuir 5 cartas para o dealer
        for _ in range(5):
            if baralho:
                carta_info = baralho.pop(0)
                dealer.mao.append(carta_info if isinstance(carta_info, Carta) else Carta(carta_info))

        return jogadores, dealer  # Retorna a lista de jogadores e o dealer
