import os
import socketio
from utils.jogador import Jogador
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
    print('idddddddd ', player_ids)
    salas_info = []
    for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
        salas_info.append({
            "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
            "jogadores": [j.to_dict() for j in sala_info["jogadores"]],
            "rodada": sala_info["rodada"],
        })
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes
    
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
        if player_ids[sid] in [j.id for j in sala["jogadores"]]:
            sio.emit('erro_criacao_sala', {'mensagem': 'Você já está em uma sala!'}, room=sid)
            return

    # Criação da sala
    sala_id = str(len(salas) + 1)
    jogador = Jogador(player_ids[sid])
    salas[sala_id] = {
        "sala_id": sala_id,
        "jogadores": [jogador],
        "rodada": 0,
        "baralho": [],  # Inicialize outros atributos se necessário
    }

    # O jogador entra na sala
    sio.enter_room(sid, sala_id)

    # Emitir evento para o criador da sala (só ele recebe isso)
    sio.emit('sala_criada', {'sala_id': sala_id, 'status': 'criada'}, room=sid)

    # Emitir a lista de salas para todos os clientes
    salas_info = [{'sala_id': sala_id, 'jogadores': [j.to_dict() for j in sala['jogadores']], 'rodada': sala['rodada']} for sala_id, sala in salas.items()]
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Envia para todos os clientes
@sio.event
def ingressar_sala(sid, sala_id):
    sala_id = str(sala_id)  # Garantir consistência no tipo
    if sala_id in salas:
        print(salas[sala_id])
        if len(salas[sala_id]["jogadores"]) < MAX_JOGADORES:
            jogador = Jogador(player_ids[sid])
            salas[sala_id]["jogadores"].append(jogador)  # Adiciona o jogador pela ID personalizada
            sio.enter_room(sid, sala_id)
            
            salas_info = []
            for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
                salas_info.append({
                    "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
                    "jogadores": [j.to_dict() for j in sala_info["jogadores"]],
                    "rodada": sala_info["rodada"],
                })
            sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes

            sio.emit('sala_ingressada', {'sala_id': sala_id, 'status': 'ingressado'}, room=sid)
            
            if len(salas[sala_id]["jogadores"]) == MAX_JOGADORES:
                print('vendo os jogadores na sala: ', [j.id for j in salas[sala_id]["jogadores"]])
                # A partida deve começar, e iniciar a distribuição de cartas
                instanciar_cartas = InitGame()
                sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes

                # Gerar o baralho para esta sala
                instanciar_cartas.init_game(sala_id)
                
                cartas = instanciar_cartas.get_baralho(sala_id)
                if cartas is not None:
                    # Distribuir as cartas para os jogadores
                    jogadores, dealer = instanciar_cartas.distribuir_cartas([j.id for j in salas[sala_id]["jogadores"]], cartas)

                    # Converter a lista de jogadores para uma lista de dicionários
                    jogadores_dict = [jogador.to_dict() for jogador in jogadores]

                    # Converter as cartas do dealer para uma lista de dicionários
                    dealer_dict = [carta.to_dict() for carta in dealer.mao]

                    # Emitir o evento com os jogadores e dealer convertidos
                    sio.emit('init_game', {
                        'sala_id': sala_id,
                        'mensagem': 'A partida vai começar!',
                        'jogadores': jogadores_dict,
                        'dealer': dealer_dict
                    }, room=sala_id)

        else:
            sio.emit('erro_sala', {'mensagem': 'Sala cheia!'}, room=sid)
    else:
        sio.emit('erro_sala', {'mensagem': 'Sala inexistente!'}, room=sid)

@sio.event
def rodadas(sid, sala_id):
    sala_id = str(sala_id)  # Garantir consistência no tipo
    if sala_id in salas:
        sala = salas[sala_id]
        if sala["rodada"] == 0:
            pass
        
        elif sala["rodada"] == 1:
            pass
        
        elif sala["rodada"] == 2:
            pass 
        
        elif sala["rodada"] == 3:  # Verificar Vitória
            pass  #teste
        
        elif sala["rodada"] != 3:
            victory = Victory()
            sala = salas[sala_id]
            
            for j in sala["jogadores"]:
                print(j) 
            #victory.verifyLogic(dealer, jogador, adversario)
            sala["rodada"] += 1  # Avança para a próxima rodada
        
        sio.emit('nova_rodada', {'sala_id': sala_id, 'rodada': sala["rodada"]}, room=sala_id)
    else:
        sio.emit('erro', {'mensagem': 'Sala inexistente!'}, room=sid)

@sio.event
def salas_disponiveis(data):
    salas_info = []
    for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
        salas_info.append({
            "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
            "jogadores": [j.to_dict() for j in sala_info["jogadores"]],
            "rodada": sala_info["rodada"],
        })
    print('imprimindo as salas info: ', salas_info)
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Envia para todos

@sio.event
def disconnect(sid):
    jogador_id = player_ids.get(sid)
    if jogador_id is None:
        return  # O jogador já foi desconectado ou não estava conectado

    # Remover o jogador da sala e do mapeamento
    sala_a_remover = None
    for sala_id, sala in list(salas.items()):
        if jogador_id in [j['id'] if isinstance(j, dict) else j.id for j in sala["jogadores"]]:
            sala["jogadores"] = [j for j in sala["jogadores"] if (j['id'] if isinstance(j, dict) else j.id) != jogador_id]
            if not sala["jogadores"]:  # Se não houver mais jogadores, marcar a sala para remoção
                sala_a_remover = sala_id
            break

    # Remover a sala se não houver jogadores restantes
    if sala_a_remover:
        del salas[sala_a_remover]

    # Remover o jogador de player_ids
    del player_ids[sid]
    
    # Atualizar a lista de salas disponíveis para todos os clientes
    salas_info = []
    for sala_id, sala_info in salas.items():
        salas_info.append({
            "sala_id": sala_id,
            "jogadores": [j.to_dict() if isinstance(j, Jogador) else j for j in sala_info["jogadores"]],
            "rodada": sala_info["rodada"],
        })
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes

sio = socketio.Server(cors_allowed_origins=["https://poker-pyxel-a16f85e125a4.herokuapp.com","http://localhost:3000", "http://localhost:4000", "*"])

port = int(os.environ.get("PORT", 4000))
# Inicia o servidor WSGI
if __name__ == '__main__':
    import eventlet
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), app)
    