import socketio

# Inicializando o servidor SocketIO
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:4000", "*"])

# Dicionário para armazenar as salas e os jogadores
salas = {}

MAX_JOGADORES = 2  # Definindo o limite de jogadores por sala

@sio.event
def connect(sid, environ, auth):
    print(f"Jogador {sid} conectado!")

@sio.event
def criar_sala(sid):
    # Verifica se o jogador já está em alguma sala
    for jogadores in salas.values():
        if sid in jogadores:
            sio.emit('erro_criacao_sala', {'mensagem': 'Você já está em uma sala!'}, room=sid)
            return  # Não permite criar nova sala se o jogador já estiver em uma

    # Cria uma sala se possível
    sala_id = len(salas) + 1  # Gerar um novo ID de sala
    salas[sala_id] = [sid]  # Adiciona o jogador à sala
    sio.enter_room(sid, str(sala_id))  # O jogador entra na sala

    # Emitir a atualização para todos os clientes sobre as salas e jogadores
    listar_salas(sid)

    sio.emit('sala_criada', {'sala_id': sala_id, 'status': 'criada'}, room=sid)

@sio.event
def ingressar_sala(sid, sala_id):
    if sala_id in salas and len(salas[sala_id]) < MAX_JOGADORES:
        salas[sala_id].append(sid)  # Adiciona o jogador à sala
        sio.enter_room(sid, str(sala_id))  # O jogador entra na sala

        # Emitir a atualização para todos os clientes sobre as salas e jogadores
        listar_salas(sid)

        sio.emit('sala_ingressada', {'sala_id': sala_id, 'status': 'ingressado'}, room=sid)
    else:
        sio.emit('erro_sala', {'mensagem': 'Sala cheia ou inexistente'}, room=sid)

@sio.event
def listar_salas(sid):
    # Emite as salas e os jogadores para todos os clientes
    salas_info = {}
    for sala_id, jogadores in salas.items():
        salas_info[sala_id] = jogadores
    sio.emit('salas_disponiveis', salas_info)  # Envia as informações das salas para todos os clientes
    
@sio.event
def disconnect(sid):
    # Quando um jogador desconectar, removemos ele das salas
    for sala_id, jogadores in salas.items():
        if sid in jogadores:
            jogadores.remove(sid)
            if len(jogadores) == 0:  # Se a sala estiver vazia, podemos removê-la
                del salas[sala_id]
            break

    # Emitir a atualização para todos os clientes sobre as salas e jogadores
    listar_salas(sid)

# Inicia o servidor WSGI
if __name__ == '__main__':
    import eventlet
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4000)), app)
