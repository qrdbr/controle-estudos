```mermaid
flowchart TD
    Client["Usuário/Cliente"] -->|HTTP Request| API["API"]
    API -->|Chama| Service["Service"]
    Service -->|Consulta/Grava| Repository["Repository"]
    Repository -->|Acessa| DB["Banco de Dados"]
    Service -->|Consulta/Usa| PriorityAdvisor["PriorityAdvisor"]
    PriorityAdvisor --|Sugestão/Prioridade| Service
    API -->|HTTP Response| Client
```
