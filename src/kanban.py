"""
kanban.py — Quadro Kanban do TaskFlow
TechFlow Solutions · Sistema de Gerenciamento de Tarefas

Baseado no Diagrama de Classes UML do projeto.
Classes: QuadroKanban, Coluna
"""

from typing import List, Dict
from src.models import Tarefa, StatusTarefa, Prioridade
from datetime import datetime

class Coluna:
    """
    Representa uma coluna do quadro Kanban.
    Conforme Diagrama de Classes — classe Coluna.

    Atributos:
        id (int):     Identificador da coluna.
        nome (str):   Nome da coluna.
        ordem (int):  Posição da coluna no quadro.
    """

    def __init__(self, id: int, nome: str, ordem: int):
        self.id     = id
        self.nome   = nome
        self.ordem  = ordem
        self._tarefas: List[Tarefa] = []

    def adicionar_tarefa(self, tarefa: Tarefa):
        """Adiciona uma tarefa na coluna."""
        if tarefa not in self._tarefas:
            self._tarefas.append(tarefa)
            self._ordenar()

    def remover_tarefa(self, tarefa: Tarefa):
        """Remove uma tarefa da coluna."""
        if tarefa in self._tarefas:
            self._tarefas.remove(tarefa)

    def mover_tarefa(self, tarefa: Tarefa, destino: "Coluna"):
        """Move uma tarefa desta coluna para outra."""
        self.remover_tarefa(tarefa)
        destino.adicionar_tarefa(tarefa)

    def listar_tarefas(self) -> List[Tarefa]:
        """Retorna todas as tarefas da coluna."""
        return list(self._tarefas)

    def _ordenar(self):
        """Ordena tarefas por prioridade: Alta → Média → Baixa."""
        ordem = {Prioridade.ALTA: 0, Prioridade.MEDIA: 1, Prioridade.BAIXA: 2}
        self._tarefas.sort(key=lambda t: ordem[t.prioridade])

    def total(self) -> int:
        """Retorna a quantidade de tarefas na coluna."""
        return len(self._tarefas)

    def __repr__(self) -> str:
        return f"Coluna(nome='{self.nome}', tarefas={self.total()})"


class QuadroKanban:
    """
    Representa o quadro Kanban completo com três colunas.
    Conforme Diagrama de Classes — classe QuadroKanban.

    Colunas:
        A Fazer      → tarefas não iniciadas
        Em Progresso → tarefas em andamento
        Concluído    → tarefas finalizadas
    """

    def __init__(self, id: int = 1, nome: str = "TaskFlow Board",
                 descricao: str = "Quadro principal do projeto"):
        self.id        = id
        self.nome      = nome
        self.descricao = descricao
        self.data_criacao = datetime.now()

        # Criação das colunas conforme o fluxo Kanban
        self._colunas: Dict[StatusTarefa, Coluna] = {
            StatusTarefa.A_FAZER:      Coluna(1, "A Fazer",      1),
            StatusTarefa.EM_PROGRESSO: Coluna(2, "Em Progresso", 2),
            StatusTarefa.CONCLUIDO:    Coluna(3, "Concluído",    3),
        }


    def listar_colunas(self) -> Dict[str, List[Tarefa]]:
        """
        Retorna todas as colunas com suas tarefas.

        Returns:
            Dicionário nome_coluna → lista de tarefas.
        """
        return {
            col.nome: col.listar_tarefas()
            for col in self._colunas.values()
        }

    def adicionar_tarefa(self, tarefa: Tarefa):
        """Adiciona tarefa na coluna do seu status atual."""
        coluna = self._colunas.get(tarefa.status)
        if coluna:
            coluna.adicionar_tarefa(tarefa)

    def mover_tarefa(self, tarefa: Tarefa, novo_status: StatusTarefa):
        """Move tarefa de uma coluna para outra e atualiza o status."""
        # Remove a tarefa da coluna atual antes de movê-la
        for coluna in self._colunas.values():
            coluna.remover_tarefa(tarefa)

        # Atualiza status e adiciona na nova coluna
        tarefa.mover(novo_status)
        self._colunas[novo_status].adicionar_tarefa(tarefa)

    def listar_criticas(self) -> List[Tarefa]:
        """Retorna todas as tarefas críticas (Alta prioridade) do quadro."""
        criticas = []
        for coluna in self._colunas.values():
            for t in coluna.listar_tarefas():
                if t.esta_critica():
                    criticas.append(t)
        return criticas

    def listar_coluna(self, status: StatusTarefa) -> List[Tarefa]:
        """Retorna as tarefas de uma coluna específica."""
        coluna = self._colunas.get(status)
        return coluna.listar_tarefas() if coluna else []

    def total_por_coluna(self) -> Dict[str, int]:
        """Retorna a quantidade de tarefas em cada coluna."""
        return {col.nome: col.total() for col in self._colunas.values()}

    def exibir(self):
        """Exibe o quadro formatado no terminal com destaque para críticas."""
        print("\n" + "=" * 55)
        print(f"  {self.nome} — TechFlow Solutions")
        print("=" * 55)

        for coluna in self._colunas.values():
            tarefas = coluna.listar_tarefas()
            print(f"\n  [{coluna.nome.upper()}] ({coluna.total()} tarefa(s))")
            print("  " + "-" * 40)
            if not tarefas:
                print("  (vazio)")
            for t in tarefas:
                if t.esta_critica():
                    print(f"  ⚠  [{t.id}] {t.titulo} | {t.prioridade.value} ← CRÍTICA")
                else:
                    print(f"  •  [{t.id}] {t.titulo} | {t.prioridade.value}")

        criticas = self.listar_criticas()
        if criticas:
            print(f"\n  ⚠  {len(criticas)} tarefa(s) crítica(s) requerem atenção!")
        print("=" * 55)