# Analisador Léxico em Python com SLY

Este projeto implementa um **Analisador Léxico** simples em Python, utilizando a biblioteca [SLY (Sly Lex-Yacc)](https://sly.readthedocs.io/_/downloads/en/latest/pdf).

O objetivo é **tokenizar** um código-fonte de exemplo (`arquivoTeste.py`), identificando palavras reservadas, identificadores, operadores, números e delimitadores, além de calcular informações de posição como linha, coluna, índice inicial e final de cada token.

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

2. \[**OPCIONAL**] Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

   > **Observação:** Caso utilize ambiente virtual no PyCharm, é necessário configurá-lo para que a IDE reconheça as bibliotecas instaladas:
   >
   > 1. Abra o PyCharm → Preferences → Project → Python Interpreter
   > 2. Clique na engrenagem → Add… → Existing environment
   > 3. Navegue até `LexicalAnalyser/venv/bin/python` e selecione
   > 4. Clique OK → agora o PyCharm vai enxergar o sly instalado

3. Instale as dependências:

   ```bash
   pip install sly
   ```

---

## 📜 Estrutura de Arquivos

```
.
├── main.py            # Código do analisador léxico
├── arquivoTeste.py    # Arquivo de entrada (código-fonte a ser analisado)
└── README.md          # Arquivo de detalhes do projeto
```

---

## ⚙️ Como Executar

1. Edite o arquivo `arquivoTeste.py` com o código que deseja analisar.

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
   Token('DEF', lexema = 'def'), linha = 1, coluna = 1, inicio = 0, fim = 3
   Token('IDENTIFICADOR', lexema = 'soma'), linha = 1, coluna = 5, inicio = 4, fim = 8
   Token('DELIMITADOR', lexema = '('), linha = 1, coluna = 9, inicio = 8, fim = 9
   ...
   ```

---

## 🔍 Funcionalidades

* Reconhece palavras-chave: `def`, `if`, `else`, `return`, `print`.
* Reconhece **identificadores** (`variaveis`, `funcoes`).
* Reconhece **números inteiros**.
* Reconhece **operadores** (`=`, `==`, `+`, `-`, `*`, `/`, `<`, `>`).
* Reconhece **delimitadores** (`{}`, `()`, `[]`, `:`, `;`, `,`).
* Ignora espaços em branco, tabulações e quebras de linha.
* Mostra informações de posição de cada token:

    * **linha**
    * **coluna**
    * **inicio**
    * **fim**

---

## 📌 Exemplo de Saída Formatada

```
Token('IF', lexema = 'if'), linha = 2, coluna = 5, inicio = 21, fim = 23
Token('IDENTIFICADOR', lexema = 'vetor'), linha = 2, coluna = 8, inicio = 24, fim = 29
Token('OPERATOR', lexema = '=='), linha = 2, coluna = 14, inicio = 30, fim = 32
Token('DELIMITADOR', lexema = '['), linha = 2, coluna = 17, inicio = 33, fim = 34
```

---

## 📖 Referências

* [Documentação oficial do SLY](https://sly.readthedocs.io/)

---
