from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QTabWidget, QTextEdit, QStatusBar, QMenu, QToolBar
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QFont, QColorConstants, QAction, QPainter

try:
    from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QValueAxis, QBarCategoryAxis
    QTCHARTS_AVAILABLE = True
except ImportError:
    QTCHARTS_AVAILABLE = False
    print("Aviso: PySide6-Charts não encontrado. A funcionalidade de gráfico será desativada.")


from ui.graph_window import GraphWindow

from database.connection import registrar_habito, limpar_dados, zerar_tempos, recomendar_habito, calcular_pontuacao, exportar_para_pdf, obter_dados_grafico_por_categoria

import webbrowser
import subprocess
import os
import sys

site_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui/dicas_sustentaveis_app.py")

ui_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.dirname(ui_dir)
icon_path = os.path.join(current_dir, "assets", "eco_icon.ico")

print(f"Caminho do ícone (sistema.py): {icon_path}")

class Sistema(QMainWindow):
    logout_successful = Signal()

    def __init__(self, usuario_id, parent=None):
        super().__init__(parent)
        self.usuario_id = usuario_id

        self.setWindowTitle("Eco-vida Sustentabilidade - Dashboard")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print(f"Erro: Ícone não encontrado em {icon_path}. Usando ícone padrão.")
            self.setWindowIcon(QIcon())
        self.setFixedSize(1024, 768)

        self.setup_ui()
        self.apply_qss()
        self.update_score_display()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        titulo = QLabel("♻ Eco-vida")
        titulo.setFont(QFont("Arial", 28, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        ctk_label_desc = QLabel("Sistema de Sustentabilidade")
        ctk_label_desc.setFont(QFont("Arial", 18))
        ctk_label_desc.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(ctk_label_desc)

        self.create_actions()
        self.create_menus()
        self.create_toolbar()

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.setup_habit_registration_tab()
        self.setup_reports_tab()
        self.setup_settings_tab()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto para registrar hábitos sustentáveis.")

        self.mensagem = QLabel("")
        self.mensagem.setAlignment(Qt.AlignCenter)
        self.mensagem.setFont(QFont("Arial", 12))
        main_layout.addWidget(self.mensagem)


    def create_actions(self):
        self.register_action = QAction(QIcon(), "Registrar Hábito", self)
        self.register_action.triggered.connect(self.registrar)

        self.show_graph_action = QAction(QIcon(), "Ver Gráfico", self)
        self.show_graph_action.triggered.connect(self.open_graph_window)

        self.recommend_action = QAction(QIcon(), "Ver Recomendação", self)
        self.recommendation_text_edit = QTextEdit()
        self.recommendation_text_edit.setMinimumHeight(100)
        self.recommend_action.triggered.connect(self.recomendar)

        self.calculate_score_action = QAction(QIcon(), "Calcular Pontuação", self)
        self.calculate_score_action.triggered.connect(self.pontuacao)

        self.export_pdf_action = QAction(QIcon(), "Exportar PDF", self)
        self.export_pdf_action.triggered.connect(self.exportar_pdf)

        self.clear_data_action = QAction(QIcon(), "Limpar Dados", self)
        self.clear_data_action.triggered.connect(self.confirmar_limpar)

        self.logout_action = QAction(QIcon(), "Deslogar", self)
        self.logout_action.triggered.connect(self.abrir_login)

        self.open_tips_action = QAction(QIcon(), "Acessar Dicas Sustentáveis", self)
        self.open_tips_action.triggered.connect(self.abrir_dicas)


    def create_menus(self):
        file_menu = self.menuBar().addMenu("&Arquivo")
        file_menu.addAction(self.register_action)
        file_menu.addAction(self.export_pdf_action)
        file_menu.addSeparator()
        file_menu.addAction(self.logout_action)

        data_menu = self.menuBar().addMenu("&Dados")
        data_menu.addAction(self.show_graph_action)
        data_menu.addAction(self.calculate_score_action)
        data_menu.addAction(self.recommend_action)
        data_menu.addSeparator()
        data_menu.addAction(self.clear_data_action)

        help_menu = self.menuBar().addMenu("&Ajuda")
        help_menu.addAction(self.open_tips_action)


    def create_toolbar(self):
        toolbar = self.addToolBar("Ações Rápidas")
        toolbar.addAction(self.register_action)
        toolbar.addAction(self.show_graph_action)
        toolbar.addAction(self.recommend_action)
        toolbar.addAction(self.calculate_score_action)
        toolbar.addSeparator()
        toolbar.addAction(self.export_pdf_action)
        toolbar.addAction(self.clear_data_action)


    def setup_habit_registration_tab(self):
        registration_widget = QWidget()
        registration_layout = QVBoxLayout(registration_widget)
        registration_layout.setContentsMargins(20, 20, 20, 20)

        habit_group = QGroupBox("Registrar Novo Hábito")
        form_layout = QFormLayout(habit_group)

        self.entrada_habito = QLineEdit()
        self.entrada_habito.setPlaceholderText("Ex: Banho rápido")
        self.entrada_habito.setMinimumWidth(300)
        form_layout.addRow("Nome do hábito:", self.entrada_habito)

        self.categoria_var = ["Água", "Energia", "Transporte", "Resíduos"]
        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(self.categoria_var)
        self.combo_categoria.currentIndexChanged.connect(self.update_unit_combo)
        self.combo_categoria.setMinimumWidth(300)
        form_layout.addRow("Categoria:", self.combo_categoria)

        self.entrada_quantidade = QDoubleSpinBox()
        self.entrada_quantidade.setRange(0.01, 10000.00)
        self.entrada_quantidade.setSingleStep(0.1)
        self.entrada_quantidade.setValue(1.0)
        self.entrada_quantidade.setMinimumWidth(300)
        form_layout.addRow("Quantidade:", self.entrada_quantidade)

        self.unidades_map = {
            "Água": ["litros", "ml", "galões"],
            "Energia": ["kWh", "MWh", "Joule"],
            "Transporte": ["km", "milhas", "m"],
            "Resíduos": ["kg", "g", "toneladas"]
        }
        self.combo_unidade = QComboBox()
        self.update_unit_combo(0)
        self.combo_unidade.setMinimumWidth(300)
        form_layout.addRow("Unidade:", self.combo_unidade)

        register_button = QPushButton("Registrar Hábito")
        register_button.clicked.connect(self.registrar)
        form_layout.addRow(register_button)

        registration_layout.addWidget(habit_group)
        self.tab_widget.addTab(registration_widget, "📝 Registro de Hábitos")

    @Slot(int)
    def update_unit_combo(self, index):
        selected_category = self.combo_categoria.currentText()
        self.combo_unidade.clear()
        self.combo_unidade.addItems(self.unidades_map.get(selected_category, []))


    def setup_reports_tab(self):
        reports_widget = QWidget()
        reports_layout = QVBoxLayout(reports_widget)
        reports_layout.setContentsMargins(20, 20, 20, 20)

        score_group = QGroupBox("Sua Pontuação de Sustentabilidade")
        score_layout = QVBoxLayout(score_group)
        self.score_label = QLabel("Pontuação Atual: Calculando...")
        self.score_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.score_label.setAlignment(Qt.AlignCenter)
        score_layout.addWidget(self.score_label)
        calculate_score_btn = QPushButton("Recalcular Pontuação")
        calculate_score_btn.clicked.connect(self.pontuacao)
        score_layout.addWidget(calculate_score_btn)
        reports_layout.addWidget(score_group)

        open_graph_btn = QPushButton("📊 Abrir Gráfico de Consumo")
        open_graph_btn.clicked.connect(self.open_graph_window)
        reports_layout.addWidget(open_graph_btn)


        recommendation_group = QGroupBox("Recomendações Personalizadas")
        recommendation_layout = QVBoxLayout(recommendation_group)
        recommendation_layout.addWidget(self.recommendation_text_edit)
        get_recommendation_btn = QPushButton("Ver Recomendação")
        get_recommendation_btn.clicked.connect(self.recomendar)
        recommendation_layout.addWidget(get_recommendation_btn)
        reports_layout.addWidget(recommendation_group)

        export_btn = QPushButton("Exportar Relatório PDF")
        export_btn.clicked.connect(self.exportar_pdf)
        reports_layout.addWidget(export_btn)

        self.tab_widget.addTab(reports_widget, "📊 Relatórios e Análises")


    def setup_settings_tab(self):
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setContentsMargins(20, 20, 20, 20)

        clear_data_btn = QPushButton("Limpar Todos os Dados")
        clear_data_btn.setStyleSheet("background-color: #dc3545; color: white;")
        clear_data_btn.clicked.connect(self.confirmar_limpar)
        settings_layout.addWidget(clear_data_btn)

        zerar_tempos_btn = QPushButton("Zerar Registros (Manter Hábitos)")
        zerar_tempos_btn.setStyleSheet("background-color: #f0ad4e; color: white;")
        zerar_tempos_btn.clicked.connect(self.zerar_registros_confirm)
        settings_layout.addWidget(zerar_tempos_btn)

        open_tips_btn = QPushButton("🌐 Acessar Dicas Sustentáveis")
        open_tips_btn.setStyleSheet("background-color: #1D4ED8; color: white;")
        open_tips_btn.clicked.connect(self.abrir_dicas)
        settings_layout.addWidget(open_tips_btn)

        logout_btn = QPushButton("Deslogar")
        logout_btn.setStyleSheet("background-color: #771212; color: white;")
        logout_btn.clicked.connect(self.abrir_login)
        settings_layout.addWidget(logout_btn)

        self.tab_widget.addTab(settings_widget, "⚙️ Configurações")


    def apply_qss(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Segoe UI', 'Arial';
            }
            QMenuBar {
                background-color: #34495e;
                color: #ecf0f1;
            }
            QMenuBar::item:selected {
                background-color: #2980b9;
            }
            QToolBar {
                background-color: #34495e;
                spacing: 10px;
                padding: 5px;
            }
            QToolButton {
                background-color: transparent;
                border: none;
                padding: 8px;
                color: #ecf0f1;
            }
            QToolButton:hover {
                background-color: #2980b9;
                border-radius: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #34495e;
                background-color: #34495e;
            }
            QTabBar::tab {
                background: #4a6984;
                color: #ecf0f1;
                padding: 10px 15px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #2c3e50;
                border-bottom-color: #2c3e50;
            }
            QTabBar::tab:hover {
                background: #5b7da0;
            }
            QGroupBox {
                background-color: #3e5c76;
                border: 1px solid #5a7d9b;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 20px;
                color: #ecf0f1;
                font-weight: bold;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: #2c3e50;
                border-radius: 5px;
            }
            QLabel {
                color: #ecf0f1;
            }
            QLineEdit, QDoubleSpinBox, QComboBox, QTextEdit {
                background-color: #4a6984;
                border: 1px solid #5a7d9b;
                border-radius: 5px;
                padding: 10px;
                color: #ecf0f1;
                selection-background-color: #2980b9;
            }
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton[styleSheet*="background-color: #dc3545"] {
                background-color: #dc3545;
            }
            QPushButton[styleSheet*="background-color: #dc3545"]:hover {
                background-color: #c82333;
            }
            QPushButton[styleSheet*="background-color: #f0ad4e"] {
                background-color: #f0ad4e;
            }
            QPushButton[styleSheet*="background-color: #f0ad4e"]:hover {
                background-color: #ed9a0c;
            }
            QPushButton[styleSheet*="background-color: #1D4ED8"] {
                background-color: #1D4ED8;
            }
            QPushButton[styleSheet*="background-color: #1D4ED8"]:hover {
                background-color: #2563EB;
            }
            QPushButton[styleSheet*="background-color: #771212"] {
                background-color: #771212;
            }
            QPushButton[styleSheet*="background-color: #771212"]:hover {
                background-color: #7F1D1D;
            }

            QMessageBox {
                background-color: #3e5c76;
                color: #ecf0f1;
            }
            QMessageBox QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QMessageBox QPushButton:hover {
                background-color: #218838;
            }
            QStatusBar {
                background-color: #34495e;
                color: #ecf0f1;
            }
        """)

    def registrar(self):
        nome = self.entrada_habito.text()
        categoria = self.combo_categoria.currentText()
        unidade = self.combo_unidade.currentText()

        try:
            quantidade = self.entrada_quantidade.value()

            if nome and quantidade > 0:
                sucesso = registrar_habito(self.usuario_id, nome, quantidade, unidade, categoria)
                if sucesso:
                    self.mensagem.setText("✅ Hábito registrado com sucesso!")
                    self.mensagem.setStyleSheet("color: green;")
                    self.entrada_habito.clear()
                    self.entrada_quantidade.setValue(1.0)
                    self.status_bar.showMessage(f"Hábito '{nome}' registrado: {quantidade} {unidade} em {categoria}", 5000)
                    self.update_score_display()
                else:
                    self.mensagem.setText("❌ Erro ao registrar o hábito")
                    self.mensagem.setStyleSheet("color: red;")
            else:
                self.mensagem.setText("❌ Preencha o nome e uma quantidade válida")
                self.mensagem.setStyleSheet("color: red;")
        except ValueError:
            self.mensagem.setText("❌ A quantidade deve ser um número")
            self.mensagem.setStyleSheet("color: red;")
        except Exception as e:
            self.mensagem.setText(f"Erro inesperado: {e}")
            self.mensagem.setStyleSheet("color: red;")


    def recomendar(self):
        try:
            recomendacao = recomendar_habito(self.usuario_id)
            QMessageBox.information(self, "Recomendação de Sustentabilidade", recomendacao)
            self.recommendation_text_edit.setText(recomendacao)
            self.status_bar.showMessage("Recomendação exibida.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar recomendação: {str(e)}")
            self.status_bar.showMessage("Erro ao gerar recomendação.", 5000)

    def pontuacao(self):
        try:
            pontos = calcular_pontuacao(self.usuario_id)
            if pontos is not None:
                QMessageBox.information(self, "Pontuação Total",
                                f"🌱 Sua pontuação sustentável: {pontos} pontos\n\n" +
                                "Quanto mais você economiza nos recursos, maior sua pontuação!\n" +
                                "Continue registrando seus hábitos diários para ver seu progresso.")
                self.score_label.setText(f"Pontuação Atual: {pontos} pontos")
                self.status_bar.showMessage(f"Pontuação calculada: {pontos} pontos.", 5000)
            else:
                QMessageBox.information(self, "Sem Pontuação",
                                "Você ainda não possui registros suficientes para calcular sua pontuação.\n" +
                                "Registre seus hábitos diários para começar a pontuar!")
                self.score_label.setText("Pontuação Atual: N/A")
                self.status_bar.showMessage("Sem pontuação calculada.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao calcular pontuação: {str(e)}")
            self.status_bar.showMessage("Erro ao calcular pontuação.", 5000)

    def update_score_display(self):
        score = calcular_pontuacao(self.usuario_id)
        if score is not None:
            self.score_label.setText(f"Pontuação Atual: {score} pontos")
        else:
            self.score_label.setText("Pontuação Atual: N/A")


    def confirmar_limpar(self):
        resposta = QMessageBox.question(self, "Confirmar", "Tem certeza que deseja limpar TODOS os dados? Esta ação não pode ser desfeita.",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.limpar_dados_completos()

    def limpar_dados_completos(self):
        try:
            if limpar_dados():
                QMessageBox.information(self, "Limpeza", "📂 Todos os registros foram apagados.")
                self.status_bar.showMessage("Dados limpos.", 5000)
                self.update_score_display()
                self.recommendation_text_edit.clear()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível limpar os dados.")
                self.status_bar.showMessage("Erro ao limpar dados.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao limpar dados: {str(e)}")
            self.status_bar.showMessage("Erro ao limpar dados.", 5000)

    def zerar_registros_confirm(self):
        resposta = QMessageBox.question(self, "Confirmar", "Tem certeza que deseja zerar apenas os registros de hábitos, mantendo os tipos de hábitos?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if resposta == QMessageBox.Yes:
            self.zerar_registros_apenas()

    def zerar_registros_apenas(self):
        try:
            if zerar_tempos():
                QMessageBox.information(self, "Zerar Registros", "⏰ Todos os registros de hábitos foram zerados.")
                self.status_bar.showMessage("Registros zerados.", 5000)
                self.update_score_display()
                self.recommendation_text_edit.clear()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível zerar os registros.")
                self.status_bar.showMessage("Erro ao zerar registros.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao zerar registros: {str(e)}")
            self.status_bar.showMessage("Erro ao zerar registros.", 5000)


    def exportar_pdf(self):
        try:
            resultado = exportar_para_pdf(self.usuario_id)
            if resultado:
                QMessageBox.information(self, "PDF Gerado", "📄 Relatório PDF gerado com sucesso!")
                self.status_bar.showMessage("PDF exportado com sucesso.", 5000)
            else:
                QMessageBox.critical(self, "Erro", "❌ Não foi possível gerar o relatório PDF. Verifique se você possui registros suficientes ou permissões de escrita.")
                self.status_bar.showMessage("Erro ao exportar PDF.", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"❌ Erro ao gerar o PDF: {str(e)}")
            self.status_bar.showMessage("Erro ao exportar PDF.", 5000)

    def abrir_login(self):
        
        self.close()
        self.logout_successful.emit() 


    def abrir_dicas(self):
        try:
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", site_path])
            self.status_bar.showMessage("Abrindo dicas sustentáveis...", 5000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir dicas sustentáveis: {str(e)}")
            self.status_bar.showMessage("Erro ao abrir dicas Streamlit.", 5000)

    def open_graph_window(self):
        graph_dialog = GraphWindow(self.usuario_id, self)
        graph_dialog.exec()