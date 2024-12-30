import pyxel
import socketio
class ServidorSocket:
    def __init__(self):
        self.sio = socketio.Client()
        self.salas_disponiveis = {}
        self.sala_selecionada = None
        # Registrando eventos
        self.sala_atual_info = None
        self.id_player = None
        self.winner = None
        self.sid = None
        self.desistir = False
        self.atualizar_sala = None
        self.sio.on('connect', self.on_connect)
        self.sio.on('sala_criada', self.on_sala_criada)
        self.sio.on('erro_sala', self.on_erro_sala)
        self.sio.on('salas_disponiveis', self.on_salas_disponiveis)  # Novo evento
        self.sio.on('sid',self.my_sid)
        self.sio.on('nova_rodada', self.handle_nova_rodada)
        
        self.sio.on('init_game',self.init_game)
        self.sio.on('vencedor', self.vencedor)


        self.sio.connect('http://localhost:4000')


    def init_game(self, data):
        print("recebemos dados! init game executada,: ", data)

        sala_id = data['sala_id']
        jogadores_data = data['jogadores']
        dealer_data = data['dealer']

        # Encontrar a sala correspondente
        for sala in self.salas_disponiveis:
            if sala['sala_id'] == sala_id:
                # Certifique-se de que a entrada para o dealer existe
                if 'dealer' not in sala:
                    sala['dealer'] = {}

                # Atribuir as mãos aos jogadores
                for jogador_info in jogadores_data:
                    jogador = next((j for j in sala['jogadores'] if j['id'] == jogador_info['id']), None)
                    if jogador:
                        jogador['mao'] = jogador_info['mao']  # Atribuir diretamente a lista de dicionários

                # Atribuir a mão ao dealer
                sala['dealer']['mao'] = dealer_data  # Atribuir diretamente a lista de dicionários

                break

    def vencedor(self,data):
        self.winner = data["vencedor"]
        print('temos um vencedor! ',self.winner)
        
    def chamar_nova_rodada(self, sala_id, id_player):
        # Cliente envia pedido para o servidor iniciar nova rodada
        self.sio.emit('nova_rodada', {'sala_id': sala_id, 'id_player': id_player})
        print(f"Nova rodada solicitada para a sala {sala_id} pelo jogador {id_player}")

    def handle_nova_rodada(self, data):
        # Salvar as informações recebidas na resposta do servidor
        self.sala_atual_info = data  # Atualiza os dados da sala localmente
        print("Recebemos dados atualizados da rodada:")
        
    def on_connect(self):
        print("Conectado ao servidor!")
        self.sio.emit('salas_disponiveis')  # Envia uma solicitação para o servidor listar salas


    def on_salas_disponiveis(self, data):
        #print("Evento 'salas_disponiveis' recebido")
        #print(f"Salas disponíveis recebidas: {data['salas']}")
        self.salas_disponiveis = data["salas"]
        #print(f"Salas disponíveis: {self.salas_disponiveis}")
        self.atualizar_sala = True
        

    # def my_id(self, data):
    #     self.id_player= data['player_id']
    #     print('idddd ',self.id_player)
        
    def my_sid(self, data):
        
        self.sid= data['sid']
        self.id_player = data['player_id']
        
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



    def criar_sala(self):
        self.sio.emit('criar_sala')

    def ingressar_sala(self, sala_id):
        # Verifica se a sala existe e se o jogador não está em nenhuma sala
        if self.id_player is not None:
            jogador_em_sala = False
            quant_jogadores = 0
            sala_encontrada = False
            sala_definida = None
            c = -1
            for sala in self.salas_disponiveis:
                c = c + 1
                if(sala["sala_id"] == sala_id):
                    sala_encontrada = True
                    sala_definida = c
                    print(sala["jogadores"])
                    quant_jogadores = len(sala["jogadores"])
                    
                if (self.id_player in sala["jogadores"]):
                    jogador_em_sala = True
            
            # Verifica se a sala está disponível e o jogador não está nela
            if (sala_encontrada == True) and (quant_jogadores < 2) and (self.sid is not None) and (jogador_em_sala == False):
                print(f'Executando função para entrar na sala {sala_id}')
                # Emite o evento para o servidor ingressar na sala
                self.sio.emit('ingressar_sala',sala_id)
                
                # Marca que o jogador está na sala
                self.salas_disponiveis[sala_definida]["jogadores"].append(self.id_player)
                
                print(f'O jogador {self.id_player} entrou na sala {sala_id}')
            else:
                print(f'O jogador {self.id_player} já está na sala {sala_id} ou a sala está cheia, ou não existe.')
        else:
            print('ID do jogador não definido ou o jogador não está logado.')
            
            




