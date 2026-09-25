import os
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt, Slot

from ui.views.login_view import Login
from ui.views.register_view import Register
from ui.views.dashboard_view import DashboardView
from ui.styles.theme import EcoTheme
from ui.styles.animations import HudAnimations

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ICON_PATH = os.path.join(BASE_DIR, "assets", "eco_icon.ico")


class MainWindow(QMainWindow):
    """Router central de navegação com HUD futurista."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eco-Vida")
        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.setFixedSize(700, 550)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("♻")
        self.title_label.setFont(QFont("Segoe UI", 36, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.welcome_label = QLabel("Sistema de Inteligência e Monitoramento Sustentável")
        self.welcome_label.setFont(QFont("Segoe UI", 12))
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color: #64748b;")
        self.layout.addWidget(self.welcome_label)

        self.enter_button = QPushButton("INICIALIZAR SISTEMA")
        self.enter_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.enter_button.clicked.connect(self.show_auth_screens)
        self.layout.addWidget(self.enter_button, alignment=Qt.AlignCenter)
        
        HudAnimations.apply_glow_shadow(self.enter_button)

        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)
        self.stacked_widget.hide()

        self.dashboard_screen = None
        self.setup_auth_screens()
        self.setStyleSheet(EcoTheme.CYBER_ECO_QSS)

    def setup_auth_screens(self):
        self.login_screen = Login(self)
        self.register_screen = Register(self)

        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.register_screen)

        self.login_screen.login_successful.connect(self.show_dashboard_screen)
        self.login_screen.go_to_register.connect(self.show_register_screen)
        
        self.register_screen.registration_successful.connect(self.show_login_screen_after_register)
        self.register_screen.go_to_login.connect(self.show_login_screen)

    def show_auth_screens(self):
        self.title_label.hide()
        self.welcome_label.hide()
        self.enter_button.hide()
        self.stacked_widget.show()
        self.setFixedSize(self.login_screen.size())
        self.stacked_widget.setCurrentWidget(self.login_screen)
        HudAnimations.fade_in(self.login_screen)

    @Slot(int)
    def show_dashboard_screen(self, user_id: int):
        self.stacked_widget.hide()
        if self.dashboard_screen is not None:
            self.dashboard_screen.close()
            self.dashboard_screen.deleteLater()

        self.dashboard_screen = DashboardView(user_id=user_id, parent=self)
        self.dashboard_screen.logout_successful.connect(self.show_login_screen_after_logout)
        self.dashboard_screen.show()
        self.hide()

    @Slot()
    def show_login_screen(self):
        self.setFixedSize(self.login_screen.size())
        self.stacked_widget.setCurrentWidget(self.login_screen)

    @Slot()
    def show_register_screen(self):
        self.setFixedSize(self.register_screen.size())
        self.stacked_widget.setCurrentWidget(self.register_screen)

    @Slot()
    def show_login_screen_after_register(self):
        self.show_login_screen()

    @Slot()
    def show_login_screen_after_logout(self):
        self.show()
        self.stacked_widget.show()
        self.show_login_screen()
        self.setFixedSize(self.login_screen.size())