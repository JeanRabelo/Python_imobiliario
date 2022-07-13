import json
from random import randint, shuffle
from pprint import pprint

def get_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

def pegar_condicoes_iniciais():
    jogadores_agrupados = {'impulsivos':None, 'exigentes':None, 'cautelosos':None, 'aleatórios':None}
    propriedades = get_json('propriedades.json')
    jogadores = []
    for tipo in jogadores_agrupados.keys():
        # jogadores_agrupados[tipo] = int(input(f'Número de jogadores {tipo}: '))
        jogadores_agrupados[tipo] = randint(0, 5)
    for tipo in jogadores_agrupados.keys():
        for i in range(jogadores_agrupados[tipo]):
            jogadores.append({'tipo':tipo[:-1], 'saldo':300, 'posicao':0})
    shuffle(jogadores)
    return [jogadores, propriedades]

def comprar_se_puder(jogadores, propriedades, n_jogador):
    preco = propriedades[jogadores[n_jogador]['posicao']]['preco']
    if preco <= jogadores[n_jogador]['saldo']:
        jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] - preco
        propriedades[jogadores[n_jogador]['posicao']]['dono'] = n_jogador
    return [jogadores, propriedades]

def jogada(n_jogador):
    # inicio da jogada
    dado = randint(1, 6)
    # dado = 1
    print(f'dado = {dado}')
    if dado + jogadores[n_jogador]['posicao'] >= 20: # ganhar os 100 da volta no tabuleiro
        jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] + 100
    # espaco
    posicao = (jogadores[n_jogador]['posicao'] + dado) % 20 # nova posição do jogador
    jogadores[n_jogador]['posicao'] = posicao
    # espaco
    if propriedades[posicao]['dono'] is not None: # se a propriedade tiver dono
        aluguel = propriedades[jogadores[n_jogador]['posicao']]['aluguel']
        n_dono = propriedades[jogadores[n_jogador]['posicao']]['dono']
        # print(aluguel)
        # print(n_dono)
        jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] - aluguel  # dinheiro pago pelo inquilino
        jogadores[n_dono]['saldo'] = jogadores[n_dono]['saldo'] + aluguel  # dinheiro recebido pelo dono
    else: # se a propriedade não tiver dono
        if jogadores[n_jogador]['tipo'] == 'impulsivo':
            comprar_se_puder(jogadores, propriedades, n_jogador)
        elif jogadores[n_jogador]['tipo'] == 'exigente':
            if propriedades[posicao]['aluguel'] > 50:
                comprar_se_puder(jogadores, propriedades, n_jogador)
        elif jogadores[n_jogador]['tipo'] == 'cauteloso':
            if jogadores[n_jogador]['saldo'] - propriedades[posicao]['preco'] >= 80:
                comprar_se_puder(jogadores, propriedades, n_jogador)
        elif jogadores[n_jogador]['tipo'] == 'aleatório':
            if randint(0,1) == 1:
                comprar_se_puder(jogadores, propriedades, n_jogador)
    # espaco
    # ajustar as propriedades caso o jogador perca
    if jogadores[n_jogador]['saldo'] < 0:
        for propriedade in propriedades:
            if propriedade['dono'] == n_jogador:
                propriedade['dono'] = None
    # espaco
    # definir o vencedor caso o jogador ganhe:
    jogador_venceu = True
    for i_jogador in set(range(0,len(jogadores)))-set([n_jogador]):
        if jogadores[i_jogador]['saldo'] > 0:
            jogador_venceu = False
    # espaco
    # fim da jogada
    # pprint(jogadores)
    # pprint(propriedades)
    return jogador_venceu

[jogadores, propriedades] = pegar_condicoes_iniciais()
jogador_venceu = False
# inicio da partida
rodada = 0
while rodada in range (0,1000) and not jogador_venceu:
    # inicio da rodada
    n_jogador = 0
    while n_jogador in range(0, len(jogadores)) and not jogador_venceu:
        jogador_venceu = jogada(n_jogador)
        n_jogador += 1
    print(f'rodada = {rodada + 1}')
    rodada += 1
    # fim da rodada

# adicionar o turno dos jogadores (para servir de critério secundário de ordenamento)
for i in range(0,len(jogadores)):
    jogadores[i]['turno'] = i

pprint(sorted(jogadores, key = lambda y: (y['saldo'], -y['turno']), reverse=True))
winner = sorted(jogadores, key = lambda y: (y['saldo'], -y['turno']), reverse=True)[0]['tipo']
# fim da partida
pprint(propriedades)
print(winner)
