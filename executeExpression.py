# Grupo: <RA1 22>
# Integrante:
# João Victor Balvedi - @JoaoVictorBalvedi


# --- Funcoes que criam nos da arvore (AST) ---

def criarNoNumero(valor):
    return {
        "tipo": "numero",
        "valor": valor
    }


def criarNoMemLeitura():
    # No para leitura da memoria especial: (MEM)
    return {
        "tipo": "mem_leitura"
    }


def criarNoMemEscrita(valor):
    # No para escrita na memoria especial: (V MEM)
    return {
        "tipo": "mem_escrita",
        "valor": valor
    }


def criarNoRes(indice):
    # No para referencia a resultado anterior: (N RES)
    return {
        "tipo": "res",
        "indice": int(indice)
    }


def criarNoOperacao(operador, esquerda, direita):
    return {
        "tipo": "operacao",
        "operador": operador,
        "esquerda": esquerda,
        "direita": direita
    }


def criarNoVarLeitura(nome):
    # No para leitura de variavel nomeada: (VAR)
    return {
        "tipo": "var_leitura",
        "nome": nome
    }


def criarNoVarEscrita(nome, valor):
    # No para escrita em variavel nomeada: (V VAR)
    return {
        "tipo": "var_escrita",
        "nome": nome,
        "valor": valor
    }


# --- Funcoes de analise da estrutura de tokens ---

def lerElemento(tokens, i):
    """
    Le um elemento simples (numero, MEM, variavel) ou
    uma sub-expressao completa (comecando com '(').
    Retorna (no, proximo_indice).
    """
    if i >= len(tokens):
        raise ValueError("Fim inesperado da expressao")

    tipo, valor = tokens[i]

    if tipo == "NUMBER":
        return criarNoNumero(valor), i + 1

    elif tipo == "IDENTIFIER":
        # Identificador solto como operando (ex: VAR dentro de operacao)
        return criarNoVarLeitura(valor), i + 1

    elif tipo == "MEM":
        # MEM como operando dentro de uma expressao (ex: (MEM 2.0 +))
        return criarNoMemLeitura(), i + 1

    elif tipo == "LPAREN":
        return analisarEstrutura(tokens, i)

    else:
        raise ValueError(f"Elemento invalido: {tokens[i]}")


def analisarEstrutura(tokens, i=0):
    """
    Analisa uma expressao completa entre parenteses.
    Reconhece: operacoes, (MEM), (V MEM), (N RES), (VAR), (V VAR).
    Retorna (no, proximo_indice).
    """
    if i >= len(tokens):
        raise ValueError("Fim inesperado dos tokens")

    if tokens[i][0] != "LPAREN":
        raise ValueError("Era esperado '(' no inicio da expressao")

    i += 1  # consome o '('

    if i >= len(tokens):
        raise ValueError("Expressao incompleta apos '('")

    # Caso especial: (MEM) — leitura da memoria especial sem operandos
    # Verificamos se eh so MEM seguido de ')' para distinguir de (MEM 2.0 +)
    if tokens[i][0] == "MEM":
        if i + 1 < len(tokens) and tokens[i + 1][0] == "RPAREN":
            # Eh o caso (MEM) — leitura simples
            return criarNoMemLeitura(), i + 2
        # Caso contrario, MEM eh o operando esquerdo de uma operacao
        # Ex: (MEM 2.0 +) — cai no fluxo normal abaixo

    # Caso especial: (IDENTIFIER) — leitura de variavel nomeada ex: (VAR)
    if tokens[i][0] == "IDENTIFIER":
        nome = tokens[i][1]
        if i + 1 < len(tokens) and tokens[i + 1][0] == "RPAREN":
            return criarNoVarLeitura(nome), i + 2
        # Caso contrario, o IDENTIFIER eh o operando esquerdo — cai no fluxo normal

    # Leitura do primeiro operando (pode ser numero, MEM, sub-expressao, etc.)
    esquerda, i = lerElemento(tokens, i)

    if i >= len(tokens):
        raise ValueError("Expressao incompleta apos primeiro elemento")

    # Verifica se eh comando (V MEM) — escrita na memoria especial
    if tokens[i][0] == "MEM":
        i += 1
        if i >= len(tokens) or tokens[i][0] != "RPAREN":
            raise ValueError("Era esperado ')' apos comando MEM")
        return criarNoMemEscrita(esquerda), i + 1

    # Verifica se eh comando (N RES) — referencia a resultado anterior
    if tokens[i][0] == "RES":
        if esquerda["tipo"] != "numero":
            raise ValueError("RES deve receber um numero como indice")
        i += 1
        if i >= len(tokens) or tokens[i][0] != "RPAREN":
            raise ValueError("Era esperado ')' apos comando RES")
        return criarNoRes(esquerda["valor"]), i + 1

    # Verifica se eh comando (V VAR) — escrita em variavel nomeada
    if tokens[i][0] == "IDENTIFIER":
        nome = tokens[i][1]
        i += 1
        if i >= len(tokens) or tokens[i][0] != "RPAREN":
            raise ValueError("Era esperado ')' apos nome da variavel")
        return criarNoVarEscrita(nome, esquerda), i + 1

    # Caso geral: operacao binaria (A B op)
    direita, i = lerElemento(tokens, i)

    if i >= len(tokens):
        raise ValueError("Faltou operador no final da expressao")

    if tokens[i][0] != "OPERATOR":
        raise ValueError(f"Era esperado operador, mas veio {tokens[i]}")

    operador = tokens[i][1]
    i += 1

    if i >= len(tokens) or tokens[i][0] != "RPAREN":
        raise ValueError("Era esperado ')' ao final da operacao")

    return criarNoOperacao(operador, esquerda, direita), i + 1


def executarExpressao(tokens, memoria=None, resultados=None):
    """
    Recebe os tokens de uma expressao e retorna um dicionario com:
    - estrutura: a arvore (AST) da expressao
    - memoria: dicionario de variaveis (compartilhado entre chamadas)
    - resultados: lista de estruturas anteriores (compartilhada entre chamadas)
    """
    if memoria is None:
        memoria = {}

    if resultados is None:
        resultados = []

    estrutura, proximo = analisarEstrutura(tokens)

    if proximo != len(tokens):
        raise ValueError("Sobraram tokens apos o fim da expressao")

    return {
        "estrutura": estrutura,
        "memoria": memoria,
        "resultados": resultados
    }