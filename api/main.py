import socketio

from utils.victory import Victory
from utils.initGame import InitGame
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
    salas_info = []
    for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
        salas_info.append({
            "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
            "jogadores": sala_info["jogadores"],
            "rodada": sala_info["rodada"],
        })
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes
    # Inicia o jogo
     
    player_id_counter += 1

    print(f"Jogador conectado: SID padrão {sid}, ID personalizado {player_ids[sid]}")

    # Envia o ID personalizado para o cliente
    sio.emit('sid', {'sid': sid, 'player_id': player_ids[sid]}, room=sid)

@sio.event
def criar_sala(sid):
    if player_ids.get(sid) is None:
        sio.emit('erro_criacao_sala', {'mensagem': 'Jogador não conectado corretamente!'}, room=sid)
        return

    # Verifica se o jogador já está em uma sala
    for sala in salas.values():
        if player_ids[sid] in sala["jogadores"]:
            sio.emit('erro_criacao_sala', {'mensagem': 'Você já está em uma sala!'}, room=sid)
            return

    # Criação da sala
    sala_id = str(len(salas) + 1)
    salas[sala_id] = {
        "sala_id": sala_id,
        "jogadores": [player_ids[sid]],
        "rodada": 0,
        "baralho": [],  # Inicialize outros atributos se necessário
    }

    # O jogador entra na sala
    sio.enter_room(sid, sala_id)

    # Emitir evento para o criador da sala (só ele recebe isso)
    sio.emit('sala_criada', {'sala_id': sala_id, 'status': 'criada'}, room=sid)

    # Emitir a lista de salas para todos os clientes
    salas_info = [{'sala_id': sala_id, 'jogadores': sala['jogadores'], 'rodada': sala['rodada']} for sala_id, sala in salas.items()]
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Envia para todos os clientes

@sio.event
# Lógica de ingressar na sala, e iniciar partida caso atinga o máximo de jogadores
def ingressar_sala(sid, sala_id):
    sala_id = str(sala_id)  # Garantir consistência no tipo
    if sala_id in salas:
        print(salas[sala_id])
        if len(salas[sala_id]["jogadores"]) < MAX_JOGADORES:
            salas[sala_id]["jogadores"].append(player_ids[sid])  # Adiciona o jogador pela ID personalizada
            sio.enter_room(sid, sala_id)
            
    
            salas_info = []
            for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
                salas_info.append({
                    "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
                    "jogadores": sala_info["jogadores"],
                    "rodada": sala_info["rodada"],
                })
            sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes

            sio.emit('sala_ingressada', {'sala_id': sala_id, 'status': 'ingressado'}, room=sid)
            
            if(len(salas[sala_id]["jogadores"]) == MAX_JOGADORES):
                print('vendo os jogadores na sala: ',salas[sala_id]["jogadores"])
                # A partida deve começar, e iniciar a distribuição de cartas
                instanciar_cartas = InitGame()
                sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes

                # Gerar o baralho para esta sala
                instanciar_cartas.init_game(sala_id)
                
                #salas[sala_id] retorna: os id personalidados de cada player na sala
                 
                cartas = instanciar_cartas.get_baralho(sala_id)
                if (cartas is not None):
                    
                   # Distribuir as cartas para os jogadores
                    # ... No seu código de evento
                    jogadores, dealer = instanciar_cartas.distribuir_cartas(salas[sala_id]["jogadores"], cartas)

                    # Converter a lista de jogadores para uma lista de dicionários
                    jogadores_dict = [jogador.to_dict() for jogador in jogadores]

                    # Converter as cartas do dealer para uma lista de dicionários
                    dealer_dict = [carta.to_dict() for carta in dealer.mao]

                    # Converter as cartas dos jogadores (caso necessário)
                    for jogador in jogadores_dict:
                        jogador['mao'] = [carta.to_dict() for carta in jogador['mao']]
                    print('jogadores dict: ',jogadores_dict)
                    print('dealer dict: ',dealer_dict)
                    # Emitir o evento com os jogadores e dealer convertidos
                    sio.emit('init_game', {
                        'sala_id':sala_id,
                        'mensagem': 'A partida vai começar!',
                        'jogadores': jogadores_dict,
                        'dealer': dealer_dict
                    }, room=sid)

        else:
            sio.emit('erro_sala', {'mensagem': 'Sala cheia!'}, room=sid)
    else:
        sio.emit('erro_sala', {'mensagem': 'Sala inexistente!'}, room=sid)

@sio.event
def rodadas(sid,sala_id):
    sala_id = str(sala_id)  # Garantir consistência no tipo
    if sala_id in salas:
        sala = salas[sala_id]
        if sala["rodada"] == 0:
            pass
        
        elif sala["rodada"] == 1:
            pass
        
        elif sala["rodada"] == 2:
            pass 
        
        elif sala["rodada"] == 3: # Verificar Vitória
            pass 
        
        elif sala["rodada"] != 3:
            victory = Victory()
            sala = salas[sala_id]
            
            for j in sala["Jogadores"]:
                print(j) 
            #victory.verifyLogic(dealer,jogador,adversario)
            sala["rodada"] += 1  # Avança para a próxima rodada
        
        sio.emit('nova_rodada', {'sala_id': sala_id, 'rodada': sala["rodada"]}, room=sala_id)
    else:
        sio.emit('erro', {'mensagem': 'Sala inexistente!'}, room=sid)
        
@sio.event
def salas_disponiveis(data):  # Adicione 'data' como parâmetro
    salas_info = []
    for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
        salas_info.append({
            "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
            "jogadores": sala_info["jogadores"],
            "rodada": sala_info["rodada"],
        })
    print('imprimindo as salas info: ', salas_info)
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Envia para todos


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
    
    salas_info = []
    for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
        salas_info.append({
            "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
            "jogadores": sala_info["jogadores"],
            "rodada": sala_info["rodada"],
        })
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes


# Inicia o servidor WSGI
if __name__ == '__main__':
    import eventlet
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4000)), app)
