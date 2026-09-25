import sqlite3
import os
from contextlib import contextmanager

# Mapeamento do caminho do .db 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "eco_habit_tracker.db")

@contextmanager
def get_db_connection():
    """
    Context Manager para gerenciar o ciclo de vida da conexão com o SQLite.
    Garante o fechamento seguro da conexão, efetua commit em caso de sucesso
    e rollback automático caso ocorra qualquer exceção SQL.
    """
    
    conn = sqlite3.connect(DB_PATH)
    
    
    conn.row_factory = sqlite3.Row 
    
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"[Database Error] Transação revertida devido a falha: {e}")
        raise e
    finally:
        conn.close()

def init_db():
    """
    Inicializa a estrutura (DDL) das tabelas no SQLite caso o banco seja novo.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 1. Tabela de Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        
        # 2. Tabela de Hábitos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                unidade TEXT,
                categoria TEXT NOT NULL
            )
        """)
                
        # 3. Tabela de Registros
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS registros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                habito_id INTEGER NOT NULL,
                data_registro DATE NOT NULL,
                quantidade REAL NOT NULL,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
                FOREIGN KEY (habito_id) REFERENCES habitos (id) ON DELETE CASCADE
            )
        """)
        print(f"✅ Esquema de Base de Dados SQLite inicializado com sucesso em:\n   {DB_PATH}")

# Roda diretamente para criar o banco 
if __name__ == "__main__":
    init_db()