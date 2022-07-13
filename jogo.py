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
    # inicio da jogada
    dado = randint(1, 6)
    # dado = 1
    # print(f'dado = {dado}')
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

[jogadores, propriedades, jogadores_agrupados] = pegar_condicoes_iniciais()

# início da simulação
resultados = []
partida = 0
while partida in range (0,300):
    # inicio da partida
    jogador_venceu = False
    rodada = 0
    while rodada in range (0,1000) and not jogador_venceu:
        # inicio da rodada
        n_jogador = 0
        while n_jogador in range(0, len(jogadores)) and not jogador_venceu:
            jogador_venceu = jogada(n_jogador)
            n_jogador += 1
        # print(f'rodada = {rodada + 1}')
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
    print(f'partida {partida} de 300', end='\r')

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

media_turnos = soma_turnos / 300.0
jogadores_agrupados_eficiencia = {}
max_eficiencia = 0
mais_eficiente = ''

for tipo in jogadores_agrupados_vitorias.keys():
    if 1.0 * jogadores_agrupados_vitorias[tipo] / jogadores_agrupados[tipo] > max_eficiencia:
        max_eficiencia = 1.0 * jogadores_agrupados_vitorias[tipo] / jogadores_agrupados[tipo]
        mais_eficiente = tipo
    jogadores_agrupados_eficiencia[tipo] = 1.0 * jogadores_agrupados_vitorias[tipo] / jogadores_agrupados[tipo]
    jogadores_agrupados_vitorias[tipo] = str(round(jogadores_agrupados_vitorias[tipo] / 300.00 * 100)) + '%' 


print(f'timeouts = {timeouts}')
print(f'média de turnos = {media_turnos}')
print('porcentagem de vitórias de acordo com o comportamento dos jogadores')
print(jogadores_agrupados_vitorias)
print(f'perfil mais vitorioso (maior quantidade de vitorias pela quantidade de jogadores) = {mais_eficiente}')
# fim da simulação 
print(len(jogadores))
print(jogadores_agrupados_eficiencia)
print(jogadores_agrupados)
