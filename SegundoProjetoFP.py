def numero_linhas(n):
    """
    Retorna o numero de linhas do tabuleiro com n orbitas.

    Assinatura:
        numero_linhas(n: int) -> int

    """
    return 2*n

def todas_colunas(n):
    """
    Retorna o conjunto de colunas do tabuleiro com n orbitas.

    Assinatura:
        todas_colunas(n: int) -> int
    """
    return {2: "abcd", 3: "abcdef", 4: "abcdefgh", 5: "abcdefghij"}[n]

def tamanho_tab(tab):
    """
    Retorna o numero de linhas/colunas do tabuleiro com n orbitas.

    Assinatura:
        tamanho_tab(tab:dict) -> int
    """
    return len(tab)


def cria_posicao(col, lin):
    """
    constroi um tuplo relativo.

    Assinatura:
        cria_posicao(col: str, lin: int) -> tuple
    """
    if not (type(col) == str and type(lin) == int and 1 <= lin <= 10 and len(col) == 1 and col in todas_colunas(5)):
        raise ValueError("cria_posicao: argumentos invalidos")
    return (col, lin)

def obtem_pos_col(pos):
    """
    seleciona posicao coluna.

    Assinatura:
        obtem_pos_col(pos: tuple) -> str
    """
    return pos[0]

def obtem_pos_lin(pos):
    """
    seleciona posicao linha.

    Assinatura:
        obtem_pos_lin(pos: tuple) -> int
    """
    return int(pos[1])

def eh_posicao(arg):
    """
    reconhece se é posicao.

    Assinatura:
        eh_posicao(arg: universal) -> bool
    """
    return (type(arg) == tuple and len(arg) == 2 and type(obtem_pos_col(arg)) == str and obtem_pos_col(arg).isalpha() \
            and obtem_pos_col(arg).islower() and len(obtem_pos_col(arg)) == 1 and type(obtem_pos_lin(arg)) == int)

def posicoes_iguais(p1, p2):
    """
    testa se as posicoes sao iguais.

    Assinatura:
        posicoes_iguais(p1: tuple, p2: tuple) -> bool
    """
    return eh_posicao(p1) and eh_posicao(p2) and p1 == p2

def posicao_para_str(pos):
    """
    transforma a posicao para str.

    Assinatura:
        posicao_para_str(pos: tuple) -> str
    """
    return obtem_pos_col(pos) + str(obtem_pos_lin(pos))

def str_para_posicao(s):
    """
    transforma str para posicao.

    Assinatura:
        str_para_posicao(s: str) -> tuple
    """
    return (obtem_pos_col(s), int(s[1]))

def eh_posicao_valida(pos, n):
    """
    verifica se a posicao é valida.

    Assinatura:
        eh_posicao_valida(pos: tuple, n: int) -> tuple
    """
    return eh_posicao(pos) and 1 <= pos[1] <= numero_linhas(n) and pos[0] in todas_colunas(n)

def posicao_para_baixo(pos):
    """
    retorna a posicao embaixo.

    Assinatura:
        posicao_para_baixo(pos: tuple) -> tuple
    """
    return (obtem_pos_col(pos), obtem_pos_lin(pos) + 1) 

def posicao_para_cima(pos):
    """
    retorna a posicao em cima.

    Assinatura:
        posicao_para_cima(pos: tuple) -> tuple
    """
    return (obtem_pos_col(pos), obtem_pos_lin(pos) - 1) 

def posicao_para_esquerda(pos):
    """
    retorna a posicao a esquerda.

    Assinatura:
        posicao_para_esquerda(pos: tuple) -> tuple
    """
    return (chr(ord(obtem_pos_col(pos)) - 1), obtem_pos_lin(pos))

def posicao_para_direita(pos):
    """
    retorna a posicao a direita.

    Assinatura:
        posicao_para_direita(pos: tuple) -> tuple
    """
    return (chr(ord(obtem_pos_col(pos)) + 1), obtem_pos_lin(pos))


