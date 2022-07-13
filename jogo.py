import json
from random import random, shuffle
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
        jogadores_agrupados[tipo] = int(random() * 5)
    for tipo in jogadores_agrupados.keys():
        for i in range(jogadores_agrupados[tipo]):
            jogadores.append({'tipo':tipo[:-1], 'saldo':300})
    shuffle(jogadores)
    return [jogadores, propriedades]

[jogadores, propriedades] = pegar_condicoes_iniciais()

pprint(jogadores)
pprint(propriedades)
