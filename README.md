# 📘 Python-Like Analyzer

### Analisador Léxico, Sintático e Semântico com Geração de AST (DOT/PNG)

Este projeto implementa um **pipeline completo de análise de código** inspirado em Python, utilizando:

* **SLY (Lexer + Parser)**
* **Analisador Semântico**
* **Geração de Árvore Sintática (AST)**
* **Exportação para GraphViz (DOT e PNG)**

O CLI permite rodar **apenas o lexer**, **apenas o parser/AST**, ou o **pipeline completo**, salvando a tabela de símbolos e gerando imagens da árvore.

---

## 🚀 Funcionalidades

* **Tokenização** de código (modo `--tokens`)
* **Geração da AST** com exportação para:

  * `ast.dot`
  * `ast.png` (requer GraphViz)
* **Análise Semântica** com salvamento da tabela de símbolos:

  * `symbol_table.json`
* **Execução completa do pipeline** (lexer + parser + semântica)
* **Mensagens detalhadas de erro**

---

## 📁 Estrutura (resumo)

```
pythonProject/
├── main.py
├── mylexer.py
├── parser_ast.py
├── semantic_analyzer.py
├── ast_to_dot.py   (opcional)
├── testes/         (arquivos de teste)
└── venv/           (ambiente virtual)
```

---

## 🧩 Requisitos

### Python

Versão **3.10+** recomendada.

### Dependências

Instale com:

```bash
pip install sly
```

### GraphViz (opcional, mas recomendado)

Necessário para gerar `ast.png`.

* Windows: [https://graphviz.org/download/](https://graphviz.org/download/)
* Linux (Debian/Ubuntu):

```bash
sudo apt install graphviz
```

---

## ▶️ Uso do CLI

### **1. Executar apenas o lexer (tokens)**

```bash
python main.py --tokens arquivo.py
```

Exibe todos os tokens reconhecidos pelo analisador léxico.

---

### **2. Gerar apenas a AST (DOT + PNG)**

```bash
python main.py --ast arquivo.py
```

Gera:

* `ast.dot`
* `ast.png` (se GraphViz estiver instalado)

---

### **3. Executar o pipeline completo (default)**

```bash
python main.py --run arquivo.py
```

Ou simplesmente:

```bash
python main.py arquivo.py
```

Executa:

1. Lexer
2. Parser
3. Análise Semântica
4. Gera `symbol_table.json`
5. Exporta AST para `ast.dot` e `ast.png`

---

## 🗂️ Saídas geradas

| Arquivo               | Descrição                                          |
| --------------------- | -------------------------------------------------- |
| **ast.dot**           | Representação DOT da árvore sintática              |
| **ast.png**           | Imagem gerada pelo GraphViz                        |
| **symbol_table.json** | Tabela de símbolos resultante da análise semântica |
| **parsetab.py**       | Tabela do parser (SLY) – gerada automaticamente    |
| **parser.out**        | Arquivo de depuração do parser                     |

---

## 📌 Exemplo de Execução

```bash
python main.py --run testes/exemplo1.py
```

Saída esperada:

```
Arquivo DOT gerado: ast.dot
Arquivo PNG gerado: ast.png
Tabela de símbolos salva em symbol_table.json
```

---

## ❗ Erros Comuns

### *"GraphViz não encontrado"*

Instale o GraphViz e garanta que o binário `dot` está no PATH.

### *Arquivo não encontrado: ...*

Verifique se o caminho do arquivo passado está correto.