def obtem_posicoes_adjacentes(pos, n, boliano):
    """
    retorna um tuplo com as posicoes adjacentes.

    Assinatura:
        obtem_posicoes_adjacentes(pos: tuple, n: int, boliano: bool) -> tuple
    """
    resp = ()
    # se forem as 8 posicoes adjacentes
    if boliano:
        # tuplo com a ordem das posicoes adjacentes
        direcoes = ( 
                (posicao_para_cima, lambda x: x),
                (posicao_para_cima, posicao_para_direita),
                (lambda x: x, posicao_para_direita),
                (posicao_para_baixo, posicao_para_direita),
                (posicao_para_baixo, lambda x: x),
                (posicao_para_baixo, posicao_para_esquerda),
                (lambda x: x, posicao_para_esquerda),
                (posicao_para_cima, posicao_para_esquerda)
            )
        # obter as posicoes adjacentes conforme a ordem
        for alteracao1, alteracao2 in direcoes:
            adj = alteracao1(alteracao2(pos))
            if eh_posicao_valida(adj, n):
                resp += (adj,)

    # se forem apenas as 4 adjacentes ortogonais
    else:
        # tuplo com a ordem das posicoes adjacentes
        direcoes = ( 
                posicao_para_cima,
                posicao_para_direita,
                posicao_para_baixo,
                posicao_para_esquerda,
            )
        # obter as posicoes adjacentes conforme a ordem
        for mudar_posicao in direcoes:
            adj = mudar_posicao(pos)
            if eh_posicao_valida(adj, n):
                resp += (adj,)

    return resp


def ordena_posicoes(posicoes, n):
    """
    retorna um tuplo com as posicoes ordenadas.

    Assinatura:
        ordena_posicoes(posicoes: tuple, n: int) -> tuple
    """
    ordenado =  ()
    # restringir o tabuleiro as posicoes centrais e ordena-las, depois expandir essas posicoes(camada) centrais por uma coluna e uma linha de cada lado
    # o i é a variavel que vai assumir quantas camadas faltam para acabar o tabuleiro(quando i==0, nao faltam amis camadas)
    i = n - 1
    while i >= 0:
        #so podem entrar no orbital posicoes do mesmo orbital
        orbital = ()
        for posicao in posicoes:
            # se posicao estiver no interior em questao mas nao tiver ja em ordenado, esta na camada que entrará em orbital
            if posicao not in ordenado and ( i < int(posicao[1]) <= numero_linhas(n) - i ) \
                and ( ord(todas_colunas(n)[i]) <= ord(posicao[0]) <= ord(todas_colunas(n)[-1]) - i ):
                orbital += (posicao,)
        
        ordenado += tuple(sorted(orbital, key = lambda x: (x[1], x[0])))
        
        i -= 1

    return ordenado



def cria_pedra_branca():
    """
    controe uma pedra branca.

    Assinatura:
        cria_pedra_branca() -> int
    """
    return -1

def cria_pedra_preta():
    """
    controe uma pedra preta.

    Assinatura:
        cria_pedra_preta() -> int
    """
    return 1

def eh_pedra(n):
    """
    reconhece se é uma pedra.

    Assinatura:
        eh_pedra(n: int) -> bool
    """
    return type(n) == int and -1 <= n <= 1 

def eh_pedra_branca(n):
    """
    reconhece se é uma pedra branca.

    Assinatura:
        eh_pedra_branca(n: int) -> bool
    """
    return type(n) == int and n == -1

def eh_pedra_preta(n):
    """
    reconhece se é uma pedra preta.

    Assinatura:
        eh_pedra_preta(n: int) -> bool
    """
    return type(n) == int and n == 1

def pedras_iguais(p1, p2):
    """
    testa se p1 e p2 sao pedras iguais.

    Assinatura:
        pedras_iguais(p1: int, p2: int) -> bool
    """
    return type(p1) == int == type(p2) and p1 == p2

def pedra_para_str(p):
    """
    transforma a pedra em str.

    Assinatura:
        pedra_para_str(p: int) -> str
    """
    return {1: "X", 0: " ", -1: "O"}[p]

def eh_pedra_jogador(p):
    """
    verifica se a pedra nao é neutra.

    Assinatura:
        eh_pedra_jogador(p: int) -> bool
    """
    return eh_pedra_preta(p) or eh_pedra_branca(p)

def pedra_para_int(p):
    """
    retorna a pedra em formato de str.

    Assinatura:
        pedra_para_int(p: int) -> int
    """
    return p



