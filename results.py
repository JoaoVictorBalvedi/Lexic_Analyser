# Grupo: <RA1 22>
# Integrante:
# João Victor Balvedi - @JoaoVictorBalvedi


def exibirResultados(resultados):
    """Exibe no terminal um resumo de cada expressao processada."""
    print("\nRESUMO")
    print("=" * 50)

    for item in resultados:
        print(f"Linha {item['linha']}: {item['expressao']}")
        print(f"Tokens   : {item['tokens']}")
        print(f"Estrutura: {item['estrutura']}")
        print("-" * 50)