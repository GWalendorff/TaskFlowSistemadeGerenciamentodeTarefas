"""
task_manager.py — CRUD de Tarefas do TaskFlow
TechFlow Solutions · Sistema de Gerenciamento de Tarefas

Baseado no Diagrama de Classes UML do projeto.
"""

from typing import List, Optional
from src.models import Tarefa, Prioridade, StatusTarefa, Usuario


class TaskError(Exception):
    """Exceção para erros no gerenciamento de tarefas."""
    pass


class TaskManager:
    """
    Gerencia o ciclo de vida completo das tarefas em memória.

    Operações:
        criar_tarefa()     → Create
        listar_tarefas()   → Read
        editar_tarefa()    → Update
        excluir_tarefa()   → Delete
    """

    def __init__(self):
        self._tarefas: List[Tarefa] = []
        self._proximo_id: int = 1

    # ── CREATE ────────────────────────────────────────────────────────────────

    def criar_tarefa(
        self,
        titulo: str,
        descricao: str,
        prioridade: Prioridade,
        responsavel: Optional[Usuario] = None,
    ) -> Tarefa:
        """
        Cria e armazena uma nova tarefa.

        Args:
            titulo:      Título obrigatório (mínimo 3 caracteres).
            descricao:   Descrição da tarefa.
            prioridade:  Nível de prioridade.
            responsavel: Usuario do responsável pela tarefa(opcional).

        Returns:
            Objeto Tarefa criado.

        Raises:
            TaskError: Se o título for inválido.
        """
        if not titulo or not titulo.strip():
            raise TaskError("Título não pode ser vazio.")
        if len(titulo.strip()) < 3:
            raise TaskError("Título deve ter no mínimo 3 caracteres.")

        tarefa = Tarefa(
            id=self._proximo_id,
            titulo=titulo.strip(),
            descricao=descricao.strip(),
            prioridade=prioridade,
            responsavel=responsavel,
        )
        tarefa.criar()
        self._tarefas.append(tarefa)
        self._proximo_id += 1
        return tarefa

    # ── READ ─────────────────────────────────────────────────────────────────

    def listar_tarefas(
        self,
        status: Optional[StatusTarefa] = None,
        prioridade: Optional[Prioridade] = None,
    ) -> List[Tarefa]:
        """
        Lista tarefas com filtros opcionais.

        Args:
            status:     Filtra pelo status da tarefa.
            prioridade: Filtra pelo nível de prioridade.

        Returns:
            Lista de tarefas filtrada.
        """
        resultado = list(self._tarefas)

        if status:
            resultado = [t for t in resultado if t.status == status]
        if prioridade:
            resultado = [t for t in resultado if t.prioridade == prioridade]

        return resultado

    def buscar_por_id(self, tarefa_id: int) -> Tarefa:
        """
        Busca uma tarefa pelo ID.

        Raises:
            TaskError: Se não encontrada.
        """
        for t in self._tarefas:
            if t.id == tarefa_id:
                return t
        raise TaskError(f"Tarefa com ID {tarefa_id} não encontrada.")

    def listar_criticas(self) -> List[Tarefa]:
        """Retorna apenas tarefas de prioridade Alta."""
        return [t for t in self._tarefas if t.esta_critica()]

    # ── UPDATE ────────────────────────────────────────────────────────────────

    def editar_tarefa(
        self,
        tarefa_id: int,
        titulo: Optional[str] = None,
        descricao: Optional[str] = None,
        prioridade: Optional[Prioridade] = None,
        responsavel: Optional[Usuario] = None,
    ) -> Tarefa:
        """
        Edita campos de uma tarefa existente.

        Raises:
            TaskError: Se não encontrada ou título inválido.
        """
        tarefa = self.buscar_por_id(tarefa_id)

        if titulo is not None and not titulo.strip():
            raise TaskError("Título não pode ser vazio.")

        dados = {}
        if titulo:      dados["titulo"]      = titulo.strip()
        if descricao:   dados["descricao"]   = descricao
        if prioridade:  dados["prioridade"]  = prioridade
        if responsavel: dados["responsavel"] = responsavel

        tarefa.atualizar(dados)
        return tarefa

    def mover_status(self, tarefa_id: int, novo_status: StatusTarefa) -> Tarefa:
        """Move uma tarefa para outro status no Kanban."""
        tarefa = self.buscar_por_id(tarefa_id)
        tarefa.mover(novo_status)
        return tarefa

    # ── DELETE ────────────────────────────────────────────────────────────────

    def excluir_tarefa(self, tarefa_id: int) -> bool:
        """
        Remove uma tarefa da lista.

        Returns:
            True se removida com sucesso.

        Raises:
            TaskError: Se não encontrada.
        """
        tarefa = self.buscar_por_id(tarefa_id)
        self._tarefas.remove(tarefa)
        return True

    # ── MÉTRICAS ──────────────────────────────────────────────────────────────

    def total_tarefas(self) -> int:
        """Retorna o total de tarefas cadastradas."""
        return len(self._tarefas)

    def total_por_status(self) -> dict:
        """Retorna contagem agrupada por status."""
        contagem = {s.value: 0 for s in StatusTarefa}
        for t in self._tarefas:
            contagem[t.status.value] += 1
        return contagem