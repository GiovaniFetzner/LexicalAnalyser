# 📘 Python-Like Analyzer

### Analisador Léxico, Sintático e Semântico com Geração de AST (DOT/PNG)

Este projeto implementa um **pipeline completo de análise de código** inspirado em Python, utilizando:

* **PLY (Lex + Yacc)**
* **Analisador Semântico**
* **Geração de Árvore Sintática (AST)**
* **Exportação para GraphViz (DOT e PNG)**

O CLI permite rodar **apenas o lexer**, **apenas o parser/AST**, ou o **pipeline completo**, salvando a tabela de símbolos e gerando imagens da árvore.

---

## 🚀 Funcionalidades

* **Tokenização** de código (modo `--tokens`)
* **Geração da AST** com exportação para:
  * `ast.dot`
  * `ast.png`
* **Análise Semântica** com salvamento da tabela de símbolos:
  * `symbol_table.json`
* **Execução completa do pipeline**
* **Mensagens de erro léxico e sintático**

---

## 📁 Estrutura (resumo)

```
pythonProject/
├── main.py
├── mylexer.py
├── parser_ast.py
├── semantic_analyzer.py
├── ast_to_dot.py   (implementação opcional)
├── testes/         (arquivos de teste, opcional)
└── venv/           (ambiente virtual)
```

> Observação: o `main.py` possui sua própria implementação de `ast_to_dot`.

---

## 🧩 Requisitos

### Python
Versão **3.10+** recomendada.

### Dependências

```bash
pip install ply
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

### **1. Lexer**
```bash
python main.py --tokens arquivo.py
```

### **2. AST (DOT + PNG)**
```bash
python main.py --ast arquivo.py
```
Gera:

* `ast.dot`
* `ast.png` (se GraphViz estiver instalado)

### **3. Pipeline completo (default)**
```bash
python main.py --run arquivo.py
```

Ou:
```bash
python main.py arquivo.py
```

---

## 🗂️ Saídas geradas

| Arquivo               | Descrição                                          |
|-----------------------|----------------------------------------------------|
| **ast.dot**           | Representação DOT da árvore sintática              |
| **ast.png**           | Imagem gerada pelo GraphViz                        |
| **symbol_table.json** | Tabela de símbolos                                 |
| **parsetab.py**       | Arquivo automático do PLY                          |
| **parser.out**        | Gerado apenas em modo debug                        |

---

## 📌 Exemplo
```bash
python main.py --run testes/exemplo1.py
```

---

## ❗ Erros Comuns

### GraphViz não encontrado
Instale e coloque o comando `dot` no PATH.

### Arquivo não encontrado
Verifique o caminho informado.
