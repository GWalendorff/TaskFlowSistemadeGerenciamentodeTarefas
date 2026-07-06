"""
models.py — Modelo de dados do TaskFlow
TechFlow Solutions · Sistema de Gerenciamento de Tarefas

Baseado no Diagrama de Classes UML do projeto.
"""

from datetime import datetime
from enum import Enum
from typing import Optional


class PapelUsuario(Enum):
    """Papéis possíveis de um usuário no sistema."""
    MEMBRO_EQUIPE   = "Membro da Equipe"
    GESTOR_PROJETO  = "Gestor de Projetos"
    CLIENTE         = "Cliente"


class Prioridade(Enum):
    """
    Níveis de prioridade de uma tarefa.
    Conforme Diagrama de Classes — TechFlow TaskFlow.
    """
    ALTA   = "Alta"
    MEDIA  = "Média"
    BAIXA  = "Baixa"


class StatusTarefa(Enum):
    """
    Status possíveis de uma tarefa no Kanban.
    Conforme Diagrama de Classes — TechFlow TaskFlow.
    """
    A_FAZER      = "A Fazer"
    EM_PROGRESSO = "Em Progresso"
    CONCLUIDO    = "Concluído"


class Usuario:
    """
    Representa um usuário do sistema.
    Conforme Diagrama de Classes — classe USUÁRIO.

    Atributos:
        id (int):          Identificador único.
        nome (str):        Nome completo.
        email (str):       E-mail do usuário.
        senha_hash (str):  Senha armazenada como hash.
        papel (PapelUsuario): Papel no sistema.
    """

    def __init__(
        self,
        id: int,
        nome: str,
        email: str,
        senha_hash: str,
        papel: PapelUsuario = PapelUsuario.MEMBRO_EQUIPE,
    ):
        self.id         = id
        self.nome       = nome
        self.email      = email
        self.senha_hash = senha_hash
        self.papel      = papel


    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, nome='{self.nome}', papel={self.papel.value})"


class Tarefa:
    """
    Representa uma tarefa no sistema TaskFlow.
    Conforme Diagrama de Classes — classe TAREFA.

    Atributos:
        id (int):                Identificador único.
        titulo (str):            Título da tarefa.
        descricao (str):         Descrição detalhada.
        status (StatusTarefa):   Status no Kanban.
        prioridade (Prioridade): Nível de prioridade.
        responsavel (Usuario):   Usuário responsável.
        data_criacao (datetime): Data de criação.
        data_atualizacao (datetime): Data de atualização.
    """

    def __init__(
        self,
        id: int,
        titulo: str,
        descricao: str,
        prioridade: Prioridade,
        responsavel: Optional[Usuario] = None,
    ):
        self.id               = id
        self.titulo           = titulo
        self.descricao        = descricao
        self.status           = StatusTarefa.A_FAZER
        self.prioridade       = prioridade
        self.responsavel      = responsavel
        self.data_criacao     = datetime.now()
        self.data_atualizacao: Optional[datetime] = None

    def criar(self):
        """Inicializa a tarefa com status A Fazer."""
        self.status       = StatusTarefa.A_FAZER
        self.data_criacao = datetime.now()

    def atualizar(self, dados: dict):
        """
        Atualiza campos da tarefa a partir de um dicionário.

        Args:
            dados: Dicionário com campos a atualizar.
                   Chaves aceitas: titulo, descricao, prioridade, responsavel.
        """
        if "titulo" in dados and dados["titulo"]:
            self.titulo = dados["titulo"]
        if "descricao" in dados:
            self.descricao = dados["descricao"]
        if "prioridade" in dados:
            self.prioridade = dados["prioridade"]
        if "responsavel" in dados:
            self.responsavel = dados["responsavel"]
        self.data_atualizacao = datetime.now()

    def concluir(self):
        """Finaliza a tarefa marcando como Concluída."""
        self.status           = StatusTarefa.CONCLUIDO
        self.data_atualizacao = datetime.now()

    def mover(self, status: StatusTarefa):
        """Move a tarefa para outro status no Kanban."""
        self.status           = status
        self.data_atualizacao = datetime.now()

    def definir_prioridade(self, prioridade: Prioridade):
        """Define ou altera a prioridade da tarefa."""
        self.prioridade       = prioridade
        self.data_atualizacao = datetime.now()

    def validar(self) -> bool:
        """Valida se os campos obrigatórios estão preenchidos."""
        return bool(self.titulo and self.titulo.strip() and len(self.titulo.strip()) >= 3)

    def esta_critica(self) -> bool:
        """Retorna True se a prioridade for Alta."""
        return self.prioridade == Prioridade.ALTA

    def __repr__(self) -> str:
        return (
            f"Tarefa(id={self.id}, titulo='{self.titulo}', "
            f"prioridade={self.prioridade.value}, status={self.status.value})"
        )