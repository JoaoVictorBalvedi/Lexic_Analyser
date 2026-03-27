# Grupo: <RA1 22>
# Integrante:
# João Victor Balvedi - @JoaoVictorBalvedi


# --- Funcoes auxiliares do automato ---

def fimDeToken(c):
    # Retorna True se o caractere indica o fim de um token
    return c is None or c.isspace() or c in "()"


# --- Estados do Automato Finito Determinístico ---

def estadoNumero(linha, i):
    # Estado: lendo um numero real (ex: 3.14, 9, 2.0)
    # Subestados: inteiro -> decimal_obrigatorio -> decimal
    inicio = i
    estado = "inteiro"

    while i < len(linha):
        c = linha[i]

        if estado == "inteiro":
            if c.isdigit():
                i += 1
            elif c == ".":
                estado = "decimal_obrigatorio"
                i += 1
            else:
                break

        elif estado == "decimal_obrigatorio":
            if c.isdigit():
                estado = "decimal"
                i += 1
            else:
                raise ValueError(
                    f"Numero invalido: ponto sem digitos depois em '{linha[inicio:i]}'"
                )

        elif estado == "decimal":
            if c.isdigit():
                i += 1
            elif c == ".":
                raise ValueError(
                    f"Numero invalido: mais de um ponto em '{linha[inicio:i+1]}'"
                )
            else:
                break

    if estado == "decimal_obrigatorio":
        raise ValueError(
            f"Numero invalido: ponto sem parte decimal em '{linha[inicio:i]}'"
        )

    lexema = linha[inicio:i]
    return ("NUMBER", lexema), i


OPERADORES_SIMPLES = {"+", "-", "*", "/", "%", "^"}


def estadoOperador(linha, i):
    # Estado: lendo um operador aritmetico (+, -, *, /, //, %, ^)
    inicio = i
    c = linha[i]
    prox = linha[i + 1] if i + 1 < len(linha) else None

    # Verifica operador de dois caracteres '//'
    if c == "/" and prox == "/":
        depois = linha[i + 2] if i + 2 < len(linha) else None
        if fimDeToken(depois):
            return ("OPERATOR", "//"), i + 2
        raise ValueError(f"Operador invalido: '{linha[inicio:i+2]}'")

    # Verifica operadores simples de um caractere
    if c in OPERADORES_SIMPLES:
        if fimDeToken(prox):
            return ("OPERATOR", c), i + 1
        raise ValueError(f"Operador invalido: '{c}{prox}'")

    raise ValueError(f"Operador invalido: '{c}'")


def estadoParenteses(linha, i):
    # Estado: lendo um parentese de abertura ou fechamento
    c = linha[i]

    if c == "(":
        return ("LPAREN", c), i + 1
    elif c == ")":
        return ("RPAREN", c), i + 1

    raise ValueError(f"Parentese invalido: '{c}'")


def estadoPalavra(linha, i):
    # Estado: lendo uma palavra em maiusculas (MEM, RES, VAR, X, etc.)
    inicio = i

    while i < len(linha) and (linha[i].isupper() or linha[i].isdigit() or linha[i] == "_"):
        i += 1

    lexema = linha[inicio:i]

    if lexema == "":
        raise ValueError(f"Token invalido em '{linha[inicio:]}'")

    prox = linha[i] if i < len(linha) else None

    if not fimDeToken(prox):
        raise ValueError(f"Palavra invalida: '{linha[inicio:i+1]}'")

    # Palavras reservadas da linguagem
    if lexema == "MEM":
        return ("MEM", lexema), i
    elif lexema == "RES":
        return ("RES", lexema), i
    else:
        return ("IDENTIFIER", lexema), i


# --- Funcao principal do analisador lexico ---

def parseExpressao(linha):
    """
    Recebe uma linha de texto com uma expressao RPN e retorna
    uma lista de tokens no formato (TIPO, valor).
    Lanca ValueError se encontrar token invalido ou parenteses desbalanceados.
    """
    tokens = []
    profundidade = 0  # controla balanceamento de parenteses
    i = 0

    while i < len(linha):
        caractere = linha[i]

        if caractere.isspace():
            i += 1

        elif caractere in "()":
            token, i = estadoParenteses(linha, i)

            # Atualiza profundidade e verifica fechamento indevido
            if token[0] == "LPAREN":
                profundidade += 1
            else:
                profundidade -= 1
                if profundidade < 0:
                    raise ValueError("Parentese fechado sem abertura correspondente")

            tokens.append(token)

        elif caractere.isdigit():
            token, i = estadoNumero(linha, i)
            tokens.append(token)

        elif caractere in "+-*/%^":
            token, i = estadoOperador(linha, i)
            tokens.append(token)

        elif caractere.isupper():
            token, i = estadoPalavra(linha, i)
            tokens.append(token)

        else:
            raise ValueError(f"Caractere invalido: '{caractere}'")

    # Verifica se todos os parenteses foram fechados
    if profundidade != 0:
        raise ValueError(f"Parenteses nao balanceados: faltam {profundidade} fechamento(s)")

    return tokens