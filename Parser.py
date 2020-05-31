from rply import ParserGenerator
from AST import *


class Parser():
    def __init__(self, module, builder, printf):
        self.pg = ParserGenerator(
            ['PROG', 'BEGIN', 'END', 'OP', 'CP', 'TZ', 'TT', 'Z', 'FUNC', 'VAR', 'INT', 'REAL', 'NUMBER', 'ID',
             'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'AND', 'NOT', 'OR', 'MORE', 'LESS', 'SUM', 'SUB', 'MUL', 'DIV',
             'IF', 'ELSE', 'WHILE', 'DO', 'BREAKCONTINUE', 'PRINT'],
            precedence=[("left", ['MUL', 'DIV']), ("left", ['SUM', 'SUB']) ])

        self.module = module
        self.builder = builder
        self.printf = printf

    def parse(self):

        @self.pg.production('program : PROG ID TZ var functions BEGIN statements END')
        def program(p):
            return p[6]

        @self.pg.production('var : VAR variable TT type TZ')
        def var(p):
            return p[1]

        @self.pg.production('var : VAR variable TT type TZ var')
        def var2(p):
            return p[1], p[5]

        @self.pg.production('variable : ID')
        def variable(p):
            return p[0]

        @self.pg.production('variable : ID Z variable')
        def variable2(p):
            return p[0], p[2]

        @self.pg.production('type : INT')
        @self.pg.production('type : REAL')
        def type(p):
            return p[0]

        @self.pg.production('functions : function')
        def functions(p):
            return p[0].eval()

        @self.pg.production('functions : function functions')
        def functions2(p):
            return Eval_(self.builder, self.module, p[0], p[2])

        @self.pg.production('function : FUNC ID OP var CP TT type TZ BEGIN statements END')
        def function(p):
            return Func_(self.builder, self.module, p[1], p[3], p[9])

        @self.pg.production('expression : OP expression CP')
        def expression(p):
            return p[1]

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression(p):
            if p[1].gettokentype() == 'SUM':
                return Sum(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'SUB':
                return Sub(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'MUL':
                return Mul(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'DIV':
                return Div(self.builder, self.module, p[0], p[2])

        @self.pg.production('expression : NUMBER')
        def number(p):
            return Number(self.builder, self.module, p[0].value)

        @self.pg.production('expression : ID')
        def expression_id(p):
            return Id_load(self.builder, self.module, p[0])

        @self.pg.production('expression : ID OP variable CP')
        def function3(p):
            return Call_(self.builder, self.module, p[0], p[2])

        @self.pg.production('statements : statement TZ')
        def statements(p):
            return p[0]

        @self.pg.production('statements : statement TZ statements')
        def statements2(p):
            return Eval_(self.builder, self.module, p[0], p[2])

        @self.pg.production('statement : type ID ASSIGN expression')
        def assign(p):
            print(p[0].value)
            return Id_save(self.builder, self.module, p[0], p[1], p[3])

        @self.pg.production('statement : IF OP bool CP BEGIN statements END ELSE BEGIN statements END')
        def if_(p):
            return If_else(self.builder, self.module, p[2], p[5], p[9])

        @self.pg.production('statement : IF OP bool CP BEGIN statements END')
        def if_2(p):
            return If_(self.builder, self.module, p[2], p[5])

        @self.pg.production('statement : WHILE OP bool CP DO BEGIN statements END')
        def while_(p):
            return While_(self.builder, self.module, p[2], p[6])

        @self.pg.production('statement : BREAKCONTINUE ')
        def breakcontinue(p):
            global goto
            goto = p[0].getstr()
            return

        @self.pg.production('statement : PRINT OP expression CP')
        def print_(p):
            return Print(self.builder, self.module, self.printf, p[2])

        @self.pg.production('bool : OP bool CP')
        def bool_(p):
            return p[1]

        @self.pg.production('bool : expression EQUAL expression')
        @self.pg.production('bool : expression MORE expression')
        @self.pg.production('bool : expression LESS expression')
        @self.pg.production('bool : expression NOT_EQUAL expression')
        def bool_2(p):
            if p[1].gettokentype() == 'EQUAL':
                return Equal(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'MORE':
                return More(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'LESS':
                return Less(self.builder, self.module, p[0], p[2])
            elif p[1].gettokentype() == 'NOT_EQUAL':
                return Not_equal(self.builder, self.module, p[0], p[2])

        @self.pg.production('bool : bool AND bool')
        def and_(p):
            return And_(self.builder, self.module, p[0], p[2])

        @self.pg.production('bool : bool OR bool')
        def or_(p):
            return Or_(self.builder, self.module, p[0], p[2])

        @self.pg.production('bool : NOT bool')
        def not_(p):
            return Not_(self.builder, self.module, p[1])

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()


goto = None


class While_():
    def __init__(self, builder, module, boolean, right):
        self.builder = builder
        self.module = module
        self.boolean = boolean
        self.right = right

    def eval(self):
        global goto
        i = None
        self.builder = new_b(self.builder)
        for x in range(5):
            with self.builder.if_then(self.boolean.eval()):
                if goto == "break":
                    break
                elif goto == "continue":
                    continue
                i = self.right.eval()
        return i
