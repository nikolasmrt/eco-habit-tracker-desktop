class EcoTheme:
    """Design System Futurista / Cyber-Neon com efeito Glassmorphism."""
    
    CYBER_ECO_QSS = """
        /* Global Base: Fundo super escuro (Deep Space) */
        QWidget {
            background-color: #07090f;
            color: #e0e0e0;
            font-family: 'Segoe UI', -apple-system, sans-serif;
            font-size: 14px;
        }

        QMainWindow, QDialog {
            background-color: #07090f;
        }

        /* CORREÇÃO DOS BLOCOS FEIOS: Labels sempre transparentes */
        QLabel {
            background: transparent;
        }

        /* Efeito de Vidro Opaco (Glassmorphism) para os Cartões */
        QFrame#auth_card {
            background-color: rgba(15, 23, 42, 180);
            border: 1px solid rgba(0, 255, 204, 40);
            border-radius: 16px;
        }

        /* Tabs Futuristas */
        QTabWidget::pane {
            border: 1px solid rgba(0, 255, 204, 30);
            background-color: rgba(15, 23, 42, 150);
            border-radius: 12px;
        }
        QTabBar::tab {
            background-color: transparent;
            color: #64748b;
            padding: 12px 24px;
            margin-right: 4px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            font-weight: bold;
            border-bottom: 2px solid transparent;
        }
        QTabBar::tab:selected {
            color: #00ffcc;
            border-bottom: 2px solid #00ffcc;
        }
        QTabBar::tab:hover {
            color: #00ffcc;
        }

        /* GroupBoxes / Containers */
        QGroupBox {
            background-color: rgba(15, 23, 42, 120);
            border: 1px solid rgba(0, 255, 204, 30);
            border-radius: 12px;
            margin-top: 20px;
            padding: 20px;
            font-weight: bold;
            color: #00ffcc;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 10px;
            color: #00ffcc;
        }

        /* Botões Principais - Estilo Cyber-Neon Brilhante */
        QPushButton {
            background-color: #00df9a;
            color: #000000;
            border: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        QPushButton:hover {
            background-color: #00ffcc;
        }
        QPushButton:pressed {
            background-color: #00b377;
            padding-top: 14px;
        }

        /* Botões de Link (Transparentes) */
        QPushButton[flat="true"], QPushButton.link-button {
            background-color: transparent !important;
            color: #00ffcc !important;
            border: none !important;
            padding: 0px !important;
        }
        QPushButton[flat="true"]:hover, QPushButton.link-button:hover {
            color: #ffffff !important;
            text-decoration: underline;
        }

        /* Botão de Logout Neon Red */
        QPushButton#logout_btn {
            background-color: rgba(255, 0, 60, 20);
            color: #ff003c;
            border: 1px solid #ff003c;
        }
        QPushButton#logout_btn:hover {
            background-color: #ff003c;
            color: #ffffff;
        }

        /* Inputs de Texto Dinâmicos & Translúcidos */
        QLineEdit, QDoubleSpinBox, QComboBox {
            background-color: rgba(0, 0, 0, 100);
            border: 1px solid rgba(255, 255, 255, 20);
            border-radius: 8px;
            padding: 12px;
            color: #ffffff;
        }
        QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus {
            border: 1px solid #00ffcc;
            background-color: rgba(0, 255, 204, 10);
        }

        QStatusBar {
            background-color: #07090f;
            color: #00ffcc;
            font-weight: bold;
            border-top: 1px solid rgba(0, 255, 204, 20);
        }
    """