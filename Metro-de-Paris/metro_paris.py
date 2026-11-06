"""Busca A* no mapa simplificado do metrô de Paris (14 estações)."""
import csv
import heapq
from itertools import count

VELOCIDADE_KMH = 30
PENALIDADE_TROCA = 5
# Distâncias reais em km e linhas identificadas pelas cores do mapa.
ARESTAS = [
    ('E1','E2',11,'Azul'), ('E2','E3',9,'Azul'),
    ('E2','E9',11,'Amarela'), ('E2','E10',4,'Amarela'),
    ('E3','E4',7,'Azul'), ('E3','E9',10,'Vermelha'),
    ('E3','E13',19,'Vermelha'), ('E4','E5',14,'Azul'),
    ('E4','E8',16,'Verde'), ('E4','E13',12,'Verde'),
    ('E5','E6',3,'Azul'), ('E5','E7',2,'Amarela'),
    ('E5','E8',33,'Amarela'), ('E8','E9',10,'Amarela'),
    ('E8','E12',7,'Verde'), ('E9','E11',14,'Vermelha'),
    ('E13','E14',5,'Verde'),
]
# Distâncias em linha reta (km), página 2 do PDF; ordem E1,...,E14.
MATRIZ_HEURISTICA = [
[0,11,20,27,40,43,39,28,18,10,18,30,30,32],
[11,0,9,16,29,32,28,19,11,4,17,23,21,24],
[20,9,0,7,20,22,19,15,10,11,21,21,13,18],
[27,16,7,0,13,16,12,13,13,18,26,21,11,17],
[40,29,20,13,0,3,2,21,25,31,38,27,16,20],
[43,32,22,16,3,0,4,23,28,33,41,30,17,20],
[39,28,19,12,2,4,0,22,25,29,38,28,13,17],
[28,19,15,13,21,23,22,0,9,22,18,7,25,30],
[18,11,10,13,25,28,25,9,0,13,12,12,23,28],
[10,4,11,18,31,33,29,22,13,0,20,27,20,23],
[18,17,21,26,38,41,38,18,12,20,0,15,35,39],
[30,23,21,21,27,30,28,7,12,27,15,0,31,37],
[30,21,13,11,16,17,13,25,23,20,35,31,0,5],
[32,24,18,17,20,20,17,30,28,23,39,37,5,0],
]
ESTACOES = [f'E{i}' for i in range(1,15)]
INDICE = {e:i for i,e in enumerate(ESTACOES)}
GRAFO = {e: [] for e in ESTACOES}
for a,b,km,linha in ARESTAS:
    GRAFO[a].append((b,km,linha))
    GRAFO[b].append((a,km,linha))

def heuristica(estacao, destino):
    """Limite inferior do tempo restante, em minutos."""
    return MATRIZ_HEURISTICA[INDICE[estacao]][INDICE[destino]] * 60 / VELOCIDADE_KMH

def a_estrela(origem, destino):
    """Retorna rota ótima considerando a linha de chegada em cada estado."""
    if origem not in GRAFO or destino not in GRAFO:
        raise ValueError('Use uma estação de E1 a E14.')
    inicial = (origem, None)  # (estação, linha utilizada para chegar)
    custos = {inicial: 0.0}
    anterior = {}
    fila = []
    sequencia = count()
    heapq.heappush(fila, (heuristica(origem,destino),next(sequencia),0.0,inicial))
    while fila:
        _,_,custo_atual,estado = heapq.heappop(fila)
        if custo_atual > custos.get(estado,float('inf')) + 1e-9:
            continue
        estacao, linha_anterior = estado
        if estacao == destino:
            passos = []
            atual = estado
            while atual != inicial:
                prev, km, linha, troca = anterior[atual]
                passos.append((prev[0],atual[0],km,linha,troca))
                atual = prev
            passos.reverse()
            return {
                'origem': origem, 'destino': destino,
                'caminho': [origem]+[p[1] for p in passos],
                'passos': passos, 'distancia_km': sum(p[2] for p in passos),
                'trocas': sum(p[4] for p in passos),
                'tempo_min': custo_atual,
            }
        for vizinho, km, linha in GRAFO[estacao]:
            troca = linha_anterior is not None and linha != linha_anterior
            custo = custo_atual + km*60/VELOCIDADE_KMH + (PENALIDADE_TROCA if troca else 0)
            proximo = (vizinho,linha)
            if custo + 1e-9 < custos.get(proximo,float('inf')):
                custos[proximo] = custo
                anterior[proximo] = (estado,km,linha,troca)
                prioridade = custo + heuristica(vizinho,destino)
                heapq.heappush(fila,(prioridade,next(sequencia),custo,proximo))
    return None

def exportar_resultados(arquivo='resultados_todas_combinacoes.csv'):
    with open(arquivo,'w',newline='',encoding='utf-8-sig') as f:
        writer=csv.writer(f,delimiter=';')
        writer.writerow(['Origem','Destino','Caminho','Distância (km)','Trocas','Tempo (min)','Mudanças de linha'])
        for origem in ESTACOES:
            for destino in ESTACOES:
                if origem==destino:
                    continue
                r=a_estrela(origem,destino)
                mudancas=[]
                for a,b,km,linha,troca in r['passos']:
                    if troca:
                        mudancas.append(f'{a}: {mudancas_linha_anterior(r,a)} -> {linha}')
                writer.writerow([origem,destino,' -> '.join(r['caminho']),r['distancia_km'],r['trocas'],int(r['tempo_min']), ' | '.join(mudancas) or 'Nenhuma'])

def mudancas_linha_anterior(resultado,estacao):
    for i,p in enumerate(resultado['passos']):
        if p[0]==estacao and p[4]:
            return resultado['passos'][i-1][3]
    return '?'

def demonstrar(resultado):
    print('\nMelhor caminho:', ' -> '.join(resultado['caminho']))
    print('Distância:', resultado['distancia_km'],'km')
    linha_anterior=None
    for a,b,km,linha,troca in resultado['passos']:
        if troca:
            print(f'  TROCA em {a}: {linha_anterior} -> {linha} (+5 min)')
        print(f'  {a} -> {b}: linha {linha}, {km} km, {km*2} min de viagem')
        linha_anterior=linha
    print('Trocas:',resultado['trocas'])
    print('Tempo total:',int(resultado['tempo_min']),'minutos')

if __name__=='__main__':
    print('METRÔ DE PARIS — BUSCA A*')
    origem=input('Origem (E1 a E14): ').strip().upper()
    destino=input('Destino (E1 a E14): ').strip().upper()
    try:
        demonstrar(a_estrela(origem,destino))
        exportar_resultados()
        print('\nTabela de todas as 182 viagens salva em resultados_todas_combinacoes.csv')
    except ValueError as erro:
        print('Erro:',erro)
