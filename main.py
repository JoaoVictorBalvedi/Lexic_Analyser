from executeExpression import executarExpressao
from generateAssembly import gerarAssembly

def lerArquivo(nomeArquivo, linhas=None):
    linhasArquivo = []

    with open(nomeArquivo, 'r') as arquivo:
        if linhas is None:
            for linha in arquivo:
                linha = linha.strip()
                if linha != "":
                    linhasArquivo.append(linha)
        else:
            for _ in range(linhas):
                linha = arquivo.readline()

                if not linha:
                    break

                linha = linha.strip()
                if linha != "":
                    linhasArquivo.append(linha)

    return linhasArquivo

def fimDeToken(c):
    return c is None or c.isspace() or c in "()"

def estadoNumero(linha, i):
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
                raise ValueError(f"Número inválido: ponto sem dígitos depois em '{linha[inicio:i]}'")

        elif estado == "decimal":
            if c.isdigit():
                i += 1
            elif c == ".":
                raise ValueError(f"Número inválido: mais de um ponto em '{linha[inicio:i+1]}'")
            else:
                break

    if estado == "decimal_obrigatorio":
        raise ValueError(f"Número inválido: ponto sem parte decimal em '{linha[inicio:i]}'")

    lexema = linha[inicio:i]
    return ("NUMBER", lexema), i

OPERADORES_SIMPLES = {"+", "-", "*", "/", "%", "^"}

def estadoOperador(linha, i):
    inicio = i
    c = linha[i]
    prox = linha[i + 1] if i + 1 < len(linha) else None

    if c == "/" and prox == "/":
        depois = linha[i + 2] if i + 2 < len(linha) else None
        if fimDeToken(depois):
            return ("OPERATOR", "//"), i + 2
        raise ValueError(f"Operador inválido: '{linha[inicio:i+2]}'")

    if c in OPERADORES_SIMPLES:
        if fimDeToken(prox):
            return ("OPERATOR", c), i + 1
        raise ValueError(f"Operador inválido: '{c}{prox}'")

    raise ValueError(f"Operador inválido: '{c}'")

def estadoParenteses(linha, i):
    c = linha[i]

    if c == "(":
        return ("LPAREN", c), i + 1
    elif c == ")":
        return ("RPAREN", c), i + 1

    raise ValueError(f"Parêntese inválido: '{c}'")
    
def estadoEspaco(i):
    return i + 1

def estadoPalavra(linha, i):
    inicio = i

    while i < len(linha) and (linha[i].isupper() or linha[i].isdigit() or linha[i] == "_"):
        i += 1

    lexema = linha[inicio:i]

    if lexema == "":
        raise ValueError(f"Token inválido em '{linha[inicio:]}'")

    prox = linha[i] if i < len(linha) else None

    if not fimDeToken(prox):
        raise ValueError(f"Palavra inválida: '{linha[inicio:i+1]}'")

    if lexema == "MEM":
        return ("MEM", lexema), i
    elif lexema == "RES":
        return ("RES", lexema), i
    else:
        return ("IDENTIFIER", lexema), i

def parseExpressao(linha):
    tokens = []
    i = 0

    while i < len(linha):
        caractere = linha[i]

        if caractere.isspace():
            i = estadoEspaco(i)
        elif caractere in "()":
            token, i = estadoParenteses(linha, i)
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
            raise ValueError(f"Caractere inválido: {caractere}")
        
    return tokens

linhasArquivo = lerArquivo("teste1.txt", 12)
primeiraLinha = linhasArquivo[0]
i = 0
while i < len(linhasArquivo):
    tokens = parseExpressao(linhasArquivo[i])
    print("TOKENS:")
    print(tokens)

    expressao = executarExpressao(tokens)
    print("ESTRUTURA:")
    print(expressao["estrutura"])

    codigo = gerarAssembly(tokens)
    print("\nASSEMBLY:")
    print(codigo)
    i += 1