"""
test_task_manager.py — Testes automatizados do TaskFlow
TechFlow Solutions · Sistema de Gerenciamento de Tarefas
Executar: pytest tests/ -v
"""

import pytest
from src.task_manager import TaskError
from src.models import Prioridade, StatusTarefa
from src.kanban import Coluna




# ── CRIAR TAREFA ─────────────────────────────────────────────────────────────

class TestCriarTarefa:

    def test_criar_tarefa_basica(self, manager):
        """✔ criar tarefa — campos obrigatórios."""
        t = manager.criar_tarefa("Nova tarefa", "Descrição", Prioridade.MEDIA)
        assert t.id == 1
        assert t.titulo == "Nova tarefa"

    def test_status_inicial_a_fazer(self, manager):
        """✔ criar tarefa — status inicial deve ser A Fazer."""
        t = manager.criar_tarefa("Tarefa teste", "Desc", Prioridade.BAIXA)
        assert t.status == StatusTarefa.A_FAZER

    def test_criar_com_responsavel(self, manager, usuario):
        """✔ criar tarefa — deve aceitar responsável."""
        t = manager.criar_tarefa("Tarefa", "Desc", Prioridade.ALTA, responsavel=usuario)
        assert t.responsavel == usuario

    def test_ids_incrementais(self, manager):
        """✔ criar tarefa — IDs devem ser únicos e crescentes."""
        t1 = manager.criar_tarefa("Tarefa um",   "D", Prioridade.ALTA)
        t2 = manager.criar_tarefa("Tarefa dois",  "D", Prioridade.MEDIA)
        t3 = manager.criar_tarefa("Tarefa tres",  "D", Prioridade.BAIXA)
        assert t1.id == 1
        assert t2.id == 2
        assert t3.id == 3

    def test_titulo_vazio_erro(self, manager):
        """✔ criar tarefa — título vazio deve lançar TaskError."""
        with pytest.raises(TaskError, match="vazio"):
            manager.criar_tarefa("", "Desc", Prioridade.MEDIA)

    def test_titulo_curto_erro(self, manager):
        """✔ criar tarefa — título curto deve lançar TaskError."""
        with pytest.raises(TaskError, match="mínimo 3"):
            manager.criar_tarefa("ab", "Desc", Prioridade.MEDIA)

    def test_titulo_espacos_removidos(self, manager):
        """✔ criar tarefa — espaços extras devem ser removidos."""
        t = manager.criar_tarefa("  Minha Tarefa  ", "Desc", Prioridade.BAIXA)
        assert t.titulo == "Minha Tarefa"

    def test_validar_tarefa(self, manager):
        """✔ criar tarefa — validar() deve retornar True para tarefa válida."""
        t = manager.criar_tarefa("Tarefa válida", "Desc", Prioridade.MEDIA)
        assert t.validar() is True


# ── LISTAR TAREFAS ────────────────────────────────────────────────────────────

class TestListarTarefas:

    def test_listar_todas(self, manager, tarefa_alta, tarefa_media):
        """✔ listar — deve retornar todas as tarefas."""
        assert len(manager.listar_tarefas()) == 2

    def test_listar_vazia(self, manager):
        """✔ listar — manager vazio retorna lista vazia."""
        assert manager.listar_tarefas() == []

    def test_filtrar_por_status(self, manager, tarefa_alta, tarefa_media):
        """✔ listar — filtra por status A Fazer."""
        lista = manager.listar_tarefas(status=StatusTarefa.A_FAZER)
        assert len(lista) == 2

    def test_filtrar_por_prioridade_alta(self, manager, tarefa_alta, tarefa_media):
        """✔ listar — filtra somente prioridade Alta."""
        lista = manager.listar_tarefas(prioridade=Prioridade.ALTA)
        assert len(lista) == 1
        assert lista[0].titulo == "Entregar relatório"

    def test_buscar_por_id_existente(self, manager, tarefa_alta):
        """✔ listar — busca por ID retorna a tarefa correta."""
        t = manager.buscar_por_id(tarefa_alta.id)
        assert t.titulo == "Entregar relatório"

    def test_buscar_id_inexistente(self, manager):
        """✔ listar — ID inexistente lança TaskError."""
        with pytest.raises(TaskError, match="não encontrada"):
            manager.buscar_por_id(999)

    def test_listar_criticas(self, manager, tarefa_alta, tarefa_media):
        """✔ listar — retorna apenas tarefas críticas."""
        criticas = manager.listar_criticas()
        assert len(criticas) == 1
        assert criticas[0].prioridade == Prioridade.ALTA


