class Carta:
    def __init__(self,dictCard):
        self.valor = dictCard['value']
        self.naipe = dictCard['naipe']

    def __str__(self):
        return f"{self.valor} de {self.naipe}"


