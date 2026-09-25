import sqlite3
import bcrypt
from typing import Optional, Dict, Any
from database.connection import get_db_connection

class UserRepository:
    """Repositório responsável pela persistência, busca e autenticação de usuários no SQLite."""

    @staticmethod
    def create_user(nome: str, email: str, senha_plana: str) -> bool:
        """
        Cadastra um novo usuário no banco de dados com a senha criptografada via bcrypt.
        """
        if not nome or not email or not senha_plana:
            return False

        senha_bytes = senha_plana.encode('utf-8')
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO usuarios (nome, email, senha)
                    VALUES (?, ?, ?)
                """, (nome.strip(), email.strip().lower(), senha_hash))
                return True
        except sqlite3.IntegrityError:
            print(f"[UserRepository Warning] Tentativa de cadastro com e-mail já existente: {email}")
            return False
        except sqlite3.Error as e:
            print(f"[UserRepository Error] Erro ao cadastrar usuário: {e}")
            return False

    @staticmethod
    def authenticate(email: str, senha_plana: str) -> Optional[int]:
        """
        Valida o e-mail e verifica se o hash da senha bate com o informado.
        Retorna o ID do usuário em caso de sucesso, ou None.
        """
        if not email or not senha_plana:
            return None

        user = UserRepository.find_by_email(email)
        if not user:
            return None

        try:
            senha_armazenada_bytes = user['senha'].encode('utf-8')
            senha_enviada_bytes = senha_plana.encode('utf-8')

            if bcrypt.checkpw(senha_enviada_bytes, senha_armazenada_bytes):
                return int(user['id'])
        except (ValueError, TypeError) as e:
            print(f"[UserRepository Error] Falha ao verificar hash da senha: {e}")

        return None

    @staticmethod
    def find_by_email(email: str) -> Optional[Dict[str, Any]]:
        """Busca um usuário pelo e-mail (case-insensitive)."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email, senha 
                FROM usuarios 
                WHERE LOWER(email) = LOWER(?)
            """, (email.strip(),))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def find_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """Busca as informações do usuário pelo ID (omitindo a senha por segurança)."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, email 
                FROM usuarios 
                WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None