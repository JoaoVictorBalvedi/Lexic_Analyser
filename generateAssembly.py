# Grupo: <nome do grupo no Canvas>
# Integrantes (ordem alfabetica):
#   Aluno 1 - @github1
#   Aluno 2 - @github2
#   Aluno 3 - @github3
#   Aluno 4 - @github4


def registrarConstante(valor, contexto):
    """Registra uma constante no contexto e retorna seu rotulo."""
    if valor not in contexto["constantes"]:
        rotulo = f"const_{len(contexto['constantes'])}"
        contexto["constantes"][valor] = rotulo
    return contexto["constantes"][valor]


def registrarVariavel(nome, contexto):
    """Registra uma variavel nomeada no contexto e retorna seu rotulo."""
    if nome not in contexto["variaveis"]:
        rotulo = f"var_{nome}"
        contexto["variaveis"][nome] = rotulo
    return contexto["variaveis"][nome]


def gerarCodigoNo(no, contexto):
    """
    Gera as instrucoes Assembly para um no da arvore.
    O resultado fica sempre em d0 ao final.
    contexto["indice_atual"] contem o indice da expressao sendo gerada,
    necessario para calcular o rotulo correto do comando RES.
    """
    tipo = no["tipo"]
    codigo = []

    if tipo == "numero":
        # Carrega constante de 64 bits da secao .data para d0
        rotulo = registrarConstante(no["valor"], contexto)
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "mem_leitura":
        # Carrega o valor da memoria especial MEM para d0
        codigo.append("LDR r0, =mem_slot")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "mem_escrita":
        # Calcula o valor e salva na memoria especial MEM
        codigo.extend(gerarCodigoNo(no["valor"], contexto))
        codigo.append("LDR r0, =mem_slot")
        codigo.append("VSTR.F64 d0, [r0]")

    elif tipo == "res":
        # (N RES): carrega o resultado de N linhas atras
        # indice_alvo = indice_atual - N
        indice_alvo = contexto["indice_atual"] - no["indice"]
        if indice_alvo < 0:
            raise ValueError(
                f"RES({no['indice']}): nao ha resultado suficiente (expressao {contexto['indice_atual']})"
            )
        codigo.append(f"LDR r0, =result_{indice_alvo}")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "var_leitura":
        # Carrega variavel nomeada (ex: VAR, X) para d0
        rotulo = registrarVariavel(no["nome"], contexto)
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VLDR.F64 d0, [r0]")

    elif tipo == "var_escrita":
        # Calcula o valor e salva em variavel nomeada
        rotulo = registrarVariavel(no["nome"], contexto)
        codigo.extend(gerarCodigoNo(no["valor"], contexto))
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VSTR.F64 d0, [r0]")

    elif tipo == "operacao":
        # Avalia esquerda, empilha, avalia direita, desempilha, opera
        # Apos: d1 = esquerda, d0 = direita
        codigo.extend(gerarCodigoNo(no["esquerda"], contexto))
        codigo.append("VPUSH {d0}")

        codigo.extend(gerarCodigoNo(no["direita"], contexto))
        codigo.append("VPOP {d1}")

        operador = no["operador"]

        if operador == "+":
            codigo.append("VADD.F64 d0, d1, d0")
        elif operador == "-":
            codigo.append("VSUB.F64 d0, d1, d0")
        elif operador == "*":
            codigo.append("VMUL.F64 d0, d1, d0")
        elif operador == "/":
            codigo.append("VDIV.F64 d0, d1, d0")
        elif operador == "//":
            # Divisao inteira: usa rotina auxiliar
            # Antes do BL: d1=dividendo, d0=divisor
            contexto["usa_div_int"] = True
            codigo.append("BL div_int_double")
        elif operador == "%":
            # Resto da divisao inteira: usa rotina auxiliar
            contexto["usa_mod_int"] = True
            codigo.append("BL mod_int_double")
        elif operador == "^":
            # Potenciacao com expoente inteiro: usa rotina auxiliar
            # Antes do BL: d1=base, d0=expoente
            contexto["usa_pow_int"] = True
            codigo.append("BL pow_int_double")
        else:
            raise ValueError(f"Operador desconhecido: {operador}")

    else:
        raise ValueError(f"Tipo de no desconhecido: {tipo}")

    return codigo


