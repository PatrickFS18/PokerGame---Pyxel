class Carta:
    def __init__(self, dictCard):
        self.dictCard = dictCard
        self.valor = dictCard['valor']
        self.naipe = dictCard['naipe']
    
    def to_dict(self):
        return {
            'valor': self.valor,
            'naipe': self.naipe
        }
    
    def __repr__(self):
        return repr(self.to_dict())
