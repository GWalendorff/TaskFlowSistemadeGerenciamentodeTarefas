# TechFlow TaskFlow
### Sistema Web de Gerenciamento de Tarefas

**Empresa:** TechFlow Solutions (Fictícia)
**Cliente:** Startup do setor de logística

### Objetivo: 
- Desenvolver um sistema web de gerenciamento de tarefas para apoiar equipes de uma startup de logística na organização das atividades, priorização de tarefas críticas e acompanhamento do fluxo de trabalho utilizando práticas de Engenharia de Software e metodologias ágeis.

### Funcionalidades
- Cadastro de tarefas
- Atualização de tarefas
- Exclusão de tarefas
- Priorização (Alta, Média, Baixa)
- Organização em Kanban
- **Ordenação automática das tarefas por prioridade**
- **Destaque automático para tarefas críticas (⚠)**
- Testes automatizados
- Integração Contínua (GitHub Actions)

### Escopo Inicial:
- CRUD de Tarefas — criar, listar, atualizar e excluir tarefas
- Priorização — classificação por prioridade (Alta, Média, Baixa)
- Relatórios — exportação de tarefas em CSV
- Testes Automatizados — cobertura mínima de 80%
- Pipeline CI/CD — GitHub Actions para validação contínua

### Tecnologias:
- Python 3.11
- Pytest
- GitHub Actions
- Git

### Metodologia

- O projeto foi desenvolvido utilizando uma abordagem híbrida baseada em Scrum e Kanban.
- O controle do fluxo de trabalho foi realizado por meio do GitHub Projects, enquanto o versionamento foi realizado utilizando Git e GitHub.

### Diretórios:
    TaskFlowSistemadeGerenciamentodeTarefas/
    │
    │─ README.md                # Documento principal 
    │─ requirements.txt         # Dependências do projeto
    │
    │─ src/                 
    │   │─ __init_.py           # Pacote Python
    │   │─ models.py            # Classe Tarefa, Prioridade, Status
    │   │─ task_manager.py      # CRUD de tarefas
    │   │─ kanban.py            # Quadro Kanban
    │
    │─ teste/
    │   │─ _init__.py           # Pacote de testes
    │   │─ models.py            # Testes automatizados com Python
    │   
    │─ docs/
    │   │─ readme.md            # Documentação técnica
    │
    │─ .github/
    │   │─ workflows/
    │       │─ ci.yml           # Pipeline GitHub Actions
    │
    │
    │─ conftest.py              # Configuração do Pytest

### Execução:
- Pré-requisitos
    Python 3.11+
    pip

- Instalação:
    # 1. Clone o repositório
    git clone https://github.com/GWalendorff/TaskFlowSistemadeGerenciamentodeTarefas.git
    cd TaskFlowSistemadeGerenciamentodeTarefas

    # 2. Instale as dependências
    pip install -r requirements.txt

    # 3. Execute o sistema
    python src/task_manager.py

    # 4. Execute os testes
    pytest tests/ -v

### Executar Testes:
- pytest tests/ -v --cov=src --cov-report=term-missing

### Histórico de Mudanças

| Sprint | Solicitação | Implementação |
|--------|-------------|---------------|
| Sprint 3 | Destacar automaticamente tarefas críticas | Ordenação automática por prioridade e destaque visual (⚠) para tarefas de 
prioridade Alta no Quadro Kanban. |

### Mudança de Escopo:
Foram adicionadas novas funcionalidades ao módulo **QuadroKanban**, permitindo um melhor gerenciamento das tarefas prioritárias:

- Ordenação automática das tarefas por prioridade (Alta → Média → Baixa);
- Destaque visual (⚠) para tarefas críticas;
- Método `listar_criticas()` para consulta de tarefas urgentes;
- Organização automática das tarefas dentro de cada coluna do Kanban.

Essas alterações foram implementadas mantendo compatibilidade com o restante da arquitetura do projeto, sem impacto nas funcionalidades já existentes.

### Desenvolvedor:
- Gabriel Augusto Walendorff
- GitHub: @GWalendorff
- Curso: Análise e Desenvolvimento de Sistemas — UNIFECAF - 2026