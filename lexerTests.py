# Grupo: <RA1 22>
# Integrante:
# João Victor Balvedi - @JoaoVictorBalvedi

from parser import parseExpressao


# -------------------------------------------------------
# Funcoes auxiliares de teste
# -------------------------------------------------------

def testarValido(descricao, entrada, esperado):
    """
    Testa uma entrada valida.
    Verifica se os tokens gerados sao iguais ao esperado.
    """
    try:
        resultado = parseExpressao(entrada)
        if resultado == esperado:
            print(f"  [OK] {descricao}")
        else:
            print(f"  [FALHOU] {descricao}")
            print(f"           Esperado : {esperado}")
            print(f"           Obtido   : {resultado}")
    except Exception as e:
        print(f"  [ERRO INESPERADO] {descricao}: {e}")


def testarInvalido(descricao, entrada):
    """
    Testa uma entrada invalida.
    Espera que parseExpressao lance ValueError.
    """
    try:
        resultado = parseExpressao(entrada)
        print(f"  [FALHOU] {descricao} — deveria ter dado erro, mas retornou: {resultado}")
    except ValueError as e:
        print(f"  [OK] {descricao} — erro detectado: {e}")


# -------------------------------------------------------
# Testes de entradas VALIDAS
# -------------------------------------------------------

def testesValidos():
    print("\n=== TESTES VALIDOS ===")

    testarValido(
        "Soma simples",
        "(3.14 2.0 +)",
        [("LPAREN","("), ("NUMBER","3.14"), ("NUMBER","2.0"), ("OPERATOR","+"), ("RPAREN",")")]
    )

    testarValido(
        "Subtracao",
        "(10.0 4.0 -)",
        [("LPAREN","("), ("NUMBER","10.0"), ("NUMBER","4.0"), ("OPERATOR","-"), ("RPAREN",")")]
    )

    testarValido(
        "Multiplicacao",
        "(2.0 3.0 *)",
        [("LPAREN","("), ("NUMBER","2.0"), ("NUMBER","3.0"), ("OPERATOR","*"), ("RPAREN",")")]
    )

    testarValido(
        "Divisao real",
        "(9.0 3.0 /)",
        [("LPAREN","("), ("NUMBER","9.0"), ("NUMBER","3.0"), ("OPERATOR","/"), ("RPAREN",")")]
    )

    testarValido(
        "Divisao inteira",
        "(9.0 2.0 //)",
        [("LPAREN","("), ("NUMBER","9.0"), ("NUMBER","2.0"), ("OPERATOR","//"), ("RPAREN",")")]
    )

    testarValido(
        "Resto da divisao",
        "(9.0 2.0 %)",
        [("LPAREN","("), ("NUMBER","9.0"), ("NUMBER","2.0"), ("OPERATOR","%"), ("RPAREN",")")]
    )

    testarValido(
        "Potenciacao",
        "(2.0 3.0 ^)",
        [("LPAREN","("), ("NUMBER","2.0"), ("NUMBER","3.0"), ("OPERATOR","^"), ("RPAREN",")")]
    )

    testarValido(
        "Comando RES",
        "(5 RES)",
        [("LPAREN","("), ("NUMBER","5"), ("RES","RES"), ("RPAREN",")")]
    )

    testarValido(
        "Comando MEM leitura",
        "(MEM)",
        [("LPAREN","("), ("MEM","MEM"), ("RPAREN",")")]
    )

    testarValido(
        "Comando MEM escrita",
        "(10.5 MEM)",
        [("LPAREN","("), ("NUMBER","10.5"), ("MEM","MEM"), ("RPAREN",")")]
    )

    testarValido(
        "Variavel nomeada escrita",
        "(10.5 CONTADOR)",
        [("LPAREN","("), ("NUMBER","10.5"), ("IDENTIFIER","CONTADOR"), ("RPAREN",")")]
    )

    testarValido(
        "Variavel nomeada leitura",
        "(CONTADOR)",
        [("LPAREN","("), ("IDENTIFIER","CONTADOR"), ("RPAREN",")")]
    )

    testarValido(
        "Expressao aninhada",
        "((2.0 3.0 *) 4.0 +)",
        [
            ("LPAREN","("),
            ("LPAREN","("), ("NUMBER","2.0"), ("NUMBER","3.0"), ("OPERATOR","*"), ("RPAREN",")"),
            ("NUMBER","4.0"), ("OPERATOR","+"),
            ("RPAREN",")")
        ]
    )

    testarValido(
        "Numero inteiro sem ponto",
        "(5 RES)",
        [("LPAREN","("), ("NUMBER","5"), ("RES","RES"), ("RPAREN",")")]
    )

    testarValido(
        "MEM como operando em operacao",
        "(MEM 2.0 +)",
        [("LPAREN","("), ("MEM","MEM"), ("NUMBER","2.0"), ("OPERATOR","+"), ("RPAREN",")")]
    )


# -------------------------------------------------------
# Testes de entradas INVALIDAS
# -------------------------------------------------------

def testesInvalidos():
    print("\n=== TESTES INVALIDOS ===")

    testarInvalido(
        "Operador invalido &",
        "(3.14 2.0 &)"
    )

    testarInvalido(
        "Numero com dois pontos (3.14.5)",
        "(3.14.5 2.0 +)"
    )

    testarInvalido(
        "Numero com virgula como decimal (3,45)",
        "(3,45 2.0 +)"
    )

    testarInvalido(
        "Ponto sem digito depois (3.)",
        "(3. 2.0 +)"
    )

    testarInvalido(
        "Parentese de fechamento sem abertura",
        "3.14 2.0 +)"
    )

    testarInvalido(
        "Parentese de abertura sem fechamento",
        "(3.14 2.0 +"
    )

    testarInvalido(
        "Caractere especial no meio",
        "(3.14 @ 2.0 +)"
    )

    testarInvalido(
        "Letra minuscula como token",
        "(3.14 2.0 add)"
    )

    testarInvalido(
        "Operador duplo invalido (/+)",
        "(3.0 2.0 /+)"
    )

    testarInvalido(
        "Parenteses extras desbalanceados",
        "((3.0 2.0 +)"
    )


# -------------------------------------------------------
# Execucao
# -------------------------------------------------------

if __name__ == "__main__":
    testesValidos()
    testesInvalidos()
    print("\nTestes concluidos.")