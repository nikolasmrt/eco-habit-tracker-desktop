import os
import matplotlib.pyplot as plt
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from repositories.user_repository import UserRepository
from repositories.habit_repository import HabitRepository
from services.score_service import ScoreService

class PdfReportService:
    """Serviço responsável pela compilação de dados, geração de gráficos estáticos e exportação de relatórios em PDF."""

    @staticmethod
    def generate_pdf_report(user_id: int) -> bool:
        user = UserRepository.find_by_id(user_id)
        if not user:
            return False

        category_data = HabitRepository.get_category_totals(user_id)
        if not category_data:
            return False

        pdf = FPDF()
        pdf.add_page()

        # Cabeçalho do Relatório 
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, "Relatório de Sustentabilidade - Eco-Vida", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(5)

        # Informações Cadastrais do Usuário
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(0, 8, f"Usuário: {user['nome']} ({user['email']})", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 8, f"Data do Relatório: {datetime.now().strftime('%d/%m/%Y %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        score = ScoreService.calculate_user_score(user_id)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, f"Pontuação Atual: {score} pontos", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

        # Geração de Gráfico Temporário
        chart_path = f"temp_chart_{user_id}.png"
        try:
            categories = [item[0] for item in category_data]
            totals = [item[1] for item in category_data]

            plt.figure(figsize=(6, 3.5))
            plt.bar(categories, totals, color='#27ae60')
            plt.xlabel("Categoria")
            plt.ylabel("Consumo Total")
            plt.title("Consumo Consolidado por Categoria")
            plt.tight_layout()
            plt.savefig(chart_path, dpi=150)
            plt.close()

            pdf.image(chart_path, x=20, w=170)
            pdf.ln(5)
        except Exception as e:
            print(f"[PDF Error] Erro ao gerar imagem do gráfico: {e}")
        finally:
            if os.path.exists(chart_path):
                os.remove(chart_path)

        # Tabela de Registros
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(60, 8, "Categoria", border=1)
        pdf.cell(60, 8, "Hábito", border=1)
        pdf.cell(40, 8, "Consumo Total", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        records = HabitRepository.get_user_records_grouped(user_id)
        pdf.set_font("Helvetica", "", 10)
        for row in records:
            pdf.cell(60, 8, str(row['categoria'])[:25], border=1)
            pdf.cell(60, 8, str(row['nome'])[:25], border=1)
            pdf.cell(40, 8, str(row['total']), border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        output_path = f"relatorio_sustentabilidade_{user_id}.pdf"
        pdf.output(output_path)
        return True