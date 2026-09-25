import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QFont, QColor, QPixmap

from repositories.user_repository import UserRepository
from ui.styles.theme import EcoTheme
from ui.styles.animations import HudAnimations

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICON_PATH = os.path.join(BASE_DIR, "assets", "eco_icon.ico")


class Login(QWidget):
    login_successful = Signal(int)
    go_to_register = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eco-Vida")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))
        self.setFixedSize(640, 640)
        self.setup_ui()
        self.setStyleSheet(EcoTheme.CYBER_ECO_QSS)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Container Principal 
        card_frame = QFrame()
        card_frame.setObjectName("auth_card")
        card_layout = QVBoxLayout(card_frame)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(35, 40, 35, 40)
        
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

        title_label = QLabel("LOGIN")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; letter-spacing: 2px;")
        card_layout.addWidget(title_label)

        subtitle_label = QLabel("Autenticação requerida para acesso ao painel sustentável")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #94a3b8;")
        card_layout.addWidget(subtitle_label)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        lbl_email = QLabel("Credencial (E-mail)")
        lbl_email.setStyleSheet("color: #00ffcc; font-weight: bold; font-size: 12px;")
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("sys.admin@ecovida.com")
        form_layout.addWidget(lbl_email)
        form_layout.addWidget(self.email_entry)

        lbl_senha = QLabel("Código de Segurança")
        lbl_senha.setStyleSheet("color: #00ffcc; font-weight: bold; font-size: 12px;")
        self.senha_entry = QLineEdit()
        self.senha_entry.setEchoMode(QLineEdit.Password)
        self.senha_entry.setPlaceholderText("••••••••••••")
        form_layout.addWidget(lbl_senha)
        form_layout.addWidget(self.senha_entry)

        card_layout.addLayout(form_layout)
        card_layout.addSpacing(10)

        login_button = QPushButton("INICIAR SESSÃO")
        login_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        login_button.clicked.connect(self.login)
        card_layout.addWidget(login_button)

        register_link_layout = QHBoxLayout()
        register_label = QLabel("Operador não identificado?")
        register_label.setStyleSheet("color: #94a3b8;")
        
        register_link = QPushButton("Registrar")
        register_link.setFlat(True)
        register_link.clicked.connect(self.abrir_registro)
        
        register_link_layout.addStretch()
        register_link_layout.addWidget(register_label)
        register_link_layout.addWidget(register_link)
        register_link_layout.addStretch()
        card_layout.addLayout(register_link_layout)

        main_layout.addWidget(card_frame)

    def login(self):
        email = self.email_entry.text().strip()
        senha = self.senha_entry.text().strip()

        if not email or not senha:
            QMessageBox.warning(self, "Acesso Negado", "Forneça as credenciais completas.")
            return

        usuario_id = UserRepository.authenticate(email, senha)
        if usuario_id:
            self.login_successful.emit(usuario_id)
        else:
            QMessageBox.critical(self, "Falha Crítica", "Credenciais inválidas ou não autorizadas.")

    def abrir_registro(self):
        self.go_to_register.emit()