# ── EDITAR TAREFA ─────────────────────────────────────────────────────────────

class TestEditarTarefa:

    def test_editar_titulo(self, manager, tarefa_alta):
        """✔ editar — deve atualizar o título."""
        t = manager.editar_tarefa(tarefa_alta.id, titulo="Título atualizado")
        assert t.titulo == "Título atualizado"

    def test_editar_prioridade(self, manager, tarefa_alta):
        """✔ editar — deve alterar a prioridade."""
        t = manager.editar_tarefa(tarefa_alta.id, prioridade=Prioridade.BAIXA)
        assert t.prioridade == Prioridade.BAIXA

    def test_editar_responsavel(self, manager, tarefa_alta, usuario2):
        """✔ editar — deve atualizar o responsável."""
        t = manager.editar_tarefa(tarefa_alta.id, responsavel=usuario2)
        assert t.responsavel == usuario2

    def test_editar_registra_timestamp(self, manager, tarefa_alta):
        """✔ editar — deve registrar data de atualização."""
        assert tarefa_alta.data_atualizacao is None
        manager.editar_tarefa(tarefa_alta.id, titulo="Atualizada")
        assert tarefa_alta.data_atualizacao is not None

    def test_editar_titulo_vazio_erro(self, manager, tarefa_alta):
        """✔ editar — título vazio deve lançar TaskError."""
        with pytest.raises(TaskError, match="vazio"):
            manager.editar_tarefa(tarefa_alta.id, titulo="")

    def test_editar_id_inexistente(self, manager):
        """✔ editar — ID inexistente deve lançar TaskError."""
        with pytest.raises(TaskError):
            manager.editar_tarefa(999, titulo="X")

    def test_mover_status_em_progresso(self, manager, tarefa_alta):
        """✔ editar — deve mover para Em Progresso."""
        t = manager.mover_status(tarefa_alta.id, StatusTarefa.EM_PROGRESSO)
        assert t.status == StatusTarefa.EM_PROGRESSO

    def test_mover_status_concluido(self, manager, tarefa_alta):
        """✔ editar — deve mover para Concluído."""
        t = manager.mover_status(tarefa_alta.id, StatusTarefa.CONCLUIDO)
        assert t.status == StatusTarefa.CONCLUIDO


# ── EXCLUIR TAREFA ────────────────────────────────────────────────────────────

class TestExcluirTarefa:

    def test_excluir_existente(self, manager, tarefa_alta):
        """✔ excluir — deve remover com sucesso."""
        resultado = manager.excluir_tarefa(tarefa_alta.id)
        assert resultado is True
        assert manager.total_tarefas() == 0

    def test_excluir_inexistente(self, manager):
        """✔ excluir — ID inexistente deve lançar TaskError."""
        with pytest.raises(TaskError):
            manager.excluir_tarefa(999)

    def test_apos_excluir_nao_encontra(self, manager, tarefa_alta):
        """✔ excluir — após excluir busca por ID deve falhar."""
        manager.excluir_tarefa(tarefa_alta.id)
        with pytest.raises(TaskError):
            manager.buscar_por_id(tarefa_alta.id)


# ── VALIDAR PRIORIDADE ────────────────────────────────────────────────────────

