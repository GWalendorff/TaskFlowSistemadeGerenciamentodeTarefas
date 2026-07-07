"""
models.py — Modelo de Dados do TaskFlow
TechFlow Solutions · Sistema de Gerenciamento de Tarefas

Contém as entidades principais do sistema conforme o Diagrama de Classes UML.

Melhorias desta versão:
    • Docstrings padronizadas
    • Tipagem completa
    • Organização dos imports
    • Classe Usuario integrada ao gerenciamento de tarefas
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


# ─────────────────────────────────────────────────────────────────────────────
# ENUMS
# ─────────────────────────────────────────────────────────────────────────────

class Prioridade(Enum):
    """Níveis de prioridade de uma tarefa."""

    ALTA = "Alta"
    MEDIA = "Média"
    BAIXA = "Baixa"


class StatusTarefa(Enum):
    """Status possíveis de uma tarefa no fluxo Kanban."""

    A_FAZER = "A Fazer"
    EM_PROGRESSO = "Em Progresso"
    CONCLUIDO = "Concluído"


class PapelUsuario(Enum):
    """Papéis disponíveis para usuários do sistema."""

    ADMIN = "Administrador"
    GERENTE = "Gerente"
    MEMBRO_EQUIPE = "Membro da Equipe"


# ─────────────────────────────────────────────────────────────────────────────
# USUÁRIO
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Usuario:
    """
    Representa um usuário do sistema.

    Attributes:
        id: Identificador único.
        nome: Nome completo.
        email: E-mail.
        senha_hash: Senha criptografada.
        papel: Papel do usuário.
    """

    id: int
    nome: str
    email: str
    senha_hash: str
    papel: PapelUsuario

    def __repr__(self) -> str:
        return (
            f"Usuario(id={self.id}, "
            f"nome='{self.nome}', "
            f"papel='{self.papel.value}')"
        )


# ─────────────────────────────────────────────────────────────────────────────
# TAREFA
# ─────────────────────────────────────────────────────────────────────────────

class Tarefa:
    """
    Representa uma tarefa do sistema TaskFlow.

    Attributes:
        id:
            Identificador único.

        titulo:
            Nome da tarefa.

        descricao:
            Descrição detalhada.

        prioridade:
            Prioridade da tarefa.

        status:
            Status atual no quadro Kanban.

        responsavel:
            Usuário responsável pela tarefa.

        data_criacao:
            Data de criação.

        data_atualizacao:
            Última atualização.
    """

    def __init__(
        self,
        id: int,
        titulo: str,
        descricao: str,
        prioridade: Prioridade,
        responsavel: Optional[Usuario] = None,
    ):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.prioridade = prioridade
        self.status = StatusTarefa.A_FAZER
        self.responsavel = responsavel

        self.data_criacao = datetime.now()
        self.data_atualizacao: Optional[datetime] = None

    # ───────────────────────────────────────────────────────────────────

    def criar(self) -> None:
        """Inicializa a tarefa."""

        self.status = StatusTarefa.A_FAZER
        self.data_criacao = datetime.now()

    # ───────────────────────────────────────────────────────────────────

    def atualizar(self, dados: dict) -> None:
        """
        Atualiza os campos informados.

        Args:
            dados: Dicionário contendo os atributos a atualizar.
        """

        for atributo, valor in dados.items():
            setattr(self, atributo, valor)

        self.data_atualizacao = datetime.now()

    # ───────────────────────────────────────────────────────────────────

    def mover(self, novo_status: StatusTarefa) -> None:
        """Move a tarefa para outro status."""

        self.status = novo_status
        self.data_atualizacao = datetime.now()

    # ───────────────────────────────────────────────────────────────────

    def concluir(self) -> None:
        """Conclui a tarefa."""

        self.status = StatusTarefa.CONCLUIDO
        self.data_atualizacao = datetime.now()

    # ───────────────────────────────────────────────────────────────────

    def definir_prioridade(self, prioridade: Prioridade) -> None:
        """Altera a prioridade da tarefa."""

        self.prioridade = prioridade
        self.data_atualizacao = datetime.now()

    # ───────────────────────────────────────────────────────────────────

    def esta_critica(self) -> bool:
        """
        Retorna True caso a tarefa seja de prioridade Alta.
        """

        return self.prioridade == Prioridade.ALTA

    # ───────────────────────────────────────────────────────────────────

    def validar(self) -> bool:
        """
        Valida os dados básicos da tarefa.

        Returns:
            True quando a tarefa é válida.
        """

        if not self.titulo.strip():
            return False

        if len(self.titulo.strip()) < 3:
            return False

        return True

    # ───────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return (
            f"Tarefa("
            f"id={self.id}, "
            f"titulo='{self.titulo}', "
            f"prioridade='{self.prioridade.value}', "
            f"status='{self.status.value}')"
        )