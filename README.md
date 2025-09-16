# 🔎 Analisador Léxico em Python com SLY

Este projeto implementa um **Analisador Léxico** em Python, utilizando a biblioteca [SLY (Sly Lex-Yacc)](https://sly.readthedocs.io).

O objetivo é **tokenizar** um código-fonte em Python (por exemplo, `MaquinaBebida.py` ou qualquer outro arquivo `.py` presente na pasta e corretamente referenciado no `main.py`), reconhecendo palavras reservadas, identificadores, operadores, números, delimitadores e literais de string, além de calcular informações de posição como **linha**, **coluna**, **índice inicial** e **índice final** de cada token.

---

## 🚀 Tecnologias

* **Python** 3.13.4
* **SLY** — Simple Lex-Yacc

---

## 📦 Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/analisador-lexico.git
   cd analisador-lexico
   ```

2. \[**OPCIONAL**] Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install sly
   ```

---

## 📜 Estrutura de Arquivos

```
.
├── main.py             # Código do analisador léxico
├── MaquinaBebida.py    # Arquivo de entrada (código-fonte exemplo a ser analisado)
├── ArquivoTeste.py     # Arquivo de entrada (código-fonte exemplo a ser analisado)
└── README.md           # Detalhes do projeto
```

---

## ⚙️ Como Executar

1. Edite o arquivo `ArquivoTeste.py` com o código Python que deseja analisar.

   Exemplo:

   ```python
   def soma(vetor):
       if vetor == []:
           return 0
       else:
           return vetor[0] + soma(vetor[1:])
   ```

2. Execute o analisador:

   ```bash
   python main.py
   ```

3. Saída esperada (tokens encontrados):

   ```
   Tipo            | Lexema                        | Linha | Coluna | Inicio | Fim
   --------------------------------------------------------------------------------
   DEF             | def                           | 1     | 1      | 0      | 3
   IDENTIFICADOR   | soma                          | 1     | 5      | 4      | 8
   DELIMITADOR     | (                             | 1     | 9      | 8      | 9
   ...
   ```

---

## 🔍 Funcionalidades

- ✅ Reconhece **palavras-chave do Python** (ex.: `def`, `if`, `else`, `return`, `class`, `while`, etc.)
- ✅ Reconhece **identificadores** (nomes de variáveis e funções)
- ✅ Reconhece **números inteiros e decimais**
- ✅ Reconhece **strings** (`'texto'`, `"texto"`)
- ✅ Reconhece **operadores** (`=`, `==`, `!=`, `<=`, `>=`, `+`, `-`, `*`, `/`, `%`, `//`, `**`)
- ✅ Reconhece **delimitadores** (`{}`, `()`, `[]`, `:`, `;`, `,`)
- ✅ Reconhece **`.` (DOT)** e **`...` (ELLIPSIS)**
- ✅ Ignora espaços, tabulações, comentários (`#`) e docstrings (`'''...'''` ou `"""..."""`)
- ✅ Exibe informações de posição: **linha**, **coluna**, **início**, **fim**

---

## 📌 Exemplo de Saída Formatada

```
IF              | if                            | 2     | 5      | 21     | 23
IDENTIFICADOR   | vetor                         | 2     | 8      | 24     | 29
OPERATOR        | ==                            | 2     | 14     | 30     | 32
DELIMITADOR     | [                             | 2     | 17     | 33     | 34
DELIMITADOR     | ]                             | 2     | 18     | 34     | 35
```

---

## 📖 Referências

* [Documentação oficial do SLY](https://sly.readthedocs.io/)

---