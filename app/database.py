import sqlite3


def get_db_connection():
    try:
        conn = sqlite3.connect('contabilidade.db')
        return conn
    except sqlite3.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contas_contabeis (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            descricao TEXT,
            is_duplicate BOOLEAN DEFAULT 0,
            is_deleted BOOLEAN DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS centros_custo (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            descricao TEXT,
            is_duplicate BOOLEAN DEFAULT 0,
            is_deleted BOOLEAN DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY,
            conta_contabil_id INTEGER,
            centro_custo_id INTEGER,
            historico TEXT,
            tipo TEXT CHECK(tipo IN ('Crédito', 'Débito')),
            valor REAL,
            data TEXT,
            is_duplicate BOOLEAN DEFAULT 0,
            is_deleted BOOLEAN DEFAULT 0,
            FOREIGN KEY (conta_contabil_id) REFERENCES contas_contabeis(id),
            FOREIGN KEY (centro_custo_id) REFERENCES centros_custo(id)
        )
    ''')

    conn.commit()
    conn.close
