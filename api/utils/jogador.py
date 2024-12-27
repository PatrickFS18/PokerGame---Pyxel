
class Jogador:
    def __init__(self, id):
        self.mao = []
        self.jogada = 1
        self.sala_selecionada = None
        self.id = id
    
    def to_dict(self):
        return {
            'id': self.id,
            'mao': [carta.to_dict() for carta in self.mao],
            'jogada': self.jogada,
            'sala_selecionada': self.sala_selecionada
        }
    
    def __repr__(self):
        return repr(self.to_dict())
