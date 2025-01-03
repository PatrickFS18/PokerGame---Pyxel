import socketio
from utils.jogador import Jogador
from utils.victory import Victory
from utils.initGame import InitGame

# Inicializando o servidor SocketIO
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:4000", "*"])

# Dicionário para armazenar as salas e os jogadores
salas = {}

# Limite de jogadores por sala
MAX_JOGADORES = 2  

# Variável usada para definir o ID dos jogadores 
player_id_counter = 1
player_ids = {}

# Função que conecta ao Socket
@sio.event
def connect(sid):
    global player_id_counter

    # Atribui o próximo ID disponível ao jogador
    player_ids[sid] = player_id_counter

    salas_info = []
    
    # Desempacotando chave (ID) e valor (informações da sala)
    for sala_id, sala_info in salas.items():  

        salas_info.append({
            "sala_id": sala_id, 
            "jogadores": [j.to_dict() for j in sala_info["jogadores"]],
            "rodada": sala_info["rodada"],
            "dealer": sala_info.get("dealer", {'mao': []}),
        })

    # Envia as salas disponíveis a todos os usuarios 
    sio.emit('salas_disponiveis', {'salas': salas_info})  
    
    player_id_counter += 1
    
    print(f"Jogador conectado: sid {sid}, id personalizado {player_ids[sid]}")
    # Envia o ID personalizado para o cliente
    sio.emit('sid', {'sid': sid, 'player_id': player_ids[sid]}, room=sid)


# Função que cria a sala Socket
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
        "baralho": [], 
        "dealer": {'mao': []}
    }

    # O jogador entra na sala
    sio.enter_room(sid, sala_id)

    # Emitir evento para o criador da sala (só ele recebe isso)
    sio.emit('sala_criada', {'sala_id': sala_id, 'status': 'criada'}, room=sid)

    # Emitir a lista de salas para todos os usuarios
    salas_info = [{'sala_id': sala_id, 'jogadores': [j.to_dict() for j in sala['jogadores']], 'rodada': sala['rodada'], 'dealer': sala['dealer']} for sala_id, sala in salas.items()]
    sio.emit('salas_disponiveis', {'salas': salas_info})  
    
@sio.event
def ingressar_sala(sid, sala_id):
    sala_id = str(sala_id) 
    if sala_id in salas:
        print(salas[sala_id])
        if len(salas[sala_id]["jogadores"]) < MAX_JOGADORES:
            jogador = Jogador(player_ids[sid])
            salas[sala_id]["jogadores"].append(jogador) 
            sio.enter_room(sid, sala_id)
            
            salas_info = []
            for sala_id, sala_info in salas.items(): 
                salas_info.append({
                    "sala_id": sala_id, 
                    "jogadores": [j.to_dict() for j in sala_info["jogadores"]],
                    "rodada": sala_info["rodada"],
                    "dealer": sala_info.get("dealer", {'mao': []}), 
                })
            sio.emit('salas_disponiveis', {'salas': salas_info})  

            sio.emit('sala_ingressada', {'sala_id': sala_id, 'status': 'ingressado'}, room=sid)
            
            if len(salas[sala_id]["jogadores"]) == MAX_JOGADORES:
                print('vendo os jogadores na sala: ', [j.id for j in salas[sala_id]["jogadores"]])

                # A partida deve começar, e iniciar a distribuição de cartas

                instanciar_cartas = InitGame()
                sio.emit('salas_disponiveis', {'salas': salas_info}) 

                # Gerar o baralho para esta sala
                instanciar_cartas.init_game(sala_id)
                
                cartas = instanciar_cartas.get_baralho(sala_id)
                if cartas is not None:
                    # Distribuir as cartas para os jogadores
                    jogadores, dealer = instanciar_cartas.distribuir_cartas([j.id for j in salas[sala_id]["jogadores"]], cartas)

                    # Atualizar os objetos dos jogadores na sala
                    for i, jogador_obj in enumerate(salas[sala_id]["jogadores"]):
                        jogador_obj.mao = jogadores[i].mao

                    # Atualizar o objeto do dealer na sala
                    salas[sala_id]["dealer"]["mao"] = dealer.mao

                    # Converter a lista de jogadores para uma lista de dicionários
                    jogadores_dict = [jogador.to_dict() for jogador in salas[sala_id]["jogadores"]]

                    # Converter as cartas do dealer para uma lista de dicionários
                    dealer_dict = [carta.to_dict() for carta in dealer.mao]

                    sio.emit('init_game', {
                        'sala_id': sala_id,
                        'mensagem': 'A partida vai começar!',
                        'jogadores': jogadores_dict,
                        'dealer': dealer_dict
                    }, room=sala_id)
                    print(salas)
        else:
            sio.emit('erro_sala', {'mensagem': 'Sala cheia!'}, room=sid) # Mensagens de erro não utilizadas no Front. Diferenciavel opcional, mas não incluído
    else:
        sio.emit('erro_sala', {'mensagem': 'Sala inexistente!'}, room=sid)

