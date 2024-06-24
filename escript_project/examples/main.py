from escript.escript_interpreter import run_escript

code = '''
function main() {
    File.create("example", "txt");
    File.write("Hello World");
    File.save();

    Db.create("example_db");
    Db.write("CREATE TABLE IF NOT EXISTS example_table (id INTEGER PRIMARY KEY, name TEXT)");
    Db.write("INSERT INTO example_table (name) VALUES ('Alice')");
    Db.write("INSERT INTO example_table (name) VALUES ('Bob')");
    Db.save();

    result = Db.read("example_db")("SELECT * FROM example_table");
    P$result;
}
'''

run_escript(code)
