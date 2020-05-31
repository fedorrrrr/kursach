from rply import LexerGenerator


class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        self.lexer.add('PROG', r'program')
        self.lexer.add('BEGIN', r'\{')
        self.lexer.add('END', r'\}')
        self.lexer.add('FUNC', r'function')

        self.lexer.add('VAR', r'var')
        self.lexer.add('INT', r'integer')
        self.lexer.add('REAL', r'float')

        self.lexer.add('ASSIGN', r'\:=')
        self.lexer.add('OP', r'\(')
        self.lexer.add('CP', r'\)')

        self.lexer.add('TT', r'\:')
        self.lexer.add('Z', r'\,')
        self.lexer.add('TZ', r'\;')
        self.lexer.add('EQUAL', r'\=')
        self.lexer.add('NOT_EQUAL', r'\!=')
        self.lexer.add('MORE', r'\>')
        self.lexer.add('LESS', r'\<')


        self.lexer.add('AND', r'and')
        self.lexer.add('NOT', r'not')
        self.lexer.add('OR', r'or')
        self.lexer.add('IF', r'if')
        self.lexer.add('THEN', r'then')
        self.lexer.add('ELSE', r'else')
        self.lexer.add('WHILE', r'while')
        self.lexer.add('DO', r'do')
        self.lexer.add('PRINT', r'print')


        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')

        self.lexer.add('BREAKCONTINUE', r'break')
        self.lexer.add('BREAKCONTINUE', r'continue')

        self.lexer.add('NUMBER', r'[0-9]+(\.[0-9]+)?')
        self.lexer.add('ID', r'[A-Za-z]\w*')

        self.lexer.ignore(r'@[^\@]*@')
        self.lexer.ignore('\s+')

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()
