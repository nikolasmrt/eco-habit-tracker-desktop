from typing import List, Dict, Any, Tuple
from datetime import datetime
from database.connection import get_db_connection

class HabitRepository:
    """
    Repositório responsável por isolar todas as operações de persistência,
    consultas e agregações referentes a Hábitos e Registros de Consumo.
    """
    
    @staticmethod
    def get_or_create_habit(nome: str, unidade: str, categoria: str) -> int:
        """
        Busca o ID de um hábito existente com as mesmas características ou cadastra um novo.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id FROM habitos 
                WHERE nome = ? AND unidade = ? AND categoria = ?
            """, (nome.strip(), unidade.strip(), categoria.strip()))
            row = cursor.fetchone()

            if row:
                return row["id"]

            cursor.execute("""
                INSERT INTO habitos (nome, unidade, categoria)
                VALUES (?, ?, ?)
            """, (nome.strip(), unidade.strip(), categoria.strip()))
            return cursor.lastrowid

    @staticmethod
    def add_record(user_id: int, habit_id: int, quantidade: float) -> bool:
        """
        Registra um novo log de consumo associado a um usuário e a um hábito com a data atual.
        """
        data_atual = datetime.now().strftime("%Y-%m-%d")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO registros (usuario_id, habito_id, quantidade, data_registro)
                VALUES (?, ?, ?, ?)
            """, (user_id, habit_id, quantidade, data_atual))
            return True

    @staticmethod
    def get_user_records_grouped(user_id: int) -> List[Dict[str, Any]]:
        """
        Agrega os registros de consumo por categoria e nome do hábito.
        Fundamental para o motor de cálculo do Score de Sustentabilidade.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.categoria, h.nome, SUM(r.quantidade) as total
                FROM registros r
                JOIN habitos h ON r.habito_id = h.id
                WHERE r.usuario_id = ?
                GROUP BY h.categoria, h.nome
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_category_totals(user_id: int) -> List[Tuple[str, float]]:
        """
        Retorna o consumo total agregado por categoria.
        Utilizado exclusivamente para a plotagem dos gráficos (Matplotlib/Qt).
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.categoria, SUM(r.quantidade) as total
                FROM registros r
                JOIN habitos h ON r.habito_id = h.id
                WHERE r.usuario_id = ?
                GROUP BY h.categoria
            """, (user_id,))
            return [(row["categoria"], float(row["total"])) for row in cursor.fetchall()]

    @staticmethod
    def clear_all_records() -> bool:
        """Apaga todos os registros e tipos de hábitos (Hard Reset)."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM registros")
            cursor.execute("DELETE FROM habitos")
            return True

    @staticmethod
    def reset_user_logs(user_id: int) -> bool:
        """Zera apenas os lançamentos de consumo do usuário, mantendo os hábitos."""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM registros WHERE usuario_id = ?", (user_id,))
            return True