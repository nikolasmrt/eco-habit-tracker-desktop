# ♻️ Eco-Vida: Desktop Habit & Sustainability Tracker

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt6-green?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

Software Desktop orientado a objetos para conscientização, monitoramento e análise de consumo e hábitos sustentáveis diários. A aplicação permite que usuários registrem atividades por categoria, calculem métricas de impacto ecológico, visualizem gráficos estatísticos e gerem relatórios automatizados em PDF.

---

## 🏛️ Arquitetura do Sistema

A aplicação adota uma arquitetura modular em camadas, separando as responsabilidades da **Interface Gráfica (PySide6/Qt)**, **Regras de Negócio/Cálculos** e **Persistência Local de Dados (SQLite3)**.

```mermaid
graph TD
    A[main.py - Entry Point] --> B[QStackedWidget - Manager de Telas]
    B --> C[ui/login.py - Autenticação]
    B --> D[ui/register.py - Cadastro]
    B --> E[ui/sistema.py - Dashboard Principal]
    
    E --> F[ui/graph_window.py - Visualização Matplotlib]
    E --> G[ui/dicas_sustentaveis_app.py - Engine de Recomendações]
    
    C & D & E & G --> H[database/connection.py - Context Manager]
    H --> I[(eco_habit_tracker.db - SQLite3)]