def cria_tabuleiro_vazio(n):
    """
    constroe um tabuleiro vazio.

    Assinatura:
        cria_tabuleiro_vazio(n: int) -> dict
    """
    if not(type(n) == int and 2 <= n <= 5):
        raise ValueError("cria_tabuleiro_vazio: argumento invalido")

    
    tabuleiro = {}
    # chaves do tabuleiro
    for j in todas_colunas(n):
        linhas = {}
        # chaves das colunas
        for i in range(1, numero_linhas(n)+1):
            linhas[i] = 0
        tabuleiro[j] = linhas

    return tabuleiro

def cria_tabuleiro(n, tp, tb): 
    """
    constroe um tabuleiro.

    Assinatura:
        cria_tabuleiro(n: int, tp: tuple, tb: tuple) -> dict
    """
    if not (type(n) == int and 2 <= n <= 5 and type(tp) == tuple and type(tb) == tuple and all(pos not in tb for pos in tp) and abs(len(tp) - len(tb)) <=1 \
           and all(type(pos) == tuple and len(pos) == 2 and type(pos[0]) == str and len(pos[0]) == 1 and type(pos[1]) == int and pos[0] in todas_colunas(n) and 0 <= pos[1] <= numero_linhas(n)  for pos in tp) \
            and all(type(pos) == tuple and len(pos) == 2 and type(pos[0]) == str and len(pos[0]) == 1 and type(pos[1]) == int and pos[0] in todas_colunas(n) and 0 <= pos[1] <= numero_linhas(n)  for pos in tb)):
        raise ValueError("cria_tabuleiro: argumentos invalidos")
    
    tab = cria_tabuleiro_vazio(n)

    # altera os valores 
    for pos in tp:
        tab[obtem_pos_col(pos)][obtem_pos_lin(pos)] = 1
    
    for pos in tb:
        tab[obtem_pos_col(pos)][obtem_pos_lin(pos)] = -1

    return tab

def obtem_numero_orbitas(tab):
    """
    seleciona o numero de orbitas do tabuleiro.

    Assinatura:
        obtem_numero_orbitas(tab: dict) -> dict
    """
    return tamanho_tab(tab)//2

def cria_copia_tabuleiro(tab):
    """
    constroe copia do tabuleiro.

    Assinatura:
        cria_copia_tabuleiro(tab) -> dict
    """
    copia = {}
    # criar copia coluna por coluna
    for coluna in todas_colunas(obtem_numero_orbitas(tab)):
        col = {}
        # criar coluna posicao por posicao
        for linha in range(1, tamanho_tab(tab) +1):
            col[linha] = tab[coluna][linha]
        copia[coluna] = col

    return copia


def obtem_pedra(tab, pos):
    """
    seleciona a pedra da pos.

    Assinatura:
        obtem_pedra(tab: dict, pos: tuple) -> tuple
    """
    return tab[obtem_pos_col(pos)][obtem_pos_lin(pos)]

def obtem_linha_horizontal(tab, pos):
    """
    seleciona linha horizontal.

    Assinatura:
        obtem_linha_horizontal(tab: dict, pos: tuple) -> tuple
    """
    res = ()
    # pegar todos os elementos da mesma linha
    for coluna in tab:
        res += ((cria_posicao(coluna, obtem_pos_lin(pos)), tab[coluna][obtem_pos_lin(pos)]),)
    
    return res

def obtem_linha_vertical(tab, pos):
    """
    seleciona linha vertical.

    Assinatura:
        obtem_linha_vertical(tab: dict, pos: tuple) -> tuple
    """
    res = ()
    # pegar todos os elementos da mesma coluna
    for linha in range(1, tamanho_tab(tab) + 1):
        res += ((cria_posicao(obtem_pos_col(pos), linha), tab[obtem_pos_col(pos)][linha]),)

    return res

