from lark import Lark, Transformer

# Load the grammar
with open("escript/escript_grammar.lark") as f:
    escript_grammar = f.read()

class EScriptTransformer(Transformer):
    def function(self, items):
        return {"type": "function", "name": items[0], "params": items[1], "body": items[2]}
    
    def params(self, items):
        return list(items) if items else []
    
    def statements(self, items):
        return list(items)
    
    def assign(self, items):
        return {"type": "assign", "var": items[0], "value": items[1]}
    
    def function_call(self, items):
        return {"type": "function_call", "name": items[0], "args": items[1]}
    
    def print(self, items):
        return {"type": "print", "value": items[0].strip('"')}
    
    def print_var(self, items):
        return {"type": "print_var", "var": items[0]}
    
    def input(self, items):
        return {"type": "input", "var": items[0], "prompt": items[1].strip('"')}
    
    def conditional(self, items):
        if len(items) == 2:
            return {"type": "if", "condition": items[0], "true_body": items[1], "false_body": None}
        else:
            return {"type": "if", "condition": items[0], "true_body": items[1], "false_body": items[2]}
    
    def condition(self, items):
        return {"left": items[0], "op": items[1], "right": items[2]}
    
    def comparator(self, items):
        return items[0]
    
    def expr(self, items):
        return items[0]
    
    def args(self, items):
        return list(items)
    
    def file_create(self, items):
        return {"type": "file_create", "filename": items[0].strip('"'), "extension": items[1].strip('"')}
    
    def file_write(self, items):
        return {"type": "file_write", "var": items[0]}
    
    def file_save(self, items):
        return {"type": "file_save"}
    
    def db_create(self, items):
        return {"type": "db_create", "db_name": items[0].strip('"')}
    
    def db_write(self, items):
        return {"type": "db_write", "var": items[0]}
    
    def db_save(self, items):
        return {"type": "db_save"}
    
    def db_read(self, items):
        return {"type": "db_read", "var": items[0], "db_name": items[1].strip('"'), "query": items[2].strip('"')}

parser = Lark(escript_grammar, parser='lalr', transformer=EScriptTransformer())

def parse_escript(code):
    return parser.parse(code)
