from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap, QImage
from io import BytesIO
import matplotlib.pyplot as plt

from repositories.habit_repository import HabitRepository
from ui.styles.theme import EcoTheme

class GraphWindow(QDialog):
    def __init__(self, usuario_id: int, parent=None):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.setWindowTitle("Eco-Vida - Gráfico de Consumo")
        self.setFixedSize(750, 550)
        self.setup_ui()
        self.setStyleSheet(EcoTheme.CYBER_ECO_QSS)
        self.load_graph()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("📊 Consumo Consolidado por Categoria")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #34d399; background: transparent;")
        layout.addWidget(title)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background: transparent;")
        layout.addWidget(self.image_label)

        btn = QPushButton("Fechar")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)

    def load_graph(self):
        dados = HabitRepository.get_category_totals(self.usuario_id)
        if not dados:
            self.image_label.setText("Sem dados para exibir.")
            return

        cats = [d[0] for d in dados]
        totais = [d[1] for d in dados]

        # Configuração do gráfico
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(cats, totais, color='#10b981')
        ax.set_title("Consumo por Categoria", color='#e2e8f0')
        ax.tick_params(colors='#e2e8f0')
        fig.patch.set_facecolor('#0b0f19')
        ax.set_facecolor('#0f172a')
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png', transparent=True, bbox_inches='tight')
        plt.close()
        buffer.seek(0)

        image = QImage.fromData(buffer.getvalue())
        self.image_label.setPixmap(QPixmap.fromImage(image))