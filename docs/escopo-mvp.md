# Escopo do MVP: Micro-API para Gestão de Controle de Estudos

## 1. Contexto

Desenvolvimento de uma micro-API para gestão de controle de estudos, contemplando trilhas, cursos de cada trilha e atividades de estudo dos cursos, voltada para estudantes de cursos de pós-graduação.

## 2. Objetivo

Fornecer uma solução backend enxuta, escalável e de fácil integração, permitindo o gerenciamento eficiente de trilhas de estudo, cursos e atividades, com foco em rastreabilidade, simplicidade e automação de validações.

## 3. Escopo Funcional

### 3.1. Modelo de Dados (Tabelas)

#### Tabela: trilha
| Campo            | Tipo     | Obrigatório | Descrição                |
|------------------|----------|-------------|--------------------------|
| id_trilha        | INTEGER  | Sim         | Identificador da trilha  |
| descricao_trilha | TEXT     | Sim         | Descrição da trilha      |

#### Tabela: curso
| Campo           | Tipo     | Obrigatório | Descrição                        |
|-----------------|----------|-------------|----------------------------------|
| id_curso        | INTEGER  | Sim         | Identificador do curso           |
| id_trilha       | INTEGER  | Sim         | FK para trilha                   |
| descricao_curso | TEXT     | Sim         | Descrição do curso               |

#### Tabela: atividades_estudo
| Campo              | Tipo     | Obrigatório | Descrição                                 |
|--------------------|----------|-------------|-------------------------------------------|
| id_atividade       | INTEGER  | Sim         | Identificador da atividade                |
| id_curso           | INTEGER  | Sim         | FK para curso                            |
| descricao_atividade| TEXT     | Sim         | Descrição da atividade                    |
| estudo_concluido   | INTEGER  | Sim         | Status de conclusão (0=pendente, 1=ok)    |
| revisao_finalizada | INTEGER  | Sim         | Status de revisão (0=pendente, 1=ok)      |

### 3.2. Trilhas de Estudo
- CRUD de trilhas de estudo
- Associação de cursos a uma trilha
- Listagem de trilhas e seus cursos

### 3.3. Cursos
- CRUD de cursos
- Associação de atividades a um curso
- Listagem de cursos e suas atividades

### 3.4. Atividades de Estudo
- CRUD de atividades
- Registro de status de conclusão e revisão conforme campos obrigatórios

### 3.5. Usuários (Estudantes)
- Cadastro e autenticação simplificada (MVP: sem OAuth, apenas usuário/senha)
- Associação de trilhas/cursos/atividades ao estudante
- Consulta do progresso individual

### 3.6. Healthcheck e Observabilidade
- Endpoint de healthcheck (/health)
- Documentação automática via Swagger/OpenAPI

### 3.7. Contrato HTTP
- Retorno de códigos de resposta HTTP compatíveis (200, 201, 204, 400, 404, 500, etc.) conforme operação executada

### 3.4. Usuários (Estudantes)
- Cadastro e autenticação simplificada (MVP: sem OAuth, apenas usuário/senha)
- Associação de trilhas/cursos/atividades ao estudante
- Consulta do progresso individual

### 3.5. Healthcheck e Observabilidade
- Endpoint de healthcheck (/health)
- Documentação automática via Swagger/OpenAPI

## 4. Requisitos Não Funcionais

### 4.1. Tecnologia e Compatibilidade
- Implementação em Python 3.11+ com FastAPI
- Execução local em ambiente virtual isolado (.venv)
- Banco de dados SQLite (MVP)
- Compatível com sistemas operacionais Windows, Linux e MacOS

### 4.2. Qualidade e Organização do Código
- Estrutura modular mínima: separação em routers, schemas e services
- Tipagem forte e validação automática de dados com Pydantic
- Código limpo, legível e documentado
- Controle de versionamento via Git

### 4.3. Testabilidade
- Testes automatizados utilizando pytest
- Cobertura mínima: validação de payloads, operações CRUD básicas e endpoint de healthcheck
- Facilidade para execução dos testes em ambiente local

### 4.4. Observabilidade
- Logs estruturados mínimos para operações relevantes
- Registro de erros com contexto suficiente para troubleshooting (ex: endpoint, payload, mensagem de erro)
- Healthcheck acessível para monitoramento básico

### 4.5. Documentação
- Documentação interativa automática disponível em /docs (Swagger/OpenAPI)
- Descrição clara dos endpoints, parâmetros e exemplos de payloads

### 4.6. Desempenho e Disponibilidade
- Uso interno, sem requisitos de alta disponibilidade
- Foco em desempenho suficiente para uso local e testes de integração

## 5. Fora do Escopo

- Interface gráfica (frontend)
- Integração com sistemas externos (ex: SSO, OAuth, ERPs)
- Notificações (email, push, etc.)
- Relatórios avançados ou exportação de dados
- Funcionalidades administrativas avançadas (ex: RBAC, logs detalhados)
- Suporte a múltiplos bancos de dados (apenas SQLite no MVP)
- Deploy em ambiente de produção (foco em ambiente local/dev)

## 6. Considerações Finais

O MVP visa validar o modelo de dados e a arquitetura da solução, priorizando simplicidade, clareza e facilidade de evolução. Funcionalidades adicionais e integrações externas poderão ser consideradas em versões futuras, conforme feedback dos usuários e necessidades do projeto.