def obtem_linhas_diagonais(tab, pos):
    """
    seleciona linha diagonal e antidiagonal.

    Assinatura:
        obtem_linhas_diagonais(tab: dict, pos: tuple) -> tuple
    """
    diag, anti = (), ()
    # associar variaveis das colunas do tab e da coluna e linha da posicao
    colunas = todas_colunas(obtem_numero_orbitas(tab))
    pos_col, pos_lin = obtem_pos_col(pos), obtem_pos_lin(pos)

    vetor = 0

    # vetor diagonal para cima e esquerda
    while pos_lin + vetor > 0 \
        and chr(ord(pos_col) + vetor) in colunas:

        diag = ((cria_posicao(chr(ord(pos_col) + vetor), pos_lin + vetor),  \
                  tab[chr(ord(pos_col) + vetor)][pos_lin + vetor]),)   \
                       + diag
        
        vetor -= 1

    vetor = 1

    # vetor diagonal para baixo e direita
    while pos_lin + vetor <= tamanho_tab(tab) \
        and chr(ord(pos_col) + vetor) in colunas:

        diag = diag +(((chr(ord(pos_col) + vetor), pos_lin + vetor),  \
                  tab[chr(ord(pos_col) + vetor)][pos_lin + vetor]),)
        
        vetor += 1

    vetor = 0

    # vetor antidiagonal para baixo e esquerda
    while pos_lin + vetor <= tamanho_tab(tab) \
        and chr(ord(pos_col) - vetor) in colunas:

        anti = ((cria_posicao(chr(ord(pos_col) - vetor), pos_lin + vetor),  \
                  tab[chr(ord(pos_col) - vetor)][pos_lin + vetor]),)   \
                       + anti
        
        vetor += 1

    vetor = -1


    # vetor diagonal para cima e direita
    while pos_lin + vetor > 0 \
        and chr(ord(pos_col) - vetor) in colunas:

        anti = anti + ((cria_posicao(chr(ord(pos_col) - vetor),pos_lin + vetor),  \
                  tab[chr(ord(pos_col) - vetor)][pos_lin + vetor]),)
        
        vetor -= 1 

    return (diag, anti)


def obtem_posicoes_pedra(tab, p):
    """
    seleciona as posicoes da pedra.

    Assinatura:
        obtem_posicoes_pedra(tab: dict, p: int) -> tuple
    """
    res = ()
    # posicao por posicao
    for coluna in tab:
        for linha in tab[coluna]:
            if tab[coluna][linha] == p:
                res += (cria_posicao(coluna, linha),)

    return ordena_posicoes(res, obtem_numero_orbitas(tab))

def coloca_pedra(tab, pos, pedra):
    """
    modifica o tabuleiro colocando a pedra na posicao.

    Assinatura:
        coloca_pedra(tab: dict, pos: tuple, pedra: int) -> dict
    """
    tab[pos[0]][pos[1]] = pedra
    return tab

def remove_pedra(tab, pos):
    """
    modifica o tabuleiro removendo a pedra na posicao.

    Assinatura:
        remove_pedra(tab: dict, pos: tuple) -> dict
    """
    tab[obtem_pos_col(pos)][obtem_pos_lin(pos)] = 0
    return tab

def eh_tabuleiro(tab):
    """
    reconhece se é um tabuleiro.

    Assinatura:
        eh_tabuleiro(tab: dict) -> bool
    """
    return (type(tab) == dict and 4 <= len(tab) <= 10 and set(tab) == set(todas_colunas(obtem_numero_orbitas(tab))) \
            and all(type(tab[linhas]) == dict and len(tab[linhas]) == tamanho_tab(tab) == len(todas_colunas(obtem_numero_orbitas(tab))) for linhas in tab))

def tabuleiros_iguais(tab1, tab2):
    """
    testa se os tabuleiros sao iguais.

    Assinatura:
        tabuleiros_iguais(tab1: dict, tab2: dict) -> bool
    """
    return tab1 == tab2

def tabuleiro_para_str(tab):
    """
    transforma o tabuleiro em str.

    Assinatura:
        tabuleiro_para_str(tab: dict) -> str
    """
    res = ""
    # primeira linha indicando as colunas
    colunas = "    " + "   ".join(tab.keys())
    # linha por linha
    for linha in tab["a"]:
        # a primeira linha nao receberá |
        if linha > 1:
            res += "\n" + "    |" + "   |" * (tamanho_tab(tab) - 1)
        if linha < 10:
            res += f"\n0{linha}"
        # a decima linha nao recebe o 0 antes
        if linha >= 10:
            res += f"\n{linha}"
        for coluna in tab:
            # a primeia coluna nao receberá -
            if coluna == "a":
                res += f" [{pedra_para_str(tab[coluna][linha])}]"
            else:
                res += f"-[{pedra_para_str(tab[coluna][linha])}]"

    return colunas + res

