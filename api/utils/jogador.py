class Jogador:
    def __init__(self):
        self.mao = []
        self.jogada = 1
        self.sala_selecionada = None
        self.id = None
    
    def to_dict(self):
        return {
            'mao': self.mao,
            'jogada': self.jogada,
            'sala_selecionada': self.sala_selecionada,
            'id': self.id
        }

    def __str__(self):
        return str(self.to_dict())

