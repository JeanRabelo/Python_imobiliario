import json
from copy import copy
from random import randint, shuffle
from pprint import pprint

def get_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
        return data

def record_json(path, info):
    with open(path, 'w') as json_file:
        json.dump(info, json_file)

def pegar_condicoes_iniciais():
    jogadores_agrupados = {'impulsivos':None, 'exigentes':None, 'cautelosos':None, 'aleatórios':None}
    propriedades = get_json('propriedades.json')
    jogadores = []
    for tipo in jogadores_agrupados.keys():
        jogadores_agrupados[tipo] = randint(1, 6)
    for tipo in jogadores_agrupados.keys():
        for i in range(jogadores_agrupados[tipo]):
            jogadores.append({'tipo':tipo[:-1], 'saldo':300, 'posicao':0})
    shuffle(jogadores)
    return [jogadores, propriedades, jogadores_agrupados]

def comprar_se_puder(jogadores, propriedades, n_jogador):
    preco = propriedades[jogadores[n_jogador]['posicao']]['preco']
    if preco <= jogadores[n_jogador]['saldo']:
        jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] - preco
        propriedades[jogadores[n_jogador]['posicao']]['dono'] = n_jogador
    return [jogadores, propriedades]

def jogada(n_jogador):
    if jogadores[n_jogador]['saldo'] < 0:
        return False
    # inicio da jogada
    dado = randint(1, 6)
    if dado + jogadores[n_jogador]['posicao'] >= 20: # ganhar os 100 da volta no tabuleiro
        jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] + 100
    posicao = (jogadores[n_jogador]['posicao'] + dado) % 20 # nova posição do jogador
    jogadores[n_jogador]['posicao'] = posicao
    if propriedades[posicao]['dono'] is not None: # se a propriedade tiver dono
        aluguel = propriedades[jogadores[n_jogador]['posicao']]['aluguel']
        n_dono = propriedades[jogadores[n_jogador]['posicao']]['dono']
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
    # ajustar as propriedades caso o jogador perca
    if jogadores[n_jogador]['saldo'] < 0:
        for propriedade in propriedades:
            if propriedade['dono'] == n_jogador:
                propriedade['dono'] = None
    # definir o vencedor caso o jogador ganhe:
    jogador_venceu_dentro_do_loop = True
    for i_jogador in set(range(0,len(jogadores)))-set([n_jogador]):
        if jogadores[i_jogador]['saldo'] > 0:
            jogador_venceu_dentro_do_loop  = False
    # fim da jogada
    return jogador_venceu_dentro_do_loop 

[jogadores_iniciais, propriedades_iniciais, jogadores_agrupados] = pegar_condicoes_iniciais()

record_json('jogadores_iniciais.json', jogadores_iniciais)
record_json('propriedades_iniciais.json', propriedades_iniciais)

# início da simulação
resultados = []
partidas = 300
partida = 0
while partida in range (0, partidas):
    # inicio da partida
    jogador_venceu_fora_do_loop = False
    rodada = 0
    jogadores_iniciais_f = get_json('jogadores_iniciais.json')
    propriedades = get_json('propriedades_iniciais.json')
    jogadores = jogadores_iniciais_f
    while rodada in range (0,1000) and not jogador_venceu_fora_do_loop:
        # inicio da rodada
        n_jogador = 0
        while n_jogador in range(0, len(jogadores)) and not jogador_venceu_fora_do_loop:
            jogador_venceu_fora_do_loop = jogada(n_jogador)
            n_jogador += 1
        rodada += 1
        # fim da rodada

    # adicionar o turno dos jogadores (para servir de critério secundário de ordenamento)
    for i in range(0,len(jogadores)):
        jogadores[i]['turno'] = i
    
    classificacao = sorted(jogadores, key = lambda y: (y['saldo'], -y['turno']), reverse=True)
    vencedor = classificacao[0]['tipo']
    # fim da partida
    partida += 1
    resultados.append({'vencedor':vencedor, 'rodada':rodada, 'n_jogador': n_jogador})
    print(f'partida {partida} de {partidas}', end='\r')

print('\n')

# calcular timeouts
timeouts = 0
soma_turnos = 0
jogadores_agrupados_vitorias = {'impulsivos':0, 'exigentes':0, 'cautelosos':0, 'aleatórios':0}
for resultado in resultados:
    if resultado['rodada'] == 1000 and classificacao[1]['saldo'] > 0:
        timeouts += 1
    soma_turnos += resultado['rodada'] * len(jogadores) + resultado['n_jogador'] + 1
    jogadores_agrupados_vitorias[resultado['vencedor']+'s'] += 1

media_turnos = soma_turnos / (partidas * 1.0)
jogadores_agrupados_eficiencia = {}
max_eficiencia = 0
mais_eficiente = ''

for tipo in jogadores_agrupados_vitorias.keys():
    if 1.0 * jogadores_agrupados_vitorias[tipo] / jogadores_agrupados[tipo] > max_eficiencia:
        max_eficiencia = 1.0 * jogadores_agrupados_vitorias[tipo] / jogadores_agrupados[tipo]
        mais_eficiente = tipo
    jogadores_agrupados_eficiencia[tipo] = 1.0 * jogadores_agrupados_vitorias[tipo] / jogadores_agrupados[tipo]
    jogadores_agrupados_vitorias[tipo] = str(round(jogadores_agrupados_vitorias[tipo] / (partidas) * 100.00)) + '%' 


print(f'timeouts = {timeouts}')
print(f'média de turnos = {media_turnos}')
print('porcentagem de vitórias de acordo com o comportamento dos jogadores')
print(jogadores_agrupados_vitorias)
print(f'perfil mais vitorioso (maior quantidade de vitorias pela quantidade de jogadores) = {mais_eficiente}')
# fim da simulação 
