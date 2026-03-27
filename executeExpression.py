def criarNoNumero(valor):
    return {
        "tipo": "numero",
        "valor": valor
    }

def criarNoIdentificador(nome):
    return {
        "tipo": "identificador",
        "valor": nome
    }

def criarNoMemLeitura():
    return {
        "tipo": "mem_leitura"
    }

def criarNoMemEscrita(valor):
    return {
        "tipo": "mem_escrita",
        "valor": valor
    }

def criarNoRes(indice):
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

def lerElemento(tokens, i):
    if i >= len(tokens):
        raise ValueError("Fim inesperado da expressão")

    tipo, valor = tokens[i]

    if tipo == "NUMBER":
        return criarNoNumero(valor), i + 1

    elif tipo == "IDENTIFIER":
        return criarNoIdentificador(valor), i + 1

    elif tipo == "MEM":
        return criarNoMemLeitura(), i + 1

    elif tipo == "LPAREN":
        return analisarEstrutura(tokens, i)

    else:
        raise ValueError(f"Elemento inválido: {tokens[i]}")
    
def analisarEstrutura(tokens, i=0):
    if i >= len(tokens):
        raise ValueError("Fim inesperado dos tokens")

    if tokens[i][0] != "LPAREN":
        raise ValueError("Era esperado '(' no início da expressão")

    i += 1

    if i >= len(tokens):
        raise ValueError("Expressão incompleta")

    if tokens[i][0] == "MEM":
        i += 1

        if i >= len(tokens) or tokens[i][0] != "RPAREN":
            raise ValueError("Era esperado ')' após MEM")

        return criarNoMemLeitura(), i + 1

    esquerda, i = lerElemento(tokens, i)

    if i >= len(tokens):
        raise ValueError("Expressão incompleta após o primeiro elemento")

    if tokens[i][0] == "MEM":
        i += 1

        if i >= len(tokens) or tokens[i][0] != "RPAREN":
            raise ValueError("Era esperado ')' após comando MEM")

        return criarNoMemEscrita(esquerda), i + 1

    if tokens[i][0] == "RES":
        if esquerda["tipo"] != "numero":
            raise ValueError("RES deve receber um número como índice")

        i += 1

        if i >= len(tokens) or tokens[i][0] != "RPAREN":
            raise ValueError("Era esperado ')' após comando RES")

        return criarNoRes(esquerda["valor"]), i + 1

    direita, i = lerElemento(tokens, i)

    if i >= len(tokens):
        raise ValueError("Faltou operador no final da expressão")

    if tokens[i][0] != "OPERATOR":
        raise ValueError(f"Era esperado operador, mas veio {tokens[i]}")

    operador = tokens[i][1]
    i += 1

    if i >= len(tokens) or tokens[i][0] != "RPAREN":
        raise ValueError("Era esperado ')' ao final da operação")

    return criarNoOperacao(operador, esquerda, direita), i + 1

def executarExpressao(tokens, memoria=None, resultados=None):
    if memoria is None:
        memoria = {}

    if resultados is None:
        resultados = []

    estrutura, proximo = analisarEstrutura(tokens)

    if proximo != len(tokens):
        raise ValueError("Sobraram tokens após o fim da expressão")

    infoExecucao = {
        "estrutura": estrutura,
        "memoria": memoria,
        "resultados": resultados
    }

    return infoExecucao