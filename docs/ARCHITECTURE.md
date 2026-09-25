# 📐 Arquitetura de Software - Eco-Vida Desktop

O projeto **Eco-Vida** foi concebido seguindo os princípios da **Clean Architecture** (Arquitetura Limpa) e padrões de projeto consolidados (*Design Patterns*), assegurando manutenibilidade e escalabilidade.

## 📂 Organização de Diretórios (`src/` e `tests/`)

```text
eco-habit-tracker-desktop/
├── src/
│   ├── database/          # Infraestrutura e gestão de conexões SQLite
│   ├── repositories/      # Camada de Acesso a Dados (Repository Pattern)
│   ├── services/          # Regras de Negócio, Gamificação e Relatórios
│   └── ui/                # Camada de Apresentação (PySide6)
│       ├── views/         # Telas específicas (Login, Registo, Dashboard, Gráficos, Dicas)
│       └── main_window.py # Router central (QStackedWidget)
├── tests/                 # Testes unitários e de integração (pytest)
├── assets/                # Recursos estáticos (ícones, imagens)
├── docs/                  # Documentação técnica detalhada
├── main.py                # Bootstrapper da aplicação
└── requirements.txt       # Dependências do projeto