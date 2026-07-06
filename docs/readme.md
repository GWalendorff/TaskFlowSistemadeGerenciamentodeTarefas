# Documentação Técnica — TaskFlow

### TechFlow Solutions · Sistema de Gerenciamento de Tarefas

### Arquitetura do Sistema
**O sistema segue uma arquitetura simples em camadas:**

<────────────────────────────────────────>
│         **Interface (Terminal)**       │
├────────────────────────────────────────┤
│      **TaskManager - QuadroKanban**    │  ← Lógica de negócio
├────────────────────────────────────────┤
│         **Modelos (Tarefa)**           │  ← Dados
<────────────────────────────────────────>


### Estrutura do Projeto

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


### Modelo de dados

**Atribuitos**          **Tipo**          **Descrição**
-  id                     int          Identificador único           
-  titulo                 str          Título da tarefa
-  descricao              str          Descrição detalhada
-  prioridade          prioridade      Alta, Média ou Baixa
-  status                status        A Fazer, Em Progresso, Concluído
-  responsavel            str          Nome do responsável
-  criado_em            datetime       Data da criação
-  atualizado_em        datetime       Data da última atualização


### Enum Prioridade
- BAIXA = "Baixa"
- MEDIA = "Média"
- ALTA  = "Alta"


### Enum Status
- A_FAZER       = "A Fazer"
- EM_PROGRESSO  = "Em Progresso"
- CONCLUIDO     = "Concluído"


### Pré-requisitos
- 1. Clone o repositório
git clone https://github.com/GWalendorff/TaskFlowSistemadeGerenciamentodeTarefas.git
cd TaskFlowSistemadeGerenciamentodeTarefas

- 2. Instale as dependências
pip install -r requirements.txt


### Como Testar
- Rodar todos os testes
pytest tests/ -v

- Rodar com relatório de cobertura
pytest tests/ -v --cov=src --cov-report=term-missing

- Rodar um teste específico
pytest tests/test_task_manager.py::TestCriarTarefa -v


### Resultado esperado
tests/test_task_manager.py::TestCriarTarefa::test_criar_tarefa_basica    PASSED
tests/test_task_manager.py::TestCriarTarefa::test_status_inicial_a_fazer PASSED
tests/test_task_manager.py::TestListarTarefas::test_listar_todas         PASSED
...
========== XX passed in 0.XXs ==========


### Organização das Classes

TaskManager
│─ criar_tarefa()
│─ listar_tarefas()
│─ editar_tarefa()
│─ mover_status()
│─ excluir_tarefa()

QuadroKanban
│─ adicionar_tarefa()
│─ mover_tarefa()
│─ listar_colunas()
│─ listar_coluna()

Tarefa
│─ criar()
│─ atualizar()
│─ mover()
│─ excluir()
│─ esta_critica()


### Dependências
- pytest==8.2.0
- pytest-cov==5.0.0


### Pipeline

**O arquivo .github/workflows/ci.yml configura o pipeline que:**

- 1. Executa em todo push para o branch main
- 2. Instala as dependências automaticamente
- 3. Roda todos os testes com pytest
- 4. Exibe relatório de cobertura de código