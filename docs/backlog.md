# Backlog Mínimo por Releases

## Release 1: Core

- [ ] **RT-01: CRUD de Trilhas**
  - Critérios de aceite:
    - [ ] Permitir criar, listar, atualizar e remover trilhas
    - [ ] Validação de campos obrigatórios
    - [ ] Retorno de códigos HTTP adequados (201, 200, 204, 404)

- [ ] **RT-02: CRUD de Cursos**
  - Critérios de aceite:
    - [ ] Permitir criar, listar, atualizar e remover cursos vinculados a uma trilha
    - [ ] Validação de vínculo obrigatório com trilha
    - [ ] Retorno de códigos HTTP adequados

- [ ] **RT-03: CRUD de Atividades de Estudo**
  - Critérios de aceite:
    - [ ] Permitir criar, listar, atualizar e remover atividades vinculadas a um curso
    - [ ] Campos obrigatórios: descricao_atividade, estudo_concluido, revisao_finalizada
    - [ ] Retorno de códigos HTTP adequados

- [ ] **RT-04: Endpoint Healthcheck**
  - Critérios de aceite:
    - [ ] GET /health retorna status ok e timestamp
    - [ ] Documentação automática disponível

## Release 2: Qualidade

- [ ] **RT-05: Estrutura Modular (routers, schemas, services)**
  - Critérios de aceite:
    - [ ] Separação clara de responsabilidades no código
    - [ ] Facilidade de manutenção e extensão

- [ ] **RT-06: Testes Automatizados (pytest)**
  - Critérios de aceite:
    - [ ] Testes cobrindo operações CRUD e healthcheck
    - [ ] Validação de payloads e respostas
    - [ ] Execução local dos testes

- [ ] **RT-07: Logs Estruturados e Tratamento de Erros**
  - Critérios de aceite:
    - [ ] Registro de logs mínimos para operações e erros
    - [ ] Contexto suficiente para troubleshooting

## Release 3: Entrega Final

- [ ] **RT-08: Documentação Interativa (/docs)**
  - Critérios de aceite:
    - [ ] Swagger/OpenAPI disponível e atualizado
    - [ ] Exemplos de payloads e descrições claras

- [ ] **RT-09: Requisitos de Execução Local (.venv)**
  - Critérios de aceite:
    - [ ] Projeto executável em ambiente virtual Python (.venv)
    - [ ] Instruções claras no README

- [ ] **RT-10: Entrega e Checklist Final**
  - Critérios de aceite:
    - [ ] Todos os itens anteriores implementados e validados
    - [ ] Projeto versionado no Git
    - [ ] Backlog revisado e encerrado
