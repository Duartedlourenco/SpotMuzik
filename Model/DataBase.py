import sqlite3

class DataBase:
    def __init__(self, db_name='app.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self): #Criação da tabela utilizador
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Utilizador (
                nome TEXT PRIMARY KEY,
                password TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    def insert_utilizador(self, nome, password): #Inserir um novo utilizador na  tabela
        try:
            self.cursor.execute('INSERT INTO Utilizador (nome, password) VALUES (?, ?)', (nome, password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def fetch_utilizador(self): #Aceder à base de dados para recolher todos os clientes
        self.cursor.execute('SELECT nome, password FROM Utilizador')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()