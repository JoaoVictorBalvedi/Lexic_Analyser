# Grupo: <RA1 22>
# Integrante:
# João Victor Balvedi - @JoaoVictorBalvedi

import json

from parser import parseExpressao
from executeExpression import executarExpressao
from generateAssembly import gerarAssembly
from results import exibirResultados


def lerArquivo(nomeArquivo):
    """Le todas as linhas nao vazias do arquivo e retorna uma lista."""
    linhasArquivo = []

    with open(nomeArquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha != "":
                linhasArquivo.append(linha)

    return linhasArquivo


def salvarAssembly(nomeArquivo, codigo):
    """Salva o codigo Assembly gerado em um arquivo .s"""
    with open(nomeArquivo, "w") as arquivo:
        arquivo.write(codigo)


def salvarTokens(nomeArquivo, todosTokens):
    """
    Salva os tokens de todas as expressoes em um arquivo JSON.
    Requisito do projeto: tokens devem ser salvos para fases futuras.
    Formato: lista de listas, uma por expressao.
    """
    with open(nomeArquivo, "w") as arquivo:
        json.dump(todosTokens, arquivo, indent=2)


def main():
    # Leitura do nome do arquivo via input() (sem menu, apenas uma pergunta)
    arquivoEntrada = input("Digite o nome do arquivo de entrada: ").strip()
    arquivoSaida = arquivoEntrada.replace(".txt", ".s")
    arquivoTokens = arquivoEntrada.replace(".txt", "_tokens.json")

    # Le todas as linhas do arquivo fonte
    linhasArquivo = lerArquivo(arquivoEntrada)

    resultados = []
    estruturas = []
    todosTokens = []

    # Contexto compartilhado entre todas as expressoes do arquivo
    # (necessario para MEM e RES funcionarem entre linhas)
    memoria = {}
    resultadosAnteriores = []

    for i, linha in enumerate(linhasArquivo):
        # 1. Analise lexica: gera lista de tokens
        tokens = parseExpressao(linha)

        # 2. Analise estrutural: gera arvore (AST) e atualiza contexto
        infoExecucao = executarExpressao(tokens, memoria, resultadosAnteriores)

        estrutura = infoExecucao["estrutura"]
        estruturas.append(estrutura)
        resultadosAnteriores.append(estrutura)
        todosTokens.append(tokens)

        resultados.append({
            "linha": i,
            "expressao": linha,
            "tokens": tokens,
            "estrutura": estrutura
        })

    # 3. Geracao do Assembly
    codigoAssembly = gerarAssembly(estruturas)
    salvarAssembly(arquivoSaida, codigoAssembly)

    # 4. Salva tokens em arquivo JSON
    salvarTokens(arquivoTokens, todosTokens)

    print(f"\nArquivo de entrada : {arquivoEntrada}")
    print(f"Assembly gerado em : {arquivoSaida}")
    print(f"Tokens salvos em   : {arquivoTokens}")

    # 5. Exibe resumo no terminal
    exibirResultados(resultados)


if __name__ == "__main__":
    main()