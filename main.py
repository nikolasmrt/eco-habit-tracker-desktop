import sys
import os

# Configuração do Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from PySide6.QtWidgets import QApplication
from database.connection import init_db
from ui.main_window import MainWindow


def main():
    """
    Ponto de entrada (Bootstrapper) principal da aplicação Eco-Vida Desktop.
    Responsável por inicializar a infraestrutura relacional e disparar o loop de eventos da GUI.
    """
    print("🚀 Inicializando Eco-Vida Sustentabilidade...")

    # Inicialização da Infraestrutura de Dados
    try:
        init_db()
    except Exception as e:
        print(f"❌ Erro crítico ao inicializar o banco de dados: {e}")
        sys.exit(1)

    # Instanciação do loop de eventos da interface gráfica
    app = QApplication(sys.argv)

    # Carregamento do gerenciador de navegação central 
    window = MainWindow()
    window.show()

    # Execução do ciclo de vida da aplicação
    sys.exit(app.exec())


if __name__ == "__main__":
    main()