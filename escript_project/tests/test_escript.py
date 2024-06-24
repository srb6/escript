from escript.escript_interpreter import run_escript

code = '''
function main() {
    var1 = "World";
    P("Hello");
    name = IN("Enter Name: ");
    if (name == "Alice") {
        P("Hello Alice");
    } else {
        P("Hello " + name);
    }
}
'''

run_escript(code)
