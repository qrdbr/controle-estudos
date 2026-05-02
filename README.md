# Controle de Estudos – Micro-API

## Objetivo
MVP de uma micro-API para gestão de controle de estudos, incluindo trilhas, cursos das trilhas e atividades de estudo de cada curso. O objetivo é facilitar o acompanhamento e organização do progresso dos estudos.

## Stack Tecnológica
- **Linguagem:** Python 3.11+
- **Framework:** FastAPI
- **Gerenciador de dependências:** pip / venv
- **Banco de dados:** SQLite
- **Testes:** pytest
- **Outros:** Uvicorn (servidor ASGI), Pydantic

## Como rodar localmente
1. **Clone o repositório:**
   ```sh
   git clone <url-do-repositorio>
   cd controle-estudos
   ```
2. **Crie o ambiente virtual:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate    # Windows
   ```
3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Execute a aplicação:**
   ```sh
   uvicorn main:app --reload
   ```
5. **Acesse a documentação interativa:**
   - [http://localhost:8000/docs](http://localhost:8000/docs)

## Roadmap de Releases
- MVP: CRUD de trilhas, cursos e atividades
- Autenticação básica de usuários
- Integração com banco de dados relacional
- Testes automatizados
- Deploy em ambiente cloud

---

Contribuições são bem-vindas!