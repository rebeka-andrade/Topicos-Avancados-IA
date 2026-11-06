"""8-Puzzle: busca em largura com poda de estados repetidos."""
from collections import deque

OBJETIVO = (0, 1, 2, 3, 4, 5, 6, 7, 8)
MOVIMENTOS = ((-1, 0, 'Cima'), (1, 0, 'Baixo'), (0, -1, 'Esquerda'), (0, 1, 'Direita'))


def mostrar(estado):
    for i in range(0, 9, 3):
        print(' '.join('X' if n == 0 else str(n) for n in estado[i:i + 3]))


def inversoes(estado):
    pecas = [n for n in estado if n != 0]
    return sum(pecas[i] > pecas[j] for i in range(8) for j in range(i + 1, 8))


def validar(estado):
    if len(estado) != 9 or set(estado) != set(range(9)):
        raise ValueError('Informe exatamente os números de 0 a 8, sem repetição (0 representa X).')


def vizinhos(estado):
    pos = estado.index(0)
    linha, coluna = divmod(pos, 3)
    for dl, dc, acao in MOVIMENTOS:
        nl, nc = linha + dl, coluna + dc
        if 0 <= nl < 3 and 0 <= nc < 3:
            nova_pos = nl * 3 + nc
            novo = list(estado)
            novo[pos], novo[nova_pos] = novo[nova_pos], novo[pos]
            yield tuple(novo), acao


def busca_largura(inicial):
    validar(inicial)
    if inversoes(inicial) % 2 != inversoes(OBJETIVO) % 2:
        return None, 0
    fila = deque([inicial])
    visitados = {inicial}
    pais = {inicial: (None, None)}
    avaliados = 0
    while fila:
        atual = fila.popleft()
        avaliados += 1
        if atual == OBJETIVO:
            caminho = []
            while atual is not None:
                anterior, acao = pais[atual]
                caminho.append((atual, acao))
                atual = anterior
            return caminho[::-1], avaliados
        for proximo, acao in vizinhos(atual):
            if proximo not in visitados:
                visitados.add(proximo)
                pais[proximo] = (atual, acao)
                fila.append(proximo)
    return None, avaliados


def criar_teste(passos):
    estado = OBJETIVO
    for acao in passos:
        alternativas = {nome: proximo for proximo, nome in vizinhos(estado)}
        estado = alternativas[acao]
    return estado


TESTES = [
    ('Teste 1 - professora', (4, 6, 2, 8, 1, 3, 7, 5, 0)),
    ('Teste 2 - professora', (6, 4, 2, 8, 1, 3, 7, 5, 0)),
    ('Teste 3 - adicional', criar_teste(['Direita', 'Baixo', 'Direita', 'Baixo', 'Esquerda', 'Cima'])),
    ('Teste 4 - adicional', criar_teste(['Baixo', 'Direita', 'Cima', 'Direita', 'Baixo', 'Esquerda', 'Baixo', 'Esquerda'])),
]


def executar(nome, estado):
    print(f'\n=== {nome} ===')
    print('Estado inicial:')
    mostrar(estado)
    print(f'Inversões: {inversoes(estado)}')
    caminho, avaliados = busca_largura(estado)
    if caminho is None:
        print('Sem solução: a paridade das inversões é incompatível com o objetivo.')
        return
    for numero, (tabuleiro, acao) in enumerate(caminho):
        print(f'\nPasso {numero} - {acao if acao else "Estado inicial"}')
        mostrar(tabuleiro)
    print(f'\nTotal de passos: {len(caminho) - 1}')
    print(f'Estados avaliados (retirados da fila): {avaliados}')


def main():
    while True:
        print('\n=== 8-PUZZLE - BUSCA EM LARGURA ===')
        for indice, (nome, _) in enumerate(TESTES, 1):
            print(f'{indice} - {nome}')
        print('5 - Tabuleiro personalizado')
        print('6 - Executar todos os testes')
        print('0 - Sair')
        escolha = input('Escolha uma opção: ').strip()
        if escolha == '0':
            break
        if escolha in ('1', '2', '3', '4'):
            executar(*TESTES[int(escolha) - 1])
        elif escolha == '5':
            try:
                texto = input('Digite 9 valores separados por espaço (X para vazio): ')
                estado = tuple(int(p) if p.upper() != 'X' else 0 for p in texto.split())
                validar(estado)
                executar('Personalizado', estado)
            except ValueError as erro:
                print('Entrada inválida:', erro)
        elif escolha == '6':
            for teste in TESTES:
                executar(*teste)
        else:
            print('Opção inválida.')


if __name__ == '__main__':
    main()
