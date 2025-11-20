import json


class SemanticAnalyzer:
    def __init__(self):
        # A tabela de símbolos será um dicionário
        # formato: name -> { 'kind': 'var'|'operator'|'builtin'|'literal', 'type': 'number'|'string'|... }
        self.symbol_table = {}

    def add_to_symbol_table(self, name, var_type=None, kind='var'):
        """Adiciona um símbolo à tabela. Pode ser variável, operador ou builtin.

        - name: nome do símbolo ('a', '+', 'print')
        - var_type: tipo associado ('number', 'string', 'operator', 'builtin', ...)
        - kind: categoria ('var', 'operator', 'builtin', 'literal')
        """
        if name in self.symbol_table:
            entry = self.symbol_table[name]
            # atualiza tipo se antes era desconhecido
            if var_type and (entry.get('type') in (None, 'unknown')):
                entry['type'] = var_type
                print(f"Atualizado: O símbolo '{name}' agora tem tipo '{var_type}'.")
            else:
                # já existe; não considera erro para operadores/builtins
                pass
        else:
            self.symbol_table[name] = {'kind': kind, 'type': var_type}
            print(f"Declaração: O símbolo '{name}' foi adicionado (kind={kind}, type={var_type}).")

    def lookup_symbol(self, name):
        """Retorna a entrada completa da tabela de símbolos (dict) ou None se não existir."""
        return self.symbol_table.get(name)

    def get_type(self, name):
        """Retorna apenas o tipo associado a um símbolo ou None."""
        entry = self.lookup_symbol(name)
        return entry.get('type') if entry else None

    def check_type_compatibility(self, left_type, right_type, operator):
        """Verifica se os tipos de duas expressões são compatíveis"""
        # Operações aritméticas requerem ambos os operandos serem numéricos
        numeric_types = {'number', 'int', 'float'}
        # se algum for None/unknown, emite aviso
        if left_type is None or right_type is None:
            print(f"Erro semântico: tipo desconhecido em operação {operator}: {left_type} e {right_type}")
            return False
        if left_type not in numeric_types or right_type not in numeric_types:
            print(f"Erro semântico: tipos incompatíveis para a operação {operator}: {left_type} e {right_type}")
            return False
        return True

    def infer_type(self, node):
        """Infere o tipo de uma expressão e retorna o tipo"""
        if node is None:
            return None

        if node.type == 'number':
            # literais numéricos são number
            return 'number'
        
        elif node.type == 'var':
            var_name = node.value
            var_type = self.get_type(var_name)
            if var_type is None:
                print(f"Erro semântico: A variável '{var_name}' não foi declarada.")
                return 'unknown'
            return var_type
        
        elif node.type == 'binop':
            # Recursivamente infer tipos dos operandos
            left_type = self.infer_type(node.children[0])
            right_type = self.infer_type(node.children[1])
            operator = node.value
            # registra operador na tabela, se necessário
            self.add_to_symbol_table(operator, var_type='operator', kind='operator')

            # Verifica compatibilidade
            if self.check_type_compatibility(left_type, right_type, operator):
                return 'number'  # Resultado de operação aritmética é número
            else:
                return 'unknown'
        
        elif node.type == 'string':
            return 'string'
        
        elif node.type == 'block':
            # Um bloco não tem tipo específico
            return None
        
        else:
            return 'unknown'

    def analyze(self, node):
        """Realiza a verificação semântica na AST"""
        if node is None:
            return

        if node.type == 'program':
            # Analisa todos os statements do programa
            for child in node.children:
                self.analyze(child)
        
        elif node.type == 'assign':  # Atribuição
            var_name = node.children[0].value  # Nome da variável
            expr_node = node.children[1]  # Nó da expressão
            expr_type = self.infer_type(expr_node)  # Infere o tipo da expressão
            self.add_to_symbol_table(var_name, expr_type, kind='var')
        
        elif node.type == 'print':
            # Apenas infer o tipo do argumento impresso
            # registra builtin print
            self.add_to_symbol_table('print', var_type='builtin', kind='builtin')
            if len(node.children) > 0:
                self.infer_type(node.children[0])
        
        elif node.type == 'if' or node.type == 'if_else' or node.type == 'while':
            # Analisa a condição e os blocos
            condition = node.children[0]
            self.infer_type(condition)
            
            # Analisa o primeiro bloco (if/while)
            if len(node.children) > 1:
                self.analyze(node.children[1])
            
            # Analisa o bloco else (se existir)
            if node.type == 'if_else' and len(node.children) > 2:
                self.analyze(node.children[2])
        
        elif node.type == 'block':
            # Analisa cada statement dentro do bloco
            for child in node.children:
                self.analyze(child)
        
        elif node.type == 'binop':
            # Apenas infere o tipo (não imprime erro redundante)
            self.infer_type(node)
        
        elif node.type == 'var':
            # Verifica se a variável foi declarada
            var_name = node.value
            entry = self.lookup_symbol(var_name)
            if entry is None:
                print(f"Erro semântico: A variável '{var_name}' não foi declarada.")
            # não adiciona variável aqui; a declaração vem via atribuição
    
    def save_symbol_table(self, filename="symbol_table.json"):
        """Salva a tabela de símbolos em um arquivo JSON"""
        with open(filename, "w") as f:
            json.dump(self.symbol_table, f, indent=4)
            print(f"Tabela de símbolos salva em {filename}")

    def load_symbol_table(self, filename="symbol_table.json"):
        """Carrega a tabela de símbolos de um arquivo JSON"""
        try:
            with open(filename, "r") as f:
                self.symbol_table = json.load(f)
                print(f"Tabela de símbolos carregada de {filename}")
        except FileNotFoundError:
            print(f"Arquivo {filename} não encontrado. Inicializando tabela vazia.")
