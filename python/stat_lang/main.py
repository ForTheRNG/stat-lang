# from .parser import Lark_StandAlone as Lark, Transformer
from lark import Lark, Transformer

def parse():
    pass

grammar = ""
with open("./grammar.lark") as f:
    grammar = "".join(f.readlines())
parser = Lark(grammar, parser="lalr")
content = ""
with open("../../samples/drop_lowest") as f:
    content = "".join(f.readlines())
print(parser.parse(content).pretty())