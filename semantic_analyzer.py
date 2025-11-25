import json

class SemanticAnalyzer:
    RED = "\033[38;2;220;20;60m"  # vermelho visivel para erros
    RESET = "\033[0m"

    def __init__(self):
        # A tabela agora é explicativa:
        # name -> {
        #   'category': 'variable' | 'operator' | 'builtin-function' | 'literal-value',
        #   'data_type': 'number' | 'string' | 'operator' | 'builtin' | ...
        #   'description': texto explicando o símbolo
        # }
        self.symbol_table = {}

    def _build_description(self, name, category, data_type):
        if category == "variable":
            return f"User-defined variable '{name}' of type {data_type}"
        elif category == "operator":
            return f"Operator '{name}' used in expressions"
        elif category == "builtin-function":
            return f"Builtin function '{name}'"
        elif category == "literal-value":
            return f"Literal value of type {data_type}"
        else:
            return f"Symbol '{name}' of category {category}"

    def add_to_symbol_table(self, name, data_type=None, category='variable'):
        """Adiciona um símbolo com nomes mais descritivos:
        - category: 'variable', 'operator', 'builtin-function', 'literal-value'
        - data_type: 'number', 'string', ...
        """

        # Normaliza os nomes das categorias
        category_map = {
            'var': 'variable',
            'operator': 'operator',
            'builtin': 'builtin-function',
            'literal': 'literal-value'
        }
        category = category_map.get(category, category)

        if name in self.symbol_table:
            entry = self.symbol_table[name]
            if data_type and (entry.get('data_type') in (None, 'unknown')):
                entry['data_type'] = data_type
                entry['description'] = self._build_description(name, entry['category'], data_type)
                print(f"Atualizado: O símbolo '{name}' agora tem tipo '{data_type}'.")
        else:
            description = self._build_description(name, category, data_type)

            self.symbol_table[name] = {
                'category': category,
                'data_type': data_type,
                'description': description
            }
            print(f"Declaração: '{name}' adicionado (category={category}, data_type={data_type}).")

    def lookup_symbol(self, name):
        return self.symbol_table.get(name)

    def get_type(self, name):
        entry = self.lookup_symbol(name)
        return entry.get('data_type') if entry else None

    def _print_error(self, message):
        print(f"{self.RED}{message}{self.RESET}")

    def _report_type_error(self, operator, left_type, right_type, detail):
        self._print_error(f"Erro semantico: {detail} na operacao '{operator}' (tipos: {left_type} e {right_type})")

    def resolve_binop_type(self, left_type, right_type, operator):
        """Retorna o tipo resultante de uma operacao binaria ou 'unknown' em caso de erro."""
        numeric_types = {'number', 'int', 'float'}

        if left_type in (None, 'unknown') or right_type in (None, 'unknown'):
            self._report_type_error(operator, left_type, right_type, "tipo desconhecido")
            return 'unknown'

        if operator == '+':
            if left_type in numeric_types and right_type in numeric_types:
                return 'number'
            if left_type == 'string' and right_type == 'string':
                return 'string'
            self._report_type_error(operator, left_type, right_type, "soma requer dois numeros ou duas strings")
            return 'unknown'

        if operator in ('-', '*', '/'):
            if left_type in numeric_types and right_type in numeric_types:
                return 'number'
            self._report_type_error(operator, left_type, right_type, f"operador '{operator}' aceita apenas tipos numericos")
            return 'unknown'

        self._report_type_error(operator, left_type, right_type, f"operador '{operator}' nao possui regra de tipos")
        return 'unknown'

    def infer_type(self, node):
        if node is None:
            return None

        if node.type == 'number':
            self.add_to_symbol_table(node.value, data_type='number', category='literal')
            return 'number'

        elif node.type == 'string':
            self.add_to_symbol_table(node.value, data_type='string', category='literal')
            return 'string'

        elif node.type == 'var':
            var_name = node.value
            var_type = self.get_type(var_name)
            if var_type is None:
                self._print_error(f"Erro semantico: A variavel '{var_name}' nao foi declarada.")
                return 'unknown'
            return var_type

        elif node.type == 'binop':
            left_type = self.infer_type(node.children[0])
            right_type = self.infer_type(node.children[1])
            operator = node.value

            self.add_to_symbol_table(operator, data_type='operator', category='operator')

            return self.resolve_binop_type(left_type, right_type, operator)

        elif node.type == 'block':
            return None

        return 'unknown'

    def analyze(self, node):
        if node is None:
            return

        if node.type == 'program':
            for child in node.children:
                self.analyze(child)

        elif node.type == 'assign':
            var_name = node.children[0].value
            expr_type = self.infer_type(node.children[1])
            self.add_to_symbol_table(var_name, expr_type, category='var')

        elif node.type == 'print':
            self.add_to_symbol_table('print', data_type='builtin', category='builtin')
            if len(node.children) > 0:
                self.infer_type(node.children[0])

        elif node.type in ('if', 'if_else', 'while'):
            self.infer_type(node.children[0])
            if len(node.children) > 1:
                self.analyze(node.children[1])
            if node.type == 'if_else' and len(node.children) > 2:
                self.analyze(node.children[2])

        elif node.type == 'block':
            for child in node.children:
                self.analyze(child)

        elif node.type == 'binop':
            self.infer_type(node)

        elif node.type == 'var':
            var_name = node.value
            if self.lookup_symbol(var_name) is None:
                self._print_error(f"Erro semantico: A variavel '{var_name}' nao foi declarada.")

    def save_symbol_table(self, filename="symbol_table.json"):
        with open(filename, "w") as f:
            json.dump(self.symbol_table, f, indent=4)
            print(f"Tabela de símbolos salva em {filename}")

    def load_symbol_table(self, filename="symbol_table.json"):
        try:
            with open(filename, "r") as f:
                self.symbol_table = json.load(f)
                print(f"Tabela carregada de {filename}")
        except FileNotFoundError:
            print(f"{filename} não encontrado. Criando tabela vazia.")
