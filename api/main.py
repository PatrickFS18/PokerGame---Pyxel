import socketio

from api.utils.initGame import InitGame
# Inicializando o servidor SocketIO
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:4000", "*"])

# Dicionário para armazenar as salas e os jogadores
salas = {}

MAX_JOGADORES = 2  # Limite de jogadores por sala
player_id_counter = 1
player_ids = {}



@sio.event
def connect(sid, environ, auth):
    global player_id_counter

    # Atribui o próximo ID disponível ao jogador
    player_ids[sid] = player_id_counter
    print('idddddddd ',player_ids)
    
    # Inicia o jogo
     
    player_id_counter += 1

    print(f"Jogador conectado: SID padrão {sid}, ID personalizado {player_ids[sid]}")

    # Envia o ID personalizado para o cliente
    sio.emit('sid', {'sid': sid, 'player_id': player_ids[sid]}, room=sid)



@sio.event
def criar_sala(sid):
    # Verifica se o jogador já está em alguma sala
    if player_ids.get(sid) is None:
        sio.emit('erro_criacao_sala', {'mensagem': 'Jogador não conectado corretamente!'}, room=sid)
        return

    for jogadores in salas.values():
        if player_ids[sid] in jogadores:  # Verifica se o ID do jogador já está em alguma sala
            sio.emit('erro_criacao_sala', {'mensagem': 'Você já está em uma sala!'}, room=sid)
            return

    # Cria uma nova sala
    sala_id = str(len(salas) + 1)  # Garantir que o ID da sala seja string
    salas[sala_id] = [player_ids[sid]]  # Adiciona o jogador à sala

    sio.enter_room(sid, sala_id)

    listar_salas(sid)

    sio.emit('sala_criada', {'sala_id': sala_id, 'status': 'criada'}, room=sid)
    
    
@sio.event
# Lógica de ingressar na sala, e iniciar partida caso atinga o máximo de jogadores
def ingressar_sala(sid, sala_id):
    sala_id = str(sala_id)  # Garantir consistência no tipo
    if sala_id in salas:
        if len(salas[sala_id]) < MAX_JOGADORES:
            salas[sala_id].append(player_ids[sid])  # Adiciona o jogador pela ID personalizada
            sio.enter_room(sid, sala_id)
            
            listar_salas(sid)

            sio.emit('sala_ingressada', {'sala_id': sala_id, 'status': 'ingressado'}, room=sid)
            
            if(len(salas[sala_id]) == MAX_JOGADORES):
                # A partida deve começar, e iniciar a distribuição de cartas
                instanciar_cartas = InitGame()
                
                # Gerar o baralho para esta sala
                instanciar_cartas.init_game(sala_id)
                
                #salas[sala_id] retorna: os id personalidados de cada player na sala
                 
                cartas = instanciar_cartas.get_baralho(sala_id)
                if (cartas is not None):
                    jogadores,dealer = instanciar_cartas.distribuir_cartas(salas[sala_id],cartas)
                
                    sio.emit('init_game', {'mensagem': 'A partida vai começar!','jogadores':jogadores,'dealer':dealer}, room=sid) # Retorna a lista de jogadores (instanciados na classe Jogador. Acessar jogador.mao)
        else:
            sio.emit('erro_sala', {'mensagem': 'Sala cheia!'}, room=sid)
    else:
        sio.emit('erro_sala', {'mensagem': 'Sala inexistente!'}, room=sid)



@sio.event
def listar_salas(sid):
    salas_info = {}
    print("Listando salas...")

    for sala_id, jogadores in salas.items():
        salas_info[sala_id] = []
        print(f"Sala {sala_id} tem os jogadores: {jogadores}")
        
        for jogador in jogadores:
            # Verifica se o jogador (SID) está no dicionário player_ids
            if jogador in player_ids.values():
                print(f"Jogador {jogador} encontrado, ID: {jogador}")
                salas_info[sala_id].append(jogador)  # Adiciona o ID personalizado
            else:
                print(f"Erro: player_id para SID {jogador} não encontrado em player_ids")
                salas_info[sala_id].append("Desconhecido")  # Ou outro valor para indicar erro

    print(f"Salas disponíveis: {salas_info}")
    sio.emit('salas_disponiveis', salas_info, room=sid or None)


@sio.event
def disconnect(sid):
    # Remove o jogador das salas e do mapeamento
    for sala_id, jogadores in list(salas.items()):
        if player_ids[sid] in jogadores:  # Verifica o ID do jogador
            jogadores.remove(player_ids[sid])  # Remove o jogador pela ID personalizada
            if not jogadores:
                del salas[sala_id]
            break

    # Remove o jogador de player_ids
    if sid in player_ids:
        del player_ids[sid]

    listar_salas(sid)

# Inicia o servidor WSGI
if __name__ == '__main__':
    import eventlet
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4000)), app)
