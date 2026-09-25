import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from database.connection import init_db
from repositories.user_repository import UserRepository
from repositories.habit_repository import HabitRepository
from services.score_service import ScoreService
from services.pdf_report_service import PdfReportService

def test_services_and_gamification():
    """Testa a engine de cálculo de score e a exportação do relatório em PDF."""
    init_db()

    test_email = "dev@ecovida.com"
    user = UserRepository.find_by_email(test_email)
    if not user:
        UserRepository.create_user("Dev Teste", test_email, "senha123")
        user = UserRepository.find_by_email(test_email)

    assert user is not None
    user_id = user['id']
    
    h_id = HabitRepository.get_or_create_habit("Banho Curto", "litros", "Água")
    HabitRepository.add_record(user_id, h_id, 45.0)

    # Validação do Score
    score = ScoreService.calculate_user_score(user_id)
    assert isinstance(score, float)
    assert score >= 0.0

    # Validação do PDF
    pdf_ok = PdfReportService.generate_pdf_report(user_id)
    assert pdf_ok is True