def move_pedra(tab, p1, p2):
    """
    retorna um tabuleiro com a pedra de p1 em p2 e p1 vazio.

    Assinatura:
        move_pedra(tab: dict, p1: tuple, p2: tuple) -> dict
    """
    coloca_pedra(tab, p2, obtem_pedra(tab, p1))
    remove_pedra(tab, p1)
    return tab

def diagonais_tabuleiro(tab):
    """
    retorna um tuplo com as posicoes da diagonal e antidiagonal.

    Assinatura:
        diagonais_tabuleiro(tab: dict) -> tuple
    """
    n = obtem_numero_orbitas(tab)
    diagonais = obtem_linhas_diagonais(tab, (todas_colunas(n)[n-1], n))[0] + \
          obtem_linhas_diagonais(tab, (todas_colunas(n)[n], n))[1]
    return tuple(map(lambda x: posicao_para_str(x[0]), diagonais))

def letra_para_numero(l,n):
    """
    retorna um inteiro com o numero da coluna.

    Assinatura:
        letra_para_numero(l:str ,n: int) -> int
    """
    for indice, letra in enumerate(todas_colunas(n)):
        if l == letra:
            return indice + 1


def obtem_posicao_seguinte(tab, pos, boliano):
    """
    retorna a posicao seguinte em sentido horario ou enti-horario.

    Assinatura:
        obtem_posicao_seguinte(tab: dict, pos: tuple, boliano: bool) -> tuple
    """
    # criar variaveis para numero de orbitas, todas as colunas, coluna em numero e diagonais
    n = obtem_numero_orbitas(tab)
    colunas = todas_colunas(n)
    coluna_em_numero = int(letra_para_numero(obtem_pos_col(pos), n))
    diagonais = diagonais_tabuleiro(tab)

    # sentido horario
    if boliano:
        # caso esteja nas diagonais
        if posicao_para_str(pos) in diagonais:
            # diagonais e esquerda
            if coluna_em_numero <= letra_para_numero(colunas[n-1], n):
                # diagonais, esquerda e cima
                if obtem_pos_lin(pos) <= n:
                    return posicao_para_direita(pos)
                # diagonais, esquerda e baixo
                return posicao_para_cima(pos)
            
            # diagonais, direita e cima
            if obtem_pos_lin(pos) <= n:
                return posicao_para_baixo(pos)
            # diagonais, direita e baixo
            return posicao_para_esquerda(pos)  
        
        # caso nao esteja nas diagonais
        # esquerda
        if coluna_em_numero < obtem_pos_lin(pos):
            # esquerda e cima
            if coluna_em_numero < tamanho_tab(tab) - obtem_pos_lin(pos) + 1:
                return posicao_para_cima(pos)
            # esquerda e baixo
            return posicao_para_esquerda(pos)
        
        # direita
        if obtem_pos_lin(pos) < tamanho_tab(tab) - coluna_em_numero + 1:
            # direita e cima
            return posicao_para_direita(pos)
        # direita e baixo
        return posicao_para_baixo(pos)   


    #sentido anti-horario

    # caso esteja nas diagonais
    if posicao_para_str(pos) in diagonais:
        # diagonais e esquerda
        if coluna_em_numero <= letra_para_numero(colunas[n-1], n):
            # diagonais, esquerda e cima
            if obtem_pos_lin(pos) <= n:
                return posicao_para_baixo(pos)
            # diagonais, esquerda e baixo
            return posicao_para_direita(pos)
        
        # diagonais, direita e cima
        if obtem_pos_lin(pos) <= n:
            return posicao_para_esquerda(pos)
        # diagonais, direita e baixo
        return posicao_para_cima(pos)  
    
    # caso nao esteja nas diagonais
    # esquerda
    if coluna_em_numero < obtem_pos_lin(pos):
        # esquerda e cima
        if coluna_em_numero < tamanho_tab(tab) - obtem_pos_lin(pos) + 1:
            return posicao_para_baixo(pos)
        # esquerda e baixo
        return posicao_para_direita(pos)
    
    # direita
    if obtem_pos_lin(pos) < tamanho_tab(tab) - coluna_em_numero + 1:
        # direita e cima
        return posicao_para_esquerda(pos)
    # direita e baixo
    return posicao_para_cima(pos)   

