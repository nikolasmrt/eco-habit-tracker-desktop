from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.styles.theme import EcoTheme

class TipsView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eco-Vida - Guia de Dicas")
        self.setFixedSize(700, 550)
        self.setup_ui()
        self.setStyleSheet(EcoTheme.CYBER_ECO_QSS)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("🌿 Guia de Hábitos Sustentáveis")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #34d399; background: transparent;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)

        tips = [
            ("💧 Água", "Tome banhos curtos (<5 min) e feche a torneira ao escovar os dentes."),
            ("⚡ Energia", "Desligue aparelhos da tomada em standby e priorize lâmpadas LED."),
            ("🚗 Transporte", "Utilize transporte público, bicicletas ou caminhe em trajetos curtos."),
            ("🗑️ Resíduos", "Separe o lixo reciclável e pratique a compostagem de orgânicos.")
        ]

        for cat, desc in tips:
            card = QFrame()
            card_layout = QVBoxLayout(card)
            c_label = QLabel(cat)
            c_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
            c_label.setStyleSheet("color: #34d399; background: transparent;")
            
            d_label = QLabel(desc)
            d_label.setWordWrap(True)
            d_label.setStyleSheet("color: #e2e8f0; background: transparent;")
            
            card_layout.addWidget(c_label)
            card_layout.addWidget(d_label)
            content_layout.addWidget(card)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        btn = QPushButton("Fechar")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, alignment=Qt.AlignCenter)