class TestValidarPrioridade:

    def test_prioridade_alta_critica(self, manager):
        """✔ validar prioridade — Alta deve ser crítica."""
        t = manager.criar_tarefa("Urgente", "Desc", Prioridade.ALTA)
        assert t.esta_critica() is True

    def test_prioridade_media_nao_critica(self, manager):
        """✔ validar prioridade — Média não deve ser crítica."""
        t = manager.criar_tarefa("Normal", "Desc", Prioridade.MEDIA)
        assert t.esta_critica() is False

    def test_prioridade_baixa_nao_critica(self, manager):
        """✔ validar prioridade — Baixa não deve ser crítica."""
        t = manager.criar_tarefa("Rotina", "Desc", Prioridade.BAIXA)
        assert t.esta_critica() is False

    def test_total_por_status(self, manager, tarefa_alta, tarefa_media):
        """✔ validar — contagem por status correta."""
        manager.mover_status(tarefa_alta.id, StatusTarefa.EM_PROGRESSO)
        contagem = manager.total_por_status()
        assert contagem["A Fazer"] == 1
        assert contagem["Em Progresso"] == 1
        assert contagem["Concluído"] == 0

    def test_definir_prioridade(self, manager, tarefa_media):
        """✔ validar prioridade — deve alterar prioridade via método."""
        tarefa_media.definir_prioridade(Prioridade.ALTA)
        assert tarefa_media.prioridade == Prioridade.ALTA
        assert tarefa_media.esta_critica() is True


# ── KANBAN ────────────────────────────────────────────────────────────────────

class TestKanban:

    def test_adicionar_tarefa_kanban(self, manager, kanban, tarefa_alta):
        """✔ Kanban — deve adicionar tarefa na coluna correta."""
        kanban.adicionar_tarefa(tarefa_alta)
        coluna = kanban.listar_coluna(StatusTarefa.A_FAZER)
        assert tarefa_alta in coluna

    def test_mover_tarefa_kanban(self, manager, kanban, tarefa_alta):
        """✔ Kanban — deve mover tarefa entre colunas."""
        kanban.adicionar_tarefa(tarefa_alta)
        kanban.mover_tarefa(tarefa_alta, StatusTarefa.EM_PROGRESSO)
        assert tarefa_alta not in kanban.listar_coluna(StatusTarefa.A_FAZER)
        assert tarefa_alta in kanban.listar_coluna(StatusTarefa.EM_PROGRESSO)

    def test_listar_colunas(self, kanban, manager, tarefa_alta, tarefa_media):
        """✔ Kanban — deve listar todas as colunas."""
        kanban.adicionar_tarefa(tarefa_alta)
        kanban.adicionar_tarefa(tarefa_media)
        colunas = kanban.listar_colunas()
        assert "A Fazer" in colunas
        assert "Em Progresso" in colunas
        assert "Concluído" in colunas

    def test_listar_criticas_kanban(self, manager, kanban, tarefa_alta, tarefa_media):
        """✔ Kanban — deve retornar apenas tarefas críticas."""
        kanban.adicionar_tarefa(tarefa_alta)
        kanban.adicionar_tarefa(tarefa_media)
        criticas = kanban.listar_criticas()
        assert len(criticas) == 1
        assert criticas[0].prioridade == Prioridade.ALTA

    def test_coluna_adicionar_remover(self, manager, tarefa_alta):
        """✔ Coluna — deve adicionar e remover tarefa."""
        coluna = Coluna(1, "Teste", 1)
        coluna.adicionar_tarefa(tarefa_alta)
        assert coluna.total() == 1
        coluna.remover_tarefa(tarefa_alta)
        assert coluna.total() == 0
    
    def test_concluir_tarefa(self, manager):
        tarefa = manager.criar_tarefa(
            "Teste",
            "Desc",
            Prioridade.MEDIA,
        )

        tarefa.concluir()

        assert tarefa.status == StatusTarefa.CONCLUIDO