def roda_tabuleiro(tab):
    """
    retorna rodado no sentido anti-horario.

    Assinatura:
        roda_tabuleiro(tab: dict) -> dict
    """
    copia_tab = cria_copia_tabuleiro(tab)
    # se baseia na copia para modificar o anterior
    for coluna in copia_tab:
        for linha in tab[coluna]:
            prox_pos = obtem_posicao_seguinte(copia_tab, cria_posicao(coluna ,linha), True)
            tab[coluna][linha] = copia_tab[obtem_pos_col(prox_pos)][obtem_pos_lin(prox_pos)]
    return tab


def sequencia(tab, linha, pos, p, boliano):
    """
    retorna a maior sequencia da linha que contenha a posicao ou cerca a posicao.

    Assinatura:
        sequencia(tab: dict, linha: tuplo, pos: tuplo, p: int, boliano: bool) -> int
    """
    i = 0
    contagem = 0
    index_pos = linha.index((pos, tab[obtem_pos_col(pos)][obtem_pos_lin(pos)]))

    # caso True ele verifica a posicao 
    if boliano and tab[obtem_pos_col(pos)][obtem_pos_lin(pos)] != p:
        return 0

    # pré posicao
    while index_pos + i >= 0   \
    and linha[index_pos + i][1] == p:
        contagem += 1
        i -= 1

    i = 1

    # pós posicao
    while index_pos + i < len(linha)   \
    and linha[index_pos + i][1] == p:
        contagem += 1
        i += 1

    return contagem

def verifica_linha_pedras(tab, pos, p, k):
    """
    retorna se a maior sequencia da posicao em qualquer uma das listas é igual ou maior que k

    Assinatura:
        verifica_linha_pedras(tab: dict, pos: tuple, p: int, k: int) -> bool
    """
    if sequencia(tab, obtem_linha_horizontal(tab, cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos))), cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)), p, True) >= k \
    or sequencia(tab, obtem_linha_vertical(tab, cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos))), cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)), p, True) >= k \
    or sequencia(tab, obtem_linhas_diagonais(tab, cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)))[0], cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)), p, True) >= k \
    or sequencia(tab, obtem_linhas_diagonais(tab, cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)))[1], cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)), p, True) >= k:
        return True
            
    return False
                


def eh_vencedor(tab, pedra):
    """
    retorna se o jogador com a pedra venceu.

    Assinatura:
        eh_vencedor(tab: dict, pedra: int) -> bool
    """
    for coluna, linha in obtem_posicoes_pedra(tab, pedra):
        if tab[coluna][linha] == pedra and verifica_linha_pedras(tab, cria_posicao(coluna, linha), pedra, tamanho_tab(tab)):
                return True
            
    return False


def eh_fim_jogo(tab):
    """
    retorna se o jogo acabou.

    Assinatura:
        eh_fim_jogo(tab: dict) -> bool
    """
    return eh_vencedor(tab, -1) or eh_vencedor(tab, 1) or not obtem_posicoes_pedra(tab, 0)

def escolhe_movimento_manual(tab):
    """
    retorna a posicao escolhida manualmente pelo jogador.

    Assinatura:
        escolhe_movimento_manual(tab: dict) -> tuple
    """
    while True:
        pos = input("Escolha uma posicao livre:")
        # so aceita a posicao escolhida caso
        if pos and type(pos) == str and len(pos) == 2 and obtem_pos_col(pos) in todas_colunas(obtem_numero_orbitas(tab)) and pos[1].isdigit() \
            and 1 <= int(obtem_pos_lin(pos)) <= tamanho_tab(tab) and cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos)) in obtem_posicoes_pedra(tab,0):
            break

    return cria_posicao(obtem_pos_col(pos), obtem_pos_lin(pos))

