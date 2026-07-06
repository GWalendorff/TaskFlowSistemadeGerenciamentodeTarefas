"""
conftest.py — Configurações compartilhadas dos testes
TechFlow Solutions · Sistema de Gerenciamento de Tarefas

Fixtures utilizadas pelos testes automatizados.
"""

import pytest

from src.task_manager import TaskManager
from src.kanban import QuadroKanban
from src.models import Usuario, PapelUsuario, Prioridade


@pytest.fixture
def manager():
    """Instância limpa do TaskManager para cada teste."""
    return TaskManager()


@pytest.fixture
def kanban():
    """Instância limpa do QuadroKanban para cada teste."""
    return QuadroKanban()


@pytest.fixture
def usuario():
    """Usuário padrão utilizado nos testes."""
    return Usuario(
        id=1,
        nome="Gabriel",
        email="gabriel@techflow.com",
        senha_hash="hash_teste",
        papel=PapelUsuario.MEMBRO_EQUIPE,
    )


@pytest.fixture
def usuario2():
    """Segundo usuário para testes de edição."""
    return Usuario(
        id=2,
        nome="Carlos",
        email="carlos@techflow.com",
        senha_hash="hash_teste",
        papel=PapelUsuario.MEMBRO_EQUIPE,
    )


@pytest.fixture
def tarefa_alta(manager, usuario):
    """Tarefa de prioridade Alta para reutilização."""
    return manager.criar_tarefa(
        titulo="Entregar relatório",
        descricao="Relatório mensal de entregas",
        prioridade=Prioridade.ALTA,
        responsavel=usuario,
    )


@pytest.fixture
def tarefa_media(manager):
    """Tarefa de prioridade Média para reutilização."""
    return manager.criar_tarefa(
        titulo="Revisar documentação",
        descricao="Revisar docs do sistema",
        prioridade=Prioridade.MEDIA,
    )


@pytest.fixture
def tarefa_baixa(manager):
    """Tarefa de prioridade Baixa para reutilização."""
    return manager.criar_tarefa(
        titulo="Organizar arquivos",
        descricao="Organizar pasta de documentos",
        prioridade=Prioridade.BAIXA,
    )