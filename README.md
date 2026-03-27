# Analisador Léxico — RPN para Assembly ARMv7

**Disciplina:** Construção de Interpretadores

## Integrantes (ordem alfabética)

|         Nome        |       GitHub       |
|---------------------|--------------------|
| Joao Victor Balvedi | @JoaoVictorBalvedi |

---

## Descrição

Programa em Python que lê expressões aritméticas em **notação polonesa reversa (RPN)** de um arquivo de texto, realiza a **análise léxica** usando Autômatos Finitos Determinísticos e gera **código Assembly** compatível com a arquitetura **ARMv7 DE1-SOC (CPUlator)**.

Nenhum cálculo é executado em Python — toda a aritmética é realizada pelo Assembly gerado, rodando no simulador CPUlator.

---

## Estrutura do Projeto

```
.
├── main.py                  # Ponto de entrada do programa
├── parser.py                # Analisador léxico (AFD com funções de estado)
├── executeExpression.py     # Constrói a árvore (AST) a partir dos tokens
├── generateAssembly.py      # Gera o código Assembly a partir da AST
├── results.py               # Exibe resumo no terminal
├── testes_lexer.py          # Testes do analisador léxico
├── teste1.txt               # Arquivo de teste 1
├── teste2.txt               # Arquivo de teste 2
├── teste3.txt               # Arquivo de teste 3
└── README.md
```

---

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa (apenas módulos da biblioteca padrão)

---

## Como executar

1. Clone o repositório e entre na pasta:
```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

2. Execute o programa e informe o arquivo de entrada quando solicitado:
```bash
python3 main.py
```

3. Digite o nome do arquivo de teste:
```
Digite o nome do arquivo de entrada: teste1.txt
```

O programa vai gerar dois arquivos na mesma pasta:
- `teste1.s` — código Assembly pronto para o CPUlator
- `teste1_tokens.json` — tokens gerados pelo analisador léxico

---

## Como rodar o Assembly no CPUlator

1. Acesse [https://cpulator.01xz.net/?sys=arm-de1soc](https://cpulator.01xz.net/?sys=arm-de1soc)
2. Selecione o modelo **ARMv7 DE1-SoC (v16.1)**
3. Copie o conteúdo do arquivo `.s` gerado e cole no editor
4. Clique em **Compile and Load**
5. Clique em **Continue** para executar
6. Inspecione os resultados na seção **Memory** nos endereços dos labels `result_0` até `result_N`
7. O último resultado também aparece nos **LEDs** (endereço `0xFF200000`), exibido como inteiro

---

## Como rodar os testes do analisador léxico

```bash
python3 testes_lexer.py
```

Saída esperada: todos os casos marcados como `[OK]`, cobrindo 15 entradas válidas e 10 inválidas.

---

## Linguagem suportada

Expressões em RPN no formato `(A B op)`, onde `A` e `B` são números reais e `op` é um operador.

| Operador | Exemplo | Descrição |
|----------|---------|-----------|
| `+` | `(3.0 4.0 +)` | Adição |
| `-` | `(10.0 2.0 -)` | Subtração |
| `*` | `(2.0 5.0 *)` | Multiplicação |
| `/` | `(9.0 3.0 /)` | Divisão real |
| `//` | `(9.0 2.0 //)` | Divisão inteira |
| `%` | `(9.0 2.0 %)` | Resto da divisão |
| `^` | `(2.0 3.0 ^)` | Potenciação |

Comandos especiais:

| Comando | Exemplo | Descrição |
|---------|---------|-----------|
| `(V MEM)` | `(5.0 MEM)` | Armazena valor em memória |
| `(MEM)` | `(MEM)` | Lê valor da memória |
| `(V VAR)` | `(8.5 VAR)` | Armazena valor em variável nomeada |
| `(VAR)` | `(VAR)` | Lê variável nomeada |
| `(N RES)` | `(1 RES)` | Retorna resultado de N linhas atrás |

Expressões podem ser aninhadas sem limite:
```
((2.0 3.0 +) 4.0 *)
(((1.0 2.0 +) (3.0 4.0 +) *) 2.0 /)
```
