# Controle de Estudos – Micro-API

Uma micro-API REST para gestão de controle de estudos, desenvolvida com FastAPI. Permite o gerenciamento de trilhas de estudo, cursos associados e atividades de estudo, com foco em rastreabilidade e organização do progresso acadêmico para estudantes de pós-graduação.

## Funcionalidades

- **CRUD de Trilhas**: Criar, listar, atualizar e remover trilhas de estudo.
- **CRUD de Cursos**: Gerenciar cursos vinculados a trilhas.
- **CRUD de Atividades**: Controlar atividades de estudo por curso, incluindo status de conclusão e revisão.
- **Sugestão de Prioridade**: Recomendação da próxima atividade usando heurística local ou IA (OpenAI GPT-4o-mini, opcional).
- **Healthcheck**: Endpoint para monitoramento de disponibilidade.
- **Documentação Interativa**: Swagger/OpenAPI em `/docs`.

## Arquitetura

A aplicação segue uma arquitetura em camadas para separação de responsabilidades:

```
Cliente → API (FastAPI) → Service → Repository → Banco de Dados
                    ↓
              PriorityAdvisor (Heurística/IA)
```

- **API**: Rotas e validação de entrada/saída com Pydantic.
- **Service**: Regras de negócio e coordenação.
- **Repository**: Acesso a dados (SQLite).
- **PriorityAdvisor**: Sugestão de atividades com fallback seguro.

### Diagrama de Fluxo

```mermaid
flowchart TD
    ClientIn["Usuário/Cliente"] --> API["API"]
    API --> Service["Service"]
    Service --> Repository["Repository"]
    Repository --> DB["Banco de Dados"]
    Service --> PriorityAdvisor["PriorityAdvisor"]
    PriorityAdvisor --> Service
    API --> ClientOut["Usuário/Cliente"]
```

## Instalação

### Pré-requisitos
- Python 3.11 ou superior
- Git

### Passos
1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd controle-estudos
   ```

2. **Crie e ative o ambiente virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

1. **Inicie o servidor**:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Acesse a aplicação**:
   - API: [http://localhost:8000](http://localhost:8000)
   - Documentação: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Healthcheck: [http://localhost:8000/health](http://localhost:8000/health)

## Testes

Execute os testes automatizados com pytest:

```bash
pytest
```

### Cobertura
- Testes unitários para serviços (`ControlService`, `PriorityAdvisor`).
- Testes de integração para rotas (usando `TestClient`).
- Cenários: CRUD, validações, erros (404, 400), fallback de IA.

Para executar testes específicos:
```bash
pytest tests/test_control_service.py
pytest tests/test_priority_advisor.py
pytest tests/test_control_routes.py
```

## Endpoints da API

### Trilhas
- `POST /api/v1/trilhas` - Criar trilha
- `GET /api/v1/trilhas` - Listar trilhas
- `GET /api/v1/trilhas/{id}` - Obter trilha por ID
- `PUT /api/v1/trilhas/{id}` - Atualizar trilha
- `DELETE /api/v1/trilhas/{id}` - Remover trilha

### Cursos
- `POST /api/v1/cursos` - Criar curso
- `GET /api/v1/cursos` - Listar cursos
- `GET /api/v1/cursos/{id}` - Obter curso por ID
- `PUT /api/v1/cursos/{id}` - Atualizar curso
- `DELETE /api/v1/cursos/{id}` - Remover curso

### Atividades
- `POST /api/v1/atividades` - Criar atividade
- `GET /api/v1/atividades` - Listar atividades
- `GET /api/v1/atividades/{id}` - Obter atividade por ID
- `PUT /api/v1/atividades/{id}` - Atualizar atividade
- `DELETE /api/v1/atividades/{id}` - Remover atividade

### Outros
- `GET /health` - Healthcheck

## Integração com IA

O `PriorityAdvisor` sugere a próxima atividade baseada em heurística local (priorizando atividades concluídas e revisadas). Opcionalmente, integra com OpenAI GPT-4o-mini para recomendações inteligentes.

### Configuração
- Defina a variável de ambiente `OPENAI_API_KEY` para habilitar IA.
- Sem chave: usa apenas heurística local (sem custo).
- Com chave: tenta IA com timeout de 3s; falha segura para heurística.

### Exemplo de Uso
```python
from app.services.priority_advisor import PriorityAdvisor

advisor = PriorityAdvisor()
sugestao = advisor.suggest_proxima_atividade(atividades, use_llm=True)
```

## Limitações

- **Banco de Dados**: SQLite (MVP); não escalável para produção.
- **Autenticação**: Não implementada (planejada para Release 2).
- **Usuários**: Gestão de estudantes não incluída no MVP.
- **IA**: Dependente de chave OpenAI; sem chave, funcionalidade limitada.
- **Desempenho**: Não otimizado para alta carga.
- **Segurança**: Sem validações avançadas ou rate limiting.

## Próximos Passos

### Release 2: Qualidade
- [ ] Estrutura modular aprimorada (DRY/SRP).
- [ ] Testes automatizados completos.
- [ ] Logs estruturados e tratamento de erros.
- [ ] Autenticação básica.

### Release 3: Entrega Final
- [ ] Migração para PostgreSQL.
- [ ] Deploy em cloud (ex: Railway, Render).
- [ ] Interface web simples (opcional).
- [ ] Monitoramento avançado.

### Melhorias Futuras
- Suporte a múltiplos usuários.
- Notificações e lembretes.
- Análise de progresso com gráficos.
- Integração com plataformas de e-learning.

## Contribuição

1. Fork o projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`).
4. Push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

Siga Conventional Commits e mantenha testes atualizados.

## Licença

Este projeto é licenciado sob a MIT License. Veja o arquivo `LICENSE` para detalhes.