def escolha_posicao_facil(tab, jog):
    """
    retorna a posicao escolhida no modo facil.

    Assinatura:
        escolha_posicao_facil(tab: dict, jog: int) -> tuple
    """
    n = obtem_numero_orbitas(tab)
    tab_modificado = roda_tabuleiro(cria_copia_tabuleiro(tab))
    posicoes = []
    # posicoes livres apos rodar o tabuleiro
    for pos_livre in obtem_posicoes_pedra(tab_modificado, 0):
        for pos_adjacente in obtem_posicoes_adjacentes(pos_livre, n, True):
            # caso alguma das posicoes adjacentes tenha uma pedra propia, acrescentar a pos livre original 
            if tab[obtem_pos_col(pos_adjacente)][obtem_pos_lin(pos_adjacente)] == jog:
                posicoes += [obtem_posicao_seguinte(tab_modificado, pos_livre, True)]


    # ordenar as posicoes pretentendes e retornar a primeira na ordem de leitura
    if posicoes:
        return ordena_posicoes(posicoes, n)[0]

    return ordena_posicoes(obtem_posicoes_pedra(tab, 0), n)[0]

def maior_sequencia_na_posicao(tab, pos, jog):
    """
    retorna um inteiro com a maior sequencia, verificando todas as linhas, que se teria colocando uma pedra naquela posicao.

    Assinatura:
        maior_sequencia_na_posicao(tab: dict, pos: tuple, jog: int) -> int
    """
    horiz = obtem_linha_horizontal(tab, pos)
    vert = obtem_linha_vertical(tab, pos)
    diag, anti = obtem_linhas_diagonais(tab, pos)

    maior = 0
    # verifica a maior sequencia por linha
    for linha in [horiz, vert, diag, anti]:
        seq = sequencia(tab, linha, pos, jog, False)
        if seq > maior:
            maior = seq

    return maior 
    


def obtem_maior_l(tab, jog, boliano):
    """
    retorna um inteiro com a maior sequencia possivel obtivel no presente tabuleiro.

    Assinatura:
        obtem_maior_l(tab: dict, jog: int, boliano: bool) -> int
    """
    resp = []
    posicoes_livres = obtem_posicoes_pedra(tab, 0)
    tab_modificado = roda_tabuleiro(cria_copia_tabuleiro(tab))
    # caso for checar o L do adversario tem que rodar uma vez mais
    if boliano:
        tab_modificado = roda_tabuleiro(cria_copia_tabuleiro(tab_modificado))
    # para posicao livre
    for pos_livre in obtem_posicoes_pedra(tab_modificado, 0):
        tab_modificado = coloca_pedra(tab_modificado, pos_livre, jog)
        pos_original = obtem_posicao_seguinte(tab_modificado, pos_livre, True)
        # caso for checar o L do adversario tem que voltar uma vez mais 
        if boliano:
            pos_original = obtem_posicao_seguinte(tab_modificado, pos_original, True)
        # acrescentar a posicao original e seu L
        resp += ((pos_original, maior_sequencia_na_posicao(tab_modificado, pos_livre, jog)),)
        tab_modificado = remove_pedra(tab_modificado, pos_livre)

    # ordenar primeiro por L e depois pela ordem de leitura
    return sorted(resp, key = lambda x: (-x[1], posicoes_livres.index(x[0])))[0]


def escolha_posicao_normal(tab, jog):
    """
    retorna a posicao escolhida no modo normal.

    Assinatura:
        escolha_posicao_normal(tab: dict, jog: int) -> int
    """
    maior_l_jog = obtem_maior_l(tab, jog, False)
    maior_l_adversario = obtem_maior_l(tab, -jog, True)
    # se o L proprio for maior que o L adversario, jogar no proprio, caso contrario jogar no adversario
    if maior_l_jog[1] >= maior_l_adversario[1]:
        return maior_l_jog[0]
    return maior_l_adversario[0]

def escolhe_movimento_auto(tab, jog, lvl):
    """
    retorna a posicao pelo computador dependendo do lvl e do jogador.

    Assinatura:
        escolhe_movimento_auto(tab: dict, jog: int, lvl: str) -> int
    """
    leveis = {"facil": escolha_posicao_facil, "normal": escolha_posicao_normal}
    return leveis[lvl](tab, jog)

def jog_para_pedra(jog):
    """
    retorna o jogador em forma de pedra.

    Assinatura:
        jog_para_pedra(jog: str) -> int
    """
    jogadores = {"X": 1, "O": -1}
    return jogadores[jog]

