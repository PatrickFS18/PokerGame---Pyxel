import pyxel
import socketio
class ServidorSocket:
    def __init__(self):
        self.sio = socketio.Client()
        self.salas_disponiveis = {}
        self.sala_selecionada = None

        # Registrando eventos
        self.sio.on('connect', self.on_connect)
        self.sio.on('sala_criada', self.on_sala_criada)
        self.sio.on('erro_sala', self.on_erro_sala)
        self.sio.on('salas_disponiveis', self.on_salas_disponiveis)  # Novo evento
        self.sio.connect('http://localhost:4000')
    
    def on_connect(self):
        print("Conectado ao servidor!")
        self.listar_salas()

    def on_sala_criada(self, data):
        if data['status'] == 'criada':
            print(f"Sala {data['sala_id']} criada com sucesso!")
            self.sala_selecionada = data['sala_id']

    def on_erro_sala(self, data):
        # Exibe uma mensagem de erro ao tentar criar uma sala
        print(f"Erro: {data['mensagem']}")
        # Aqui você pode adicionar alguma forma de exibir a mensagem para o jogador no Pyxel
        # Exemplo simples:
        pyxel.text(10, 80, f"Erro: {data['mensagem']}", pyxel.COLOR_RED)

    def on_salas_disponiveis(self, salas):
        # Atualiza a lista de salas disponíveis no cliente
        self.salas_disponiveis = salas
        print(f"Salas disponíveis: {self.salas_disponiveis}")

    def listar_salas(self):
        # Solicitar salas disponíveis
        self.sio.emit('listar_salas')

    def criar_sala(self):
        self.sio.emit('criar_sala')

    def ingressar_sala(self, sala_id):
        self.sio.emit('ingressar_sala', sala_id)
