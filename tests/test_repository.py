import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from repositories.user_repository import UserRepository
from database.connection import init_db

def test_user_repository_flow():
    """Testa o fluxo completo de criação e autenticação via UserRepository."""
    init_db()

    email_teste = "dev@ecovida.com"
    # Tenta criar o usuário
    UserRepository.create_user("Engenheiro Teste", email_teste, "senhaSuperSegura123")

    # Valida autenticação com senha correta
    user_auth = UserRepository.authenticate(email_teste, "senhaSuperSegura123")
    assert user_auth is not None, "A autenticação deveria ter sucedido com a senha correta."

    # Valida bloqueio com senha incorreta
    user_auth_invalido = UserRepository.authenticate(email_teste, "senha_errada")
    assert user_auth_invalido is None, "A autenticação deveria ter falhado com a senha incorreta."