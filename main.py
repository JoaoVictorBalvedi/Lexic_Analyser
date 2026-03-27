def lerArquivo(nomeArquivo, linhas):
    linhasArquivo = []

    with open(nomeArquivo, 'r') as arquivo:
        for i in range(linhas):
            linha = arquivo.readline().strip()
            if linha != "":
                linhasArquivo.append(linha)

    return linhasArquivo

linhasArquivo = lerArquivo("teste1.txt", 12)

for i in linhasArquivo:
    print(i)
