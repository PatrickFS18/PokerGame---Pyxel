import pyxel
import socketio
class ServidorSocket:
    def __init__(self):
        self.sio = socketio.Client()
        self.salas_disponiveis = {}
        self.sala_selecionada = None
        # Registrando eventos
        self.id_player = None
        self.sid = None
        self.sio.on('connect', self.on_connect)
        self.sio.on('sala_criada', self.on_sala_criada)
        self.sio.on('erro_sala', self.on_erro_sala)
        self.sio.on('salas_disponiveis', self.on_salas_disponiveis)  # Novo evento
        self.sio.on('sid',self.my_sid)

        self.sio.connect('http://localhost:4000')
       
        
    def on_connect(self):
        print("Conectado ao servidor!")
        self.listar_salas()

    # def my_id(self, data):
    #     self.id_player= data['player_id']
    #     print('idddd ',self.id_player)
        
    def my_sid(self, data):
        
        self.sid= data['sid']
        self.id_player = data['player_id']
        
        print('sidddd ',self.sid)
        print('iddd ',self.id_player)
        
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
        # Verifica se a sala existe e se o jogador não está em nenhuma sala
        print('ingressando na sala linha 59')
        if self.id_player is not None:
            print('ingressando na sala linha 61')

            # Verifica se a sala está disponível e o jogador não está nela
            if (sala_id in self.salas_disponiveis) and (len(self.salas_disponiveis[sala_id]) < 2) and (self.sid is not None) and (self.id_player not in self.salas_disponiveis[sala_id]):
                print(f'Executando função para entrar na sala {sala_id}')
                print(f'Salas disponíveis: {self.salas_disponiveis[sala_id]}')
                # Emite o evento para o servidor ingressar na sala
                self.sio.emit('ingressar_sala',sala_id)
                
                # Marca que o jogador está na sala
                self.salas_disponiveis[sala_id].append(self.id_player)
                
                print(f'O jogador {self.id_player} entrou na sala {sala_id}')
            else:
                print(f'O jogador {self.id_player} já está na sala {sala_id} ou a sala está cheia, ou não existe.')
        else:
            print('ID do jogador não definido ou o jogador não está logado.')
            