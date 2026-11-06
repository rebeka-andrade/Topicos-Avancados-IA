TAMANHO = 8


def posicao_segura(rainhas, linha, coluna):
    for outra_linha, outra_coluna in rainhas.items():
        if outra_linha == linha or outra_coluna == coluna:
            return False
        if abs(outra_linha - linha) == abs(outra_coluna - coluna):
            return False
    return True


def mostrar_tabuleiro(rainhas):
    print('    ' + ' '.join(str(c) for c in range(1, TAMANHO + 1)))
    for linha in range(TAMANHO):
        casas = ['Q' if rainhas.get(linha) == coluna else '.'
                 for coluna in range(TAMANHO)]
        print(f'{linha + 1:2}  ' + ' '.join(casas))


def busca_profundidade(iniciais):
    rainhas = dict(iniciais)
    estatisticas = {'criados': 1, 'explorados': 0}

    def dfs(linha):
        estatisticas['explorados'] += 1
        if linha == TAMANHO:
            return True
        if linha in rainhas:
            return dfs(linha + 1)
        for coluna in range(TAMANHO):
            if posicao_segura(rainhas, linha, coluna):
                rainhas[linha] = coluna
                estatisticas['criados'] += 1
                if dfs(linha + 1):
                    return True
                del rainhas[linha]
        return False

    encontrou = dfs(0)
    return (dict(rainhas) if encontrou else None), estatisticas


def ler_rainhas(quantidade):
    rainhas = {}
    while len(rainhas) < quantidade:
        indice = len(rainhas) + 1
        entrada = input(f'Rainha {indice} - linha e coluna (ex.: 1 4): ').split()
        if len(entrada) != 2:
            print('Digite dois números separados por espaço.')
            continue
        try:
            linha, coluna = map(int, entrada)
        except ValueError:
            print('Digite apenas números inteiros.')
            continue
        if not (1 <= linha <= 8 and 1 <= coluna <= 8):
            print('Linha e coluna devem estar entre 1 e 8.')
            continue
        linha -= 1
        coluna -= 1
        if not posicao_segura(rainhas, linha, coluna):
            print('Posição inválida: essa rainha atacaria outra. Tente novamente.')
            continue
        rainhas[linha] = coluna
    return rainhas


def main():
    while True:
        print('\n=== PROBLEMA DAS 8 RAINHAS - DFS ===')
        print('1 - Tabuleiro vazio')
        print('2 - Tabuleiro com 1 rainha')
        print('3 - Tabuleiro com 2 rainhas')
        print('4 - Tabuleiro com 3 rainhas')
        print('0 - Sair')
        opcao = input('Escolha uma opção: ').strip()
        if opcao == '0':
            print('Programa encerrado.')
            break
        if opcao not in ('1', '2', '3', '4'):
            print('Opção inválida.')
            continue
        quantidade = int(opcao) - 1
        iniciais = ler_rainhas(quantidade)
        print('\nTabuleiro inicial:')
        mostrar_tabuleiro(iniciais)
        solucao, estatisticas = busca_profundidade(iniciais)
        if solucao is None:
            print('\nNão existe solução para essas posições fixas.')
        else:
            print('\nSolução encontrada:')
            mostrar_tabuleiro(solucao)
        print(f"\nNós criados: {estatisticas['criados']}")
        print(f"Nós explorados: {estatisticas['explorados']}")
        print('Critério: o estado inicial conta como 1 nó; cada nova rainha')
        print('posicionada pela busca cria mais 1 nó. Avanços por linhas')
        print('com rainhas fixas não criam novos nós.')


if __name__ == '__main__':
    main()