def gerarRotinasAuxiliares(contexto):
    """Gera as rotinas Assembly para //, % e ^ se forem usadas."""
    rotinas = []

    if contexto["usa_div_int"] or contexto["usa_mod_int"]:
        # sdiv_software: divide r1 por r0, quociente em r2, resto em r3
        # O Cortex-A9 (DE1-SOC) nao possui instrucao SDIV em modo ARM,
        # entao implementamos divisao por subtracao repetida.
        # Algoritmo: conta quantas vezes o divisor (r0) cabe no dividendo (r1).
        # Funciona para inteiros nao-negativos (suficiente para os testes).
        rotinas.extend([
            "",
            "@ sdiv_software: r1 / r0 -> quociente em r2, resto em r3",
            "@ nao salva lr pois e chamado por div_int_double e mod_int_double",
            "sdiv_software:",
            "    MOV r2, #0",              # quociente = 0
            "sdiv_loop:",
            "    CMP r1, r0",              # dividendo >= divisor?
            "    BLT sdiv_fim",            # nao: termina
            "    SUB r1, r1, r0",          # dividendo -= divisor
            "    ADD r2, r2, #1",          # quociente++
            "    B sdiv_loop",
            "sdiv_fim:",
            "    MOV r3, r1",              # resto = dividendo restante
            "    BX lr"
        ])

    if contexto["usa_div_int"]:
        # div_int_double: d1 // d0, resultado (double) em d0
        rotinas.extend([
            "",
            "div_int_double:",
            "    PUSH {lr}",
            "    VCVT.S32.F64 s2, d1",    # s2 = int(d1) = dividendo
            "    VCVT.S32.F64 s0, d0",    # s0 = int(d0) = divisor
            "    VMOV r1, s2",
            "    VMOV r0, s0",
            "    BL sdiv_software",        # r2 = quociente, r3 = resto
            "    VMOV s0, r2",
            "    VCVT.F64.S32 d0, s0",    # d0 = double(quociente)
            "    POP {lr}",
            "    BX lr"
        ])

    if contexto["usa_mod_int"]:
        # mod_int_double: d1 % d0, resultado (double) em d0
        rotinas.extend([
            "",
            "mod_int_double:",
            "    PUSH {lr}",
            "    VCVT.S32.F64 s2, d1",    # s2 = int(d1) = dividendo
            "    VCVT.S32.F64 s0, d0",    # s0 = int(d0) = divisor
            "    VMOV r1, s2",
            "    VMOV r0, s0",
            "    BL sdiv_software",        # r2 = quociente, r3 = resto
            "    VMOV s0, r3",
            "    VCVT.F64.S32 d0, s0",    # d0 = double(resto)
            "    POP {lr}",
            "    BX lr"
        ])

    if contexto["usa_pow_int"]:
        # pow_int_double: d1 ^ d0 (expoente inteiro), resultado em d0
        # Loop: multiplica d1 por si mesmo d0 vezes
        rotinas.extend([
            "",
            "pow_int_double:",
            "    PUSH {lr}",
            "    VCVT.S32.F64 s0, d0",    # s0 = int(d0) = expoente
            "    VMOV r0, s0",            # r0 = expoente (contador)
            "    VMOV.F64 d2, #1.0",      # d2 = acumulador, comeca em 1.0
            "pow_loop:",
            "    CMP r0, #0",
            "    BEQ pow_fim",
            "    VMUL.F64 d2, d2, d1",    # d2 = d2 * base
            "    SUB r0, r0, #1",
            "    B pow_loop",
            "pow_fim:",
            "    VMOV.F64 d0, d2",        # resultado em d0
            "    POP {lr}",
            "    BX lr"
        ])

    return rotinas


def gerarAssembly(estruturas):
    """
    Recebe uma lista de nos (AST) de cada expressao e gera
    o codigo Assembly completo para o CPUlator ARMv7 DE1-SOC.

    Cada resultado e salvo em result_N na secao .data.
    O ultimo resultado tambem e exibido nos LEDs do DE1-SOC
    (endereco mapeado 0xFF200000), como inteiro truncado.
    """
    contexto = {
        "constantes":  {},
        "variaveis":   {},
        "usa_div_int": False,
        "usa_mod_int": False,
        "usa_pow_int": False,
        "indice_atual": 0      # atualizado a cada expressao para o calculo do RES
    }

    corpo = []

    for i, estrutura in enumerate(estruturas):
        contexto["indice_atual"] = i

        corpo.append(f"    @ --- expressao {i} ---")
        linhas = gerarCodigoNo(estrutura, contexto)
        corpo.extend("    " + linha for linha in linhas)

        # Salva resultado em result_i na memoria
        corpo.append(f"    LDR r0, =result_{i}")
        corpo.append("    VSTR.F64 d0, [r0]")
        corpo.append("")

    # Exibe o ultimo resultado nos LEDs do DE1-SOC (0xFF200000)
    # Converte o double para inteiro e escreve no registrador mapeado
    total = len(estruturas)
    corpo.append("    @ --- exibe ultimo resultado nos LEDs ---")
    corpo.append(f"    LDR r0, =result_{total - 1}")
    corpo.append("    VLDR.F64 d0, [r0]")
    corpo.append("    VCVT.S32.F64 s0, d0")
    corpo.append("    VMOV r1, s0")
    corpo.append("    LDR r0, =0xFF200000")
    corpo.append("    STR r1, [r0]")
    corpo.append("")

    # --- Secao .data ---
    linhasData = [".data", ".align 3"]

    for valor, rotulo in contexto["constantes"].items():
        linhasData.append(f"{rotulo}: .double {valor}")

    linhasData.append("mem_slot: .double 0.0")

    for nome, rotulo in contexto["variaveis"].items():
        linhasData.append(f"{rotulo}: .double 0.0")

    for i in range(len(estruturas)):
        linhasData.append(f"result_{i}: .double 0.0")

    # --- Secao .text ---
    linhasText = [
        ".text",
        ".global _start",
        "_start:"
    ]

    linhasText.extend(corpo)
    linhasText.extend([
        "fim:",
        "    B fim"          # loop infinito para inspecao no CPUlator
    ])

    linhasText.extend(gerarRotinasAuxiliares(contexto))

    return "\n".join(linhasData + [""] + linhasText)