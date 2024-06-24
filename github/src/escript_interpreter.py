import os
import sqlite3

from escript_project.escript.escript_parser import parse_escript

class EScriptInterpreter:
    def __init__(self):
        self.variables = {}
        self.current_file = None
        self.current_db = None

    def execute(self, node):
        if node['type'] == 'function':
            self.execute_function(node)
        elif node['type'] == 'assign':
            self.execute_assign(node)
        elif node['type'] == 'function_call':
            self.execute_function_call(node)
        elif node['type'] == 'print':
            self.execute_print(node)
        elif node['type'] == 'print_var':
            self.execute_print_var(node)
        elif node['type'] == 'input':
            self.execute_input(node)
        elif node['type'] == 'if':
            self.execute_if(node)
        elif node['type'] == 'file_create':
            self.execute_file_create(node)
        elif node['type'] == 'file_write':
            self.execute_file_write(node)
        elif node['type'] == 'file_save':
            self.execute_file_save(node)
        elif node['type'] == 'db_create':
            self.execute_db_create(node)
        elif node['type'] == 'db_write':
            self.execute_db_write(node)
        elif node['type'] == 'db_save':
            self.execute_db_save(node)
        elif node['type'] == 'db_read':
            self.execute_db_read(node)

    def execute_function(self, node):
        for statement in node['body']:
            self.execute(statement)

    def execute_assign(self, node):
        var_name = node['var']
        value = self.evaluate_expr(node['value'])
        self.variables[var_name] = value

    def execute_function_call(self, node):
        func_name = node['name']
        args = [self.evaluate_expr(arg) for arg in node['args']]
        # Placeholder for function calls; currently only supports print and input
        return None

    def execute_print(self, node):
        print(node['value'])

    def execute_print_var(self, node):
        var_name = node['var']
        if var_name in self.variables:
            print(self.variables[var_name])
        else:
            print(f"Undefined variable: {var_name}")

    def execute_input(self, node):
        prompt = node['prompt']
        var_name = node['var']
        input_value = input(prompt)
        self.variables[var_name] = input_value

    def execute_if(self, node):
        condition = node['condition']
        if self.evaluate_condition(condition):
            for statement in node['true_body']:
                self.execute(statement)
        elif node['false_body']:
            for statement in node['false_body']:
                self.execute(statement)

    def execute_file_create(self, node):
        filename = f"{node['filename']}.{node['extension']}"
        self.current_file = open(filename, "w")

    def execute_file_write(self, node):
        if self.current_file:
            var_name = node['var']
            if var_name in self.variables:
                self.current_file.write(self.variables[var_name] + "\n")

    def execute_file_save(self, node):
        if self.current_file:
            self.current_file.close()
            self.current_file = None

    def execute_db_create(self, node):
        db_name = f"{node['db_name']}.db"
        self.current_db = sqlite3.connect(db_name)

    def execute_db_write(self, node):
        if self.current_db:
            var_name = node['var']
            if var_name in self.variables:
                cursor = self.current_db.cursor()
                cursor.execute(self.variables[var_name])
                self.current_db.commit()

    def execute_db_save(self, node):
        if self.current_db:
            self.current_db.close()
            self.current_db = None

    def execute_db_read(self, node):
        if self.current_db:
            cursor = self.current_db.cursor()
            cursor.execute(node['query'])
            result = cursor.fetchall()
            self.variables[node['var']] = result

    def evaluate_expr(self, expr):
        if isinstance(expr, str):
            if expr in self.variables:
                return self.variables[expr]
            return expr.strip('"')
        return expr

    def evaluate_condition(self, condition):
        left = self.evaluate_expr(condition['left'])
        right = self.evaluate_expr(condition['right'])
        op = condition['op']
        if         op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>':
            return left > right
        elif op == '>=':
            return left >= right
        elif op == '<':
            return left < right
        elif op == '<=':
            return left <= right
        return False

    def run(self, tree):
        for function in tree:
            self.execute(function)

def run_escript(code):
    parsed_code = parse_escript(code)
    interpreter = EScriptInterpreter()
    interpreter.run(parsed_code)
