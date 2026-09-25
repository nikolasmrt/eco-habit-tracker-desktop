import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QFont, QColor, QPixmap

from repositories.user_repository import UserRepository
from ui.styles.theme import EcoTheme
from ui.styles.animations import HudAnimations

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICON_PATH = os.path.join(BASE_DIR, "assets", "eco_icon.ico")


class Register(QWidget):
    registration_successful = Signal()
    go_to_login = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eco-Vida - Criar Identidade")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        self.setFixedSize(640, 640)
        self.setup_ui()
        self.setStyleSheet(EcoTheme.CYBER_ECO_QSS)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        card_frame = QFrame()
        card_frame.setObjectName("auth_card")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(16)
        card_layout.setContentsMargins(35, 30, 35, 30)

        HudAnimations.apply_glow_shadow(card_frame, blur_radius=30, color=QColor(0, 255, 204, 60))

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        if os.path.exists(ICON_PATH):
            pixmap = QPixmap(ICON_PATH).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("♻")
            logo_label.setFont(QFont("Segoe UI", 48, QFont.Bold))
            logo_label.setStyleSheet("color: #00ffcc;")

        HudAnimations.apply_glow_shadow(logo_label, blur_radius=20, color=QColor(0, 255, 204, 120))
        card_layout.addWidget(logo_label)

        title_label = QLabel("NOVO OPERADOR")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; letter-spacing: 2px;")
        card_layout.addWidget(title_label)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        lbl_nome = QLabel("Identificação Completa")
        lbl_nome.setStyleSheet("color: #00ffcc; font-weight: bold; font-size: 12px;")
        self.nome_entry = QLineEdit()
        self.nome_entry.setPlaceholderText("Nome do Operador")
        form_layout.addWidget(lbl_nome)
        form_layout.addWidget(self.nome_entry)

        lbl_email = QLabel("Canal de Comunicação (E-mail)")
        lbl_email.setStyleSheet("color: #00ffcc; font-weight: bold; font-size: 12px;")
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("operador@ecovida.com")
        form_layout.addWidget(lbl_email)
        form_layout.addWidget(self.email_entry)

        lbl_senha = QLabel("Chave de Encriptação (Senha)")
        lbl_senha.setStyleSheet("color: #00ffcc; font-weight: bold; font-size: 12px;")
        self.senha_entry = QLineEdit()
        self.senha_entry.setEchoMode(QLineEdit.Password)
        self.senha_entry.setPlaceholderText("Mínimo 6 caracteres")
        form_layout.addWidget(lbl_senha)
        form_layout.addWidget(self.senha_entry)

        card_layout.addLayout(form_layout)
        card_layout.addSpacing(10)

        register_button = QPushButton("GERAR CREDENCIAL")
        register_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        register_button.clicked.connect(self.button_register)
        card_layout.addWidget(register_button)

        login_button = QPushButton("Possui credencial ativa? Logar")
        login_button.setFlat(True)
        login_button.clicked.connect(self.abrir_login)
        card_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(card_frame)

    def button_register(self):
        nome = self.nome_entry.text().strip()
        email = self.email_entry.text().strip()
        senha = self.senha_entry.text().strip()

        if not nome or not email or not senha:
            QMessageBox.warning(self, "Protocolo Incompleto", "Forneça todos os dados vitais.")
            return

        if UserRepository.create_user(nome, email, senha):
            self.registration_successful.emit()
        else:
            QMessageBox.critical(self, "Falha de Conflito", "A credencial informada já está mapeada no sistema.")

    def abrir_login(self):
        self.go_to_login.emit()