# Função usada para chamar nova rodada
@sio.event
def nova_rodada(sid, data):
    victory = Victory()
    sala_id = str(data["sala_id"])  
    id_player = data["id_player"] 
    print(f'aqui chamou com sala_id: {sala_id} pelo jogador {id_player}')
    
    sala_encontrada = None
    
    # Procurar pela sala correspondente no dicionário
    for id, sala in salas.items():
        if id == sala_id:
            sala_encontrada = sala
            break
    
    if sala_encontrada:
        sala = sala_encontrada
        
        # Verificar se é a vez do jogador correspondente
        rodada = sala["rodada"]
        # Lógica que considera o primeiro jogador na sala quem inicia a parida. Desta forma, em rodadas ímpares será sua vez
        jogador_permitido = sala["jogadores"][0].id if rodada % 2 != 0 else sala["jogadores"][1].id
        
        if id_player != jogador_permitido:
            sio.emit('erro', {'mensagem': 'Não é a sua vez de jogar!'}, room=sid)
            
            return
        else:
            
            if sala["rodada"] < 6:
                sala["rodada"] += 1

            if sala["rodada"] == 6:
            # VERIFICAR GANHADOR
                if len(sala["jogadores"]) >= 2:
                    jogador = sala["jogadores"][0]
                    adversario = sala["jogadores"][1]
                    dealer = sala["dealer"]
                    if jogador is not None and dealer is not None and adversario is not None and sala["rodada"] == 6:
                        victory.verifyLogic(dealer, jogador, adversario)
                    if victory.winner is not None:
                        sio.emit('vencedor', {'sala_id': sala_id, 'vencedor': victory.winner, 'rodada': sala["rodada"]}, room=sala_id)
                    else:
                        sio.emit('erro', {'mensagem': 'Sala inexistente!'}, room=sid)

        sio.emit('nova_rodada', {'sala_id': sala_id, 'rodada': sala["rodada"]}, room=sala_id)
        print(f"Rodada atualizada para: {sala['rodada']}")
    else:
        sio.emit('erro', {'mensagem': 'Sala inexistente!'}, room=sid)


# Função usada para listar salas disponíveis
@sio.event
def salas_disponiveis(data):
    salas_info = []
    for sala_id, sala_info in salas.items():  # Desempacotando chave (ID) e valor (informações da sala)
        salas_info.append({
            "sala_id": sala_id,  # Adicione o ID da sala para facilitar no cliente
            "jogadores": [j.to_dict() for j in sala_info["jogadores"]],
            "rodada": sala_info["rodada"],
            "dealer": sala_info.get("dealer", {'mao': []}),  # Inclua o dealer se ele existir, caso contrário, uma lista vazia
        })
    print('imprimindo as salas info: ', salas_info)
    sio.emit('salas_disponiveis', {'salas': salas_info})  # Envia para todos


# Função que disconecta o usuario da sala e remove as suas informações da sala
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
            "dealer": sala_info.get("dealer", {'mao': []}),  # Inclua o dealer se ele existir, caso contrário, uma lista vazia
            
        })
        sio.emit('salas_disponiveis', {'salas': salas_info})  # Atualiza todos os clientes


# Inicia o servidor
if __name__ == '__main__':
    import eventlet
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 4000)), app)
