import sqlite3
import os
from contextlib import contextmanager

# Definir caminho do banco de dados na raiz
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "eco_habit_tracker.db")


@contextmanager
def conectar_db():
    """Context Manager para  garantir abertura e fechamento seguro das conexões SQLite."""
    conectar = sqlite3.Connection(db_path)
    conectar.row_factory = sqlite3.Row
    try:
        yield conectar
        conectar.commit()
    except sqlite3.Error as e:
        conectar.rollback()
        print(f"[Database Error] Transação revertida: {e}")
        raise e
    finally:
        conectar.close()
        
def iniciar_db():
    """Inicializa as tabelas do banco de dados SQLite se não existirem."""
    with conectar_db() as conectar:
        cursor = conectar.cursor()
        
        # 1- Tabela de Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        
        # 2- Tabela de Hábitos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                unidade TEXT,
                categoria TEXT NOT NULL
            )
        """)
        
        # 3- Tabela de Registros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                habito_id INTEGER,
                data_registro DATE,
                quantidade REAL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (habito_id) REFERENCES habitos (id)
            )
        """)
        print("✅ Banco de dados SQLite inicializado com sucesso.")

if __name__ == "__main__":
    iniciar_db()