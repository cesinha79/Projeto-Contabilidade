import sqlite3

def init_db():
    conn = sqlite3.connect('app/contabilidade.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS contas_contabeis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        descricao TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS centros_custo (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        descricao TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conta_contabil_id INTEGER,
                        centro_custo_id INTEGER,
                        descricao TEXT,
                        valor REAL,
                        data DATE,
                        FOREIGN KEY(conta_contabil_id) REFERENCES contas_contabeis(id),
                        FOREIGN KEY(centro_custo_id) REFERENCES centros_custo(id))''')

    conn.commit()
    conn.close()
