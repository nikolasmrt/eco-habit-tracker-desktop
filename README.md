# ♻️ Eco-Vida: Desktop Habit & Sustainability Tracker

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Software Desktop orientado a objetos desenvolvido em Python, estruturado sob os princípios de **Clean Architecture**, focado na conscientização, monitoramento e análise de consumo e hábitos sustentáveis diários. A aplicação permite o registo seguro de atividades por categoria, cálculo automatizado de impacto ecológico (gamificação), visualização de gráficos estatísticos e exportação de relatórios profissionais em PDF.

---

## 🏛️ Arquitetura do Sistema

O sistema adota uma separação estrita de responsabilidades em camadas, garantindo baixo acoplamento e alta testabilidade entre a Interface Gráfica (PySide6), as Regras de Negócio e a Persistência Local (SQLite3).

```mermaid
graph TD
    A[main.py - Bootstrapper] --> B[src/ui/main_window.py]
    B --> C[src/ui/views/login_view.py]
    B --> D[src/ui/views/register_view.py]
    B --> E[src/ui/views/dashboard_view.py]
    
    E --> F[src/ui/views/analytics_view.py]
    E --> G[src/ui/views/tips_view.py]
    
    C & D --> H[src/repositories/user_repository.py]
    E --> I[src/repositories/habit_repository.py]
    
    E --> J[src/services/score_service.py]
    E --> K[src/services/pdf_report_service.py]
    
    H & I --> L[src/database/connection.py]
    L --> M[(eco_habit_tracker.db - SQLite)]
