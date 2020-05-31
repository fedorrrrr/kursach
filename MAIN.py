from Codegener import CodeGen
from Lexer import Lexer
from Parser import Parser

with open("/home/fedor/kursach/kurs/primer.txt") as file:
    text_input = file.read()

lexer = Lexer().get_lexer()
tokens = lexer.lex(text_input)
new_tokens = lexer.lex(text_input)

token_stream = []
for i in new_tokens:
    token_stream.append(i)
    print(i)

codegen = CodeGen()


module = codegen.module
builder = codegen.builder
printf = codegen.printf

pg = Parser(module, builder, printf)
pg.parse()
parser = pg.get_parser()
parse = parser.parse(tokens).eval()



codegen.create_ir()
codegen.save_ir("/home/fedor/kursach/kurs/out.ll")


