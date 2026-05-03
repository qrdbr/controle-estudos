```mermaid
flowchart TD
    Client[Usuário/Cliente] -->|HTTP Request| API[API (FastAPI Routers)]
    API -->|Chama| Service[Service Layer]
    Service -->|Consulta/Grava| Repository[Repository Layer]
    Repository -->|Acessa| DB[(Banco de Dados SQLite)]
    Service -->|Consulta/Usa| PriorityAdvisor[PriorityAdvisor Component]
    PriorityAdvisor --|Sugestão/Prioridade| Service
    API -->|HTTP Response| Client
```
