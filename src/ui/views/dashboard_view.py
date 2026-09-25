import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QTabWidget, QStatusBar
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QFont, QColor

from repositories.habit_repository import HabitRepository
from services.score_service import ScoreService
from services.pdf_report_service import PdfReportService

from ui.views.analytics_view import GraphWindow
from ui.views.tips_view import TipsView
from ui.styles.theme import EcoTheme

from ui.styles.animations import HudAnimations

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICON_PATH = os.path.join(BASE_DIR, "assets", "eco_icon.ico")


class DashboardView(QMainWindow):
    logout_successful = Signal()

    def __init__(self, user_id: int, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.setWindowTitle("Eco-Vida — Dashboard")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        self.setFixedSize(1024, 768)

        self.setup_ui()
        self.setStyleSheet(EcoTheme.CYBER_ECO_QSS)
        self.update_score_display()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.titulo = QLabel("ECO-VIDA")
        self.titulo.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("color: #00ffcc;")
        HudAnimations.apply_glow_shadow(self.titulo, blur_radius=25, color=QColor(0, 255, 204, 80))
        main_layout.addWidget(self.titulo)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.setup_habit_registration_tab()
        self.setup_reports_tab()
        self.setup_settings_tab()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🟢 Conexão Estável. Sistema Pronto.")

        self.mensagem = QLabel("")
        self.mensagem.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.mensagem)

    def setup_habit_registration_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        group = QGroupBox("Registrar Novo Hábito")
        form = QFormLayout(group)

        self.entrada_habito = QLineEdit()
        self.entrada_habito.setPlaceholderText("Ex: Banho rápido")
        form.addRow("Nome:", self.entrada_habito)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(["Água", "Energia", "Transporte", "Resíduos"])
        self.combo_categoria.currentIndexChanged.connect(self.update_unit_combo)
        form.addRow("Categoria:", self.combo_categoria)

        self.entrada_quantidade = QDoubleSpinBox()
        self.entrada_quantidade.setRange(0.01, 10000.00)
        self.entrada_quantidade.setValue(1.0)
        form.addRow("Quantidade:", self.entrada_quantidade)

        self.unidades_map = {
            "Água": ["litros", "ml"], "Energia": ["kWh", "MWh"],
            "Transporte": ["km", "milhas"], "Resíduos": ["kg", "g"]
        }
        self.combo_unidade = QComboBox()
        self.update_unit_combo(0)
        form.addRow("Unidade:", self.combo_unidade)

        btn = QPushButton("Registrar Hábito")
        btn.clicked.connect(self.registrar_habito)
        form.addRow(btn)

        layout.addWidget(group)
        self.tab_widget.addTab(widget, "📝 Registro")

    @Slot(int)
    def update_unit_combo(self, index: int):
        cat = self.combo_categoria.currentText()
        self.combo_unidade.clear()
        self.combo_unidade.addItems(self.unidades_map.get(cat, []))

    def setup_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        group = QGroupBox("Métricas de Impacto")
        score_layout = QVBoxLayout(group)
        self.score_label = QLabel("Pontuação Atual: Calculando...")
        self.score_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.score_label.setStyleSheet("color: #34d399;")
        score_layout.addWidget(self.score_label)
        layout.addWidget(group)

        btn_graph = QPushButton("📊 Ver Gráfico de Consumo")
        btn_graph.clicked.connect(self.open_graph_window)
        layout.addWidget(btn_graph)

        btn_pdf = QPushButton("📄 Exportar Relatório PDF")
        btn_pdf.clicked.connect(self.exportar_pdf)
        layout.addWidget(btn_pdf)

        self.tab_widget.addTab(widget, "📊 Relatórios")

    def setup_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Grupo: Base de Conhecimento
        group_prefs = QGroupBox("MÓDULOS DE CONHECIMENTO")
        form_prefs = QVBoxLayout(group_prefs)
        form_prefs.setSpacing(15)

        lbl_info = QLabel("Aceda aos protocolos de preservação e metas de otimização de recursos globais.")
        lbl_info.setStyleSheet("color: #94a3b8; font-size: 13px;")
        form_prefs.addWidget(lbl_info)

        btn_tips = QPushButton("INICIAR GUIA SUSTENTÁVEL")
        btn_tips.clicked.connect(self.abrir_dicas)
        form_prefs.addWidget(btn_tips)

        layout.addWidget(group_prefs)

        # Grupo: Risco & Segurança
        group_session = QGroupBox("SEGURANÇA DE SISTEMA")
        group_session.setStyleSheet("color: #ff003c; border: 1px solid rgba(255, 0, 60, 40);")
        form_session = QVBoxLayout(group_session)
        form_session.setSpacing(15)

        lbl_session_info = QLabel("Encerre a conexão com a base de dados de forma segura para prevenir violações.")
        lbl_session_info.setStyleSheet("color: #94a3b8; font-size: 13px;")
        form_session.addWidget(lbl_session_info)

        btn_logout = QPushButton("DESCONECTAR SESSÃO")
        btn_logout.setObjectName("logout_btn") 
        btn_logout.clicked.connect(self.efetuar_logout)
        form_session.addWidget(btn_logout)

        layout.addWidget(group_session)
        layout.addStretch()

        self.tab_widget.addTab(widget, "⚙️ Configurações")

    def registrar_habito(self):
        nome = self.entrada_habito.text().strip()
        cat = self.combo_categoria.currentText()
        unidade = self.combo_unidade.currentText()
        qtd = self.entrada_quantidade.value()

        if not nome:
            QMessageBox.warning(self, "Aviso", "Informe o nome do hábito.")
            return

        h_id = HabitRepository.get_or_create_habit(nome, unidade, cat)
        if HabitRepository.add_record(self.user_id, h_id, qtd):
            self.mensagem.setText("✅ Hábito registrado com sucesso!")
            self.mensagem.setStyleSheet("color: #34d399; font-weight: bold;")
            self.entrada_habito.clear()
            self.update_score_display()

    def update_score_display(self):
        score = ScoreService.calculate_user_score(self.user_id)
        self.score_label.setText(f"Pontuação Atual: {score} pontos")

    def exportar_pdf(self):
        if PdfReportService.generate_pdf_report(self.user_id):
            QMessageBox.information(self, "Sucesso", "Relatório PDF gerado na raiz do projeto!")
        else:
            QMessageBox.warning(self, "Aviso", "Nenhum dado encontrado para exportar.")

    def abrir_dicas(self):
        TipsView(self).exec()

    def open_graph_window(self):
        GraphWindow(self.user_id, self).exec()

    def efetuar_logout(self):
        self.close()
        self.logout_successful.emit()