def orbito(n, modo, jog):
    """
    joga o jogo e retorna o jogador ganhador.

    Assinatura:
        orbito(n: int, modo: str, jog; str) -> int
    """
    modos = {"facil", "normal", "2jogadores"}
    jogadores = {"O", "X"}
    if not (type(n) == int and 2 <= n <= 5 and type(modo) == str and modo in modos and type(jog) == str and jog in jogadores):
        raise ValueError("orbito: argumentos invalidos")
    
    tab = cria_tabuleiro_vazio(n)
    pedra = jog_para_pedra(jog)

    print(f"Bem-vindo ao ORBITO-{n}.")

    # modo 2 jogadors
    if modo == "2jogadores":
        print("Jogo para dois jogadores.")
        print(tabuleiro_para_str(tab))
        while True:
            print("Turno do jogador 'X'.")
            # coloca a pedra e roda o tabuleiro
            pos = escolhe_movimento_manual(tab)
            tab = coloca_pedra(tab, pos, 1)
            tab = roda_tabuleiro(tab)
            print(tabuleiro_para_str(tab))    
            x_venc = eh_vencedor(tab, 1)
            o_venc = eh_vencedor(tab, -1)
            # verifica se o jogo acabou
            if (x_venc and o_venc) or not obtem_posicoes_pedra(tab, 0):
                print("EMPATE")
                return pedra_para_int(0)
            if x_venc:
                print("VITORIA DO JOGADOR 'X'")
                return pedra_para_int(1)
            if o_venc:
                print("VITORIA DO JOGADOR 'O'")
                return pedra_para_int(-1)       
            print("Turno do jogador 'O'.")
            # coloca a pedra e roda o tabuleiro
            pos = escolhe_movimento_manual(tab)
            tab = coloca_pedra(tab, pos, -1)
            tab = roda_tabuleiro(tab)
            print(tabuleiro_para_str(tab))    
            x_venc = eh_vencedor(tab, 1)
            o_venc = eh_vencedor(tab, -1)
            # verifica se o jogo acabou
            if (x_venc and o_venc) or not obtem_posicoes_pedra(tab, 0):
                print("EMPATE")
                return pedra_para_int(0)
            if x_venc:
                print("VITORIA DO JOGADOR 'X'")
                return pedra_para_int(1)
            if o_venc:
                print("VITORIA DO JOGADOR 'O'")
                return pedra_para_int(-1)   
             



    print(f"Jogo contra o computador ({modo}).")
    print(f"O jogador joga com '{pedra_para_str(pedra)}'.")
    print(tabuleiro_para_str(tab))
    # caso o jogador comece jogando
    if pedra == 1:
            print("Turno do jogador.")
            pos = escolhe_movimento_manual(tab)
            tab = coloca_pedra(tab, pos, pedra)
            tab = roda_tabuleiro(tab)
            print(tabuleiro_para_str(tab))

    while True:
        print(f"Turno do computador ({modo}):")
        # coloca a pedra e roda o tabuleiro
        pos = escolhe_movimento_auto(tab, -pedra, modo)
        tab = coloca_pedra(tab, pos, -pedra)
        tab = roda_tabuleiro(tab)
        print(tabuleiro_para_str(tab))
        adversario_venc = eh_vencedor(tab, -pedra)
        jog_venc = eh_vencedor(tab, pedra)
        # verifica se o jogo acabou
        if (adversario_venc and jog_venc) or not obtem_posicoes_pedra(tab, 0):
            print("EMPATE")
            return pedra_para_int(0)
        if jog_venc:
            print("VITORIA")
            return pedra_para_int(pedra)
        if adversario_venc:
            print("DERROTA")
            return pedra_para_int(-pedra)
        print("Turno do jogador.")
        # coloca a pedra e roda o tabuleiro
        pos = escolhe_movimento_manual(tab)
        tab = coloca_pedra(tab, pos, pedra)
        tab = roda_tabuleiro(tab)
        print(tabuleiro_para_str(tab))            
        adversario_venc = eh_vencedor(tab, -pedra)
        jog_venc = eh_vencedor(tab, pedra)
        # verifica se o jogo acabou
        if (adversario_venc and jog_venc) or not obtem_posicoes_pedra(tab, 0):
            print("EMPATE")
            return pedra_para_int(0)
        if jog_venc:
            print("VITORIA")
            return pedra_para_int(pedra)
        if adversario_venc:
            print("DERROTA")
            return pedra_para_int(-pedra)


