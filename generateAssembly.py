from executeExpression import executarExpressao


def registrarConstante(valor, contexto):
    if valor not in contexto["constantes"]:
        rotulo = f"const_{len(contexto['constantes'])}"
        contexto["constantes"][valor] = rotulo
    return contexto["constantes"][valor]


def registrarResultado(indice, contexto):
    contexto["resultados_usados"].add(indice)
    return f"result_{indice}"


def gerarCodigoNo(no, contexto):
    tipo = no["tipo"]
    codigo = []

    if tipo == "numero":
        rotulo = registrarConstante(no["valor"], contexto)
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VLDR.F64 d0, [r0]")
        return codigo

    elif tipo == "mem_leitura":
        contexto["usa_mem"] = True
        codigo.append("LDR r0, =mem_slot")
        codigo.append("VLDR.F64 d0, [r0]")
        return codigo

    elif tipo == "mem_escrita":
        contexto["usa_mem"] = True
        codigo.extend(gerarCodigoNo(no["valor"], contexto))
        codigo.append("LDR r0, =mem_slot")
        codigo.append("VSTR.F64 d0, [r0]")
        return codigo

    elif tipo == "res":
        rotulo = registrarResultado(no["indice"], contexto)
        codigo.append(f"LDR r0, ={rotulo}")
        codigo.append("VLDR.F64 d0, [r0]")
        return codigo

    elif tipo == "identificador":
        raise NotImplementedError(
            f"Identificador '{no['valor']}' ainda não teve semântica definida"
        )

    elif tipo == "operacao":
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
            contexto["usa_div_int"] = True
            codigo.append("BL div_int_double")
        elif operador == "%":
            contexto["usa_mod_int"] = True
            codigo.append("BL mod_int_double")
        elif operador == "^":
            contexto["usa_pow_int"] = True
            codigo.append("BL pow_int_double")
        else:
            raise ValueError(f"Operador desconhecido: {operador}")

        return codigo

    else:
        raise ValueError(f"Tipo de nó desconhecido: {tipo}")


def gerarRotinasAuxiliares(contexto):
    rotinas = []

    if contexto["usa_div_int"]:
        rotinas.extend([
            "",
            "div_int_double:",
            "    @ entrada: d1 = esquerda, d0 = direita",
            "    VCVT.S32.F64 s2, d1",
            "    VCVT.S32.F64 s0, d0",
            "    VMOV r1, s2",
            "    VMOV r0, s0",
            "    SDIV r2, r1, r0",
            "    VMOV s0, r2",
            "    VCVT.F64.S32 d0, s0",
            "    BX lr"
        ])

    if contexto["usa_mod_int"]:
        rotinas.extend([
            "",
            "mod_int_double:",
            "    @ entrada: d1 = esquerda, d0 = direita",
            "    VCVT.S32.F64 s2, d1",
            "    VCVT.S32.F64 s0, d0",
            "    VMOV r1, s2",
            "    VMOV r0, s0",
            "    SDIV r2, r1, r0",
            "    MUL r3, r2, r0",
            "    SUB r4, r1, r3",
            "    VMOV s0, r4",
            "    VCVT.F64.S32 d0, s0",
            "    BX lr"
        ])

    if contexto["usa_pow_int"]:
        rotinas.extend([
            "",
            "pow_int_double:",
            "    @ entrada: d1 = base, d0 = expoente",
            "    VCVT.S32.F64 s0, d0",
            "    VMOV r0, s0",
            "    VMOV.F64 d2, #1.0",
            "pow_loop:",
            "    CMP r0, #0",
            "    BEQ pow_fim",
            "    VMUL.F64 d2, d2, d1",
            "    SUB r0, r0, #1",
            "    B pow_loop",
            "pow_fim:",
            "    VMOV.F64 d0, d2",
            "    BX lr"
        ])

    return rotinas


def gerarAssembly(tokens, memoria=None, resultados=None):
    info = executarExpressao(tokens, memoria, resultados)
    estrutura = info["estrutura"]

    contexto = {
        "constantes": {},
        "resultados_usados": set(),
        "usa_mem": False,
        "usa_div_int": False,
        "usa_mod_int": False,
        "usa_pow_int": False
    }

    corpo = gerarCodigoNo(estrutura, contexto)

    linhasData = [".data", ".align 3"]

    for valor, rotulo in contexto["constantes"].items():
        linhasData.append(f"{rotulo}: .double {valor}")

    linhasData.append("mem_slot: .double 0.0")
    linhasData.append("result_out: .double 0.0")

    for indice in sorted(contexto["resultados_usados"]):
        linhasData.append(f"result_{indice}: .double 0.0")

    linhasText = [
        ".text",
        ".global _start",
        "_start:"
    ]

    linhasText.extend("    " + linha for linha in corpo)
    linhasText.extend([
        "    LDR r0, =result_out",
        "    VSTR.F64 d0, [r0]",
        "fim:",
        "    B fim"
    ])

    linhasText.extend(gerarRotinasAuxiliares(contexto))

    codigoAssembly = "\n".join(linhasData + [""] + linhasText)
    return codigoAssembly