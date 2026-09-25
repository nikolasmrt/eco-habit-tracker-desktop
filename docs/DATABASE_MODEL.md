# 🗄️ Modelo de Dados e Esquema DDL - SQLite

A persistência do Eco-Vida utiliza o **SQLite 3**, garantindo portabilidade e robustez local sem necessidade de servidores externos.

## 📊 Diagrama Entidade-Relacionamento (ERD)

```mermaid
erDiagram
    USUARIOS ||--o{ REGISTROS : realiza
    HABITOS ||--o{ REGISTROS : possui
    
    USUARIOS {
        integer id PK
        text nome
        text email UK
        text senha
    }
    
    HABITOS {
        integer id PK
        text nome
        text unidade
        text categoria
    }
    
    REGISTROS {
        integer id PK
        integer usuario_id FK
        integer habito_id FK
        date data_registro
        real quantidade
    }