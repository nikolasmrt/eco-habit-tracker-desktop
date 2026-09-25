# 🚀 Funcionalidades e Regras de Negócio - Eco-Vida

O **Eco-Vida** é um sistema desktop orientado a objetos desenvolvido em Python e PySide6, estruturado sob os princípios de Clean Architecture. Abaixo estão detalhadas as funcionalidades e regras de negócio implementadas na aplicação:

## 1. Autenticação e Segurança

* **Registo Seguro de Utilizadores:** Validação de unicidade de e-mail no SQLite e encriptação de palavras-passe utilizando `bcrypt` com *salt* dinâmico para proteção contra ataques de dicionário e *Rainbow Tables*.
* **Sessão Isolada (User Scoping):** Cada utilizador autenticado possui o seu próprio escopo privado de registos, métricas e pontuações no dashboard central.

## 2. Registo de Hábitos e Consumo

* **Categorização Dinâmica:** Lançamento de atividades parametrizadas por unidades específicas (litros, ml, kWh, MWh, km, kg, g) divididas em quatro pilares ambientais:
  * 💧 **Água**
  * ⚡ **Energia**
  * 🚗 **Transporte**
  * 🗑️ **Resíduos**
* **Prevenção de Duplicidade:** O `HabitRepository` gerencia automaticamente a recuperação ou criação de tipos de hábitos para manter a integridade do catálogo relacional.

## 3. Engine de Gamificação (`ScoreService`)

O cálculo do score de sustentabilidade baseia-se em comparações algorítmicas estritas contra metas de referência por categoria:

* **Bonificação por Economia:** Se o consumo registado for **inferior** à referência estabelecida, o utilizador recebe pontos de bonificação proporcionais à percentagem de recursos poupados, multiplicados pelo peso de impacto da categoria[cite: 2, 9].
* **Penalização por Excesso:** Se o consumo for **superior** à referência, aplica-se uma penalização proporcional ao excesso de recursos consumidos[cite: 2, 9].
* **Piso de Pontuação:** O score final é tratado de forma defensiva para nunca assumir valores negativos (`max(score, 0.0)`).

## 4. Relatórios e Visualização Gráfica (`Analytics & PDF`)

* **Gráficos Dinâmicos em PySide6:** Renderização nativa de gráficos de barras via `matplotlib` em janelas dedicadas (`analytics_view.py`), consolidando os totais de consumo por categoria[cite: 2, 9].
* **Exportação Executiva em PDF:** O `PdfReportService` compila dados cadastrais, pontuação atual, gráficos temporários em imagem e tabelas detalhadas de registos num relatório profissional formatado com `fpdf2`[cite: 2, 9].

## 5. Guia de Conscientização (`TipsView`)

* Componente modular nativo em PySide6 (`QDialog`) contendo um guia interativo de boas práticas diárias de sustentabilidade, substituindo dependências externas e enriquecendo a experiência do utilizador.
