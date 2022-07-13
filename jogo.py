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

[jogadores, propriedades] = pegar_condicoes_iniciais()
# inicio da rodada
# inicio da jogada
n_jogador = 0
# dado = randint(1, 6)
dado = 1
if dado + jogadores[n_jogador]['posicao'] >= 20: # ganhar os 100 da volta no tabuleiro
    jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] + 100
jogadores[n_jogador]['posicao'] = (jogadores[n_jogador]['posicao'] + dado) % 20 # nova posição do jogador

if propriedades[jogadores[n_jogador]['posicao']]['dono'] is not None: # se a propriedade tiver dono
    aluguel = propriedades[jogadores[n_jogador]['posicao']]['aluguel']
    n_dono = propriedades[jogadores[n_jogador]['posicao']]['dono']
    print(aluguel)
    print(n_dono)
    jogadores[n_jogador]['saldo'] = jogadores[n_jogador]['saldo'] - aluguel  # dinheiro pago pelo inquilino
    jogadores[n_dono]['saldo'] = jogadores[n_dono]['saldo'] + aluguel  # dinheiro recebido pelo dono
else: # se a propriedade não tiver dono
    if jogadores[n_jogador]['tipo'] == 'impulsivo':
        comprar_se_puder(jogadores, propriedades, n_jogador)

# fim da jogada 
# fim da rodada
pprint(jogadores)
pprint(propriedades)
