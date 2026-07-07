"""
kanban.py — Quadro Kanban do TaskFlow
TechFlow Solutions · Sistema de Gerenciamento de Tarefas

Baseado no Diagrama de Classes UML do projeto.

Mudança de Escopo implementada:
    • Ordenação automática das tarefas por prioridade.
    • Destaque visual para tarefas críticas (Prioridade Alta).
    • Método listar_criticas() para identificação de tarefas urgentes.

Classes:
    • QuadroKanban
    • Coluna
"""

from typing import List, Dict
from src.models import Tarefa, StatusTarefa, Prioridade

class Coluna:
    """
    Representa uma coluna do quadro Kanban.
    """

    def __init__(self, id: int, nome: str, ordem: int):
        self.id = id
        self.nome = nome
        self.ordem = ordem
        self.tarefas = []

    def adicionar_tarefa(self, tarefa):
        if tarefa not in self.tarefas:
            self.tarefas.append(tarefa)

    def remover_tarefa(self, tarefa):
        if tarefa in self.tarefas:
            self.tarefas.remove(tarefa)

    def mover_tarefa(self, tarefa, destino):
        self.remover_tarefa(tarefa)
        destino.adicionar_tarefa(tarefa)

    def total(self):
        return len(self.tarefas)


class QuadroKanban:
    """
    Representa o quadro Kanban com três colunas.

    Colunas:
        A Fazer      → tarefas ainda não iniciadas
        Em Progresso → tarefas em andamento
        Concluído    → tarefas finalizadas

    Funcionalidade adicionada (Mudança de Escopo):
        - Organização automática das tarefas por prioridade
        - Destaque visual para tarefas críticas (prioridade Alta)
        - Consulta de tarefas críticas
    """

    COLUNAS = [
        StatusTarefa.A_FAZER,
        StatusTarefa.EM_PROGRESSO,
        StatusTarefa.CONCLUIDO,
    ]

    def __init__(self):
        self._colunas: Dict[StatusTarefa, List[Tarefa]] = {
            StatusTarefa.A_FAZER:       [],
            StatusTarefa.EM_PROGRESSO:  [],
            StatusTarefa.CONCLUIDO:     [],
        }

    # ── Operações ─────────────────────────────────────────────────────────────

    def adicionar_tarefa(self, tarefa: Tarefa):
        """Adiciona tarefa na coluna do status atual."""
        coluna = self._colunas.get(tarefa.status)
        if coluna is not None and tarefa not in coluna:
            coluna.append(tarefa)
            self._ordenar_coluna(tarefa.status)

    def mover_tarefa(self, tarefa: Tarefa, novo_status: StatusTarefa):
        """Move uma tarefa de uma coluna para outra."""
        for coluna in self._colunas.values():
            if tarefa in coluna:
                coluna.remove(tarefa)
                break

        tarefa.mover(novo_status)
        self._colunas[novo_status].append(tarefa)
        self._ordenar_coluna(novo_status)

    def listar_colunas(self) -> Dict[str, List[Tarefa]]:
        """Retorna todas as colunas com suas tarefas."""
        return {
            status.value: tarefas
            for status, tarefas in self._colunas.items()
        }

    def listar_coluna(self, status: StatusTarefa) -> List[Tarefa]:
        """Retorna as tarefas de uma coluna específica."""
        return self._colunas.get(status, [])

    # ── Mudança de Escopo: destaque de tarefas críticas ───────────────────────

    def listar_criticas(self) -> List[Tarefa]:
        """
        Retorna todas as tarefas críticas (prioridade Alta) do quadro.

        Returns:
            Lista de tarefas com prioridade Alta em qualquer coluna.
        """
        criticas = []
        for tarefas in self._colunas.values():
            for t in tarefas:
                if t.esta_critica():        # Destaca visualmente tarefas críticas (Prioridade Alta)
                    criticas.append(t)
        return criticas

    def _ordenar_coluna(self, status: StatusTarefa):
        """
        Ordena automaticamente uma coluna por prioridade.
        Alta → Média → Baixa (tarefas críticas sempre primeiro).
        """
        ordem = {Prioridade.ALTA: 0, Prioridade.MEDIA: 1, Prioridade.BAIXA: 2}
        self._colunas[status].sort(key=lambda t: ordem[t.prioridade])

    def total_por_coluna(self) -> Dict[str, int]:
        """Retorna a quantidade de tarefas em cada coluna."""
        return {
            status.value: len(tarefas)
            for status, tarefas in self._colunas.items()
        }

    def exibir(self):
        """Exibe o quadro Kanban formatado com destaque para críticas."""
        print("\n" + "=" * 55)
        print("  QUADRO KANBAN — TaskFlow · TechFlow Solutions")
        print("=" * 55)

        for status, tarefas in self._colunas.items():
            print(f"\n  [{status.value.upper()}] ({len(tarefas)} tarefa(s))")
            print("  " + "-" * 40)
            if not tarefas:
                print("  (vazio)")
            for t in tarefas:
                # Destaque para tarefas críticas
                if t.esta_critica():
                    print(f"  ⚠  [{t.id}] {t.titulo} | {t.prioridade.value} ← CRÍTICA")
                else:
                    print(f"  •  [{t.id}] {t.titulo} | {t.prioridade.value}")

        # Resumo de críticas
        criticas = self.listar_criticas()
        if criticas:
            print(f"\n  ⚠  {len(criticas)} tarefa(s) crítica(s) requerem atenção!")

        print("=" * 55)