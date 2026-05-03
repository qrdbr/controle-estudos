import pytest
import tempfile
import os
from unittest.mock import MagicMock
from app.services.control_service import ControlService
from app.repositories.control_repository import ControlRepository
from app.services.priority_advisor import PriorityAdvisor


@pytest.fixture
def temp_db():
    """Fixture para criar um banco de dados temporário para testes."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    try:
        os.unlink(path)
    except PermissionError:
        pass  # Arquivo ainda em uso, será deletado pelo sistema


@pytest.fixture
def repository(temp_db):
    """Fixture para criar um ControlRepository com banco temporário."""
    return ControlRepository(db_path=temp_db)


@pytest.fixture
def mock_advisor():
    """Fixture para mockar o PriorityAdvisor."""
    advisor = MagicMock(spec=PriorityAdvisor)
    advisor.suggest_proxima_atividade.return_value = None
    return advisor


@pytest.fixture
def service(repository, mock_advisor):
    """Fixture para criar um ControlService com dependências injetadas."""
    return ControlService(repository=repository, advisor=mock_advisor)


# ============================================================================
# Testes para Trilhas
# ============================================================================

class TestTrilhaCreate:
    """Testes de criação de trilhas."""

    def test_criar_trilha_com_sucesso(self, service):
        """Deve criar uma trilha e retornar um ID válido."""
        trilha_id = service.create_trilha("Python Avançado")
        assert trilha_id is not None
        assert isinstance(trilha_id, int)
        assert trilha_id > 0

    def test_criar_multiplas_trilhas(self, service):
        """Deve criar múltiplas trilhas com IDs diferentes."""
        id1 = service.create_trilha("Trilha 1")
        id2 = service.create_trilha("Trilha 2")
        assert id1 != id2
        assert id1 > 0 and id2 > 0


class TestTrilhaList:
    """Testes de listagem de trilhas."""

    def test_listar_trilhas_vazio(self, service):
        """Deve retornar lista vazia quando não há trilhas."""
        trilhas = service.list_trilhas()
        assert trilhas == []

    def test_listar_trilhas_com_dados(self, service):
        """Deve listar todas as trilhas criadas."""
        service.create_trilha("Trilha A")
        service.create_trilha("Trilha B")
        trilhas = service.list_trilhas()
        assert len(trilhas) == 2
        assert trilhas[0]["descricao_trilha"] == "Trilha A"
        assert trilhas[1]["descricao_trilha"] == "Trilha B"


class TestTrilhaGetById:
    """Testes de busca de trilha por ID."""

    def test_obter_trilha_existente(self, service):
        """Deve retornar a trilha quando o ID existe."""
        id_criado = service.create_trilha("Minha Trilha")
        trilha = service.get_trilha_by_id(id_criado)
        assert trilha is not None
        assert trilha["id_trilha"] == id_criado
        assert trilha["descricao_trilha"] == "Minha Trilha"

    def test_obter_trilha_inexistente(self, service):
        """Deve retornar None quando o ID não existe."""
        trilha = service.get_trilha_by_id(999)
        assert trilha is None


class TestTrilhaUpdate:
    """Testes de atualização de trilhas."""

    def test_atualizar_trilha_com_sucesso(self, service):
        """Deve atualizar a descricao da trilha."""
        id_trilha = service.create_trilha("Descrição Original")
        success = service.update_trilha(id_trilha, "Descrição Atualizada")
        assert success is True
        trilha = service.get_trilha_by_id(id_trilha)
        assert trilha["descricao_trilha"] == "Descrição Atualizada"

    def test_atualizar_trilha_inexistente(self, service):
        """Deve retornar False ao tentar atualizar trilha inexistente."""
        success = service.update_trilha(999, "Nova Descrição")
        assert success is False

    def test_atualizar_trilha_com_none(self, service):
        """Deve manter a descrição original se None for passado."""
        id_trilha = service.create_trilha("Original")
        success = service.update_trilha(id_trilha, None)
        assert success is True
        trilha = service.get_trilha_by_id(id_trilha)
        assert trilha["descricao_trilha"] == "Original"


class TestTrilhaDelete:
    """Testes de exclusão de trilhas."""

    def test_deletar_trilha_existente(self, service):
        """Deve deletar a trilha e não poder recuperá-la."""
        id_trilha = service.create_trilha("Trilha Temporária")
        success = service.delete_trilha(id_trilha)
        assert success is True
        trilha = service.get_trilha_by_id(id_trilha)
        assert trilha is None

    def test_deletar_trilha_inexistente(self, service):
        """Deve retornar False ao tentar deletar trilha inexistente."""
        success = service.delete_trilha(999)
        assert success is False


# ============================================================================
# Testes para Cursos
# ============================================================================

class TestCursoCreate:
    """Testes de criação de cursos."""

    def test_criar_curso_com_sucesso(self, service):
        """Deve criar um curso ligado a uma trilha existente."""
        id_trilha = service.create_trilha("Trilha Base")
        id_curso = service.create_curso("Curso Python", id_trilha)
        assert id_curso is not None
        assert isinstance(id_curso, int)
        assert id_curso > 0

    def test_criar_curso_com_trilha_inexistente(self, service):
        """Deve retornar None ao tentar criar curso com trilha inexistente."""
        id_curso = service.create_curso("Curso Órfão", 999)
        assert id_curso is None


class TestCursoList:
    """Testes de listagem de cursos."""

    def test_listar_cursos_vazio(self, service):
        """Deve retornar lista vazia quando não há cursos."""
        cursos = service.list_cursos()
        assert cursos == []

    def test_listar_cursos_com_dados(self, service):
        """Deve listar todos os cursos criados."""
        id_trilha = service.create_trilha("Trilha")
        service.create_curso("Curso A", id_trilha)
        service.create_curso("Curso B", id_trilha)
        cursos = service.list_cursos()
        assert len(cursos) == 2
        assert cursos[0]["descricao_curso"] == "Curso A"


class TestCursoGetById:
    """Testes de busca de curso por ID."""

    def test_obter_curso_existente(self, service):
        """Deve retornar o curso quando o ID existe."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Meu Curso", id_trilha)
        curso = service.get_curso_by_id(id_curso)
        assert curso is not None
        assert curso["id_curso"] == id_curso
        assert curso["descricao_curso"] == "Meu Curso"
        assert curso["id_trilha"] == id_trilha

    def test_obter_curso_inexistente(self, service):
        """Deve retornar None quando o ID não existe."""
        curso = service.get_curso_by_id(999)
        assert curso is None


class TestCursoUpdate:
    """Testes de atualização de cursos."""

    def test_atualizar_curso_descricao(self, service):
        """Deve atualizar a descrição do curso."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Descrição Original", id_trilha)
        success = service.update_curso(id_curso, "Descrição Atualizada", id_trilha)
        assert success is True
        curso = service.get_curso_by_id(id_curso)
        assert curso["descricao_curso"] == "Descrição Atualizada"

    def test_atualizar_curso_trilha(self, service):
        """Deve atualizar a trilha do curso."""
        id_trilha1 = service.create_trilha("Trilha 1")
        id_trilha2 = service.create_trilha("Trilha 2")
        id_curso = service.create_curso("Curso", id_trilha1)
        success = service.update_curso(id_curso, None, id_trilha2)
        assert success is True
        curso = service.get_curso_by_id(id_curso)
        assert curso["id_trilha"] == id_trilha2

    def test_atualizar_curso_com_trilha_inexistente(self, service):
        """Deve retornar False ao atualizar com trilha inexistente."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        success = service.update_curso(id_curso, None, 999)
        assert success is False

    def test_atualizar_curso_inexistente(self, service):
        """Deve retornar False ao atualizar curso inexistente."""
        success = service.update_curso(999, "Nova Descrição", 1)
        assert success is False


class TestCursoDelete:
    """Testes de exclusão de cursos."""

    def test_deletar_curso_existente(self, service):
        """Deve deletar o curso."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso Temporário", id_trilha)
        success = service.delete_curso(id_curso)
        assert success is True
        curso = service.get_curso_by_id(id_curso)
        assert curso is None

    def test_deletar_curso_inexistente(self, service):
        """Deve retornar False ao deletar curso inexistente."""
        success = service.delete_curso(999)
        assert success is False


# ============================================================================
# Testes para Atividades
# ============================================================================

class TestAtividadeCreate:
    """Testes de criação de atividades."""

    def test_criar_atividade_com_sucesso(self, service):
        """Deve criar uma atividade ligada a um curso existente."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade 1", id_curso)
        assert id_atividade is not None
        assert isinstance(id_atividade, int)
        assert id_atividade > 0

    def test_criar_atividade_com_curso_inexistente(self, service):
        """Deve retornar None ao criar atividade com curso inexistente."""
        id_atividade = service.create_atividade("Atividade Órfã", 999)
        assert id_atividade is None


class TestAtividadeList:
    """Testes de listagem de atividades."""

    def test_listar_atividades_vazio(self, service):
        """Deve retornar lista vazia quando não há atividades."""
        atividades = service.list_atividades()
        assert atividades == []

    def test_listar_atividades_com_dados(self, service):
        """Deve listar todas as atividades criadas."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        service.create_atividade("Atividade A", id_curso)
        service.create_atividade("Atividade B", id_curso)
        atividades = service.list_atividades()
        assert len(atividades) == 2
        assert atividades[0]["descricao_atividade"] == "Atividade A"


class TestAtividadeGetById:
    """Testes de busca de atividade por ID."""

    def test_obter_atividade_existente(self, service):
        """Deve retornar a atividade quando o ID existe."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Minha Atividade", id_curso)
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade is not None
        assert atividade["id_atividade"] == id_atividade
        assert atividade["descricao_atividade"] == "Minha Atividade"
        assert atividade["id_curso"] == id_curso

    def test_obter_atividade_inexistente(self, service):
        """Deve retornar None quando o ID não existe."""
        atividade = service.get_atividade_by_id(999)
        assert atividade is None


class TestAtividadeUpdate:
    """Testes de atualização de atividades."""

    def test_atualizar_atividade_descricao(self, service):
        """Deve atualizar a descrição da atividade."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Original", id_curso)
        success = service.update_atividade(id_atividade, "Atualizada", id_curso)
        assert success is True
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade["descricao_atividade"] == "Atualizada"

    def test_atualizar_atividade_estudo_concluido(self, service):
        """Deve marcar o estudo como concluído."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade", id_curso)
        success = service.update_atividade(id_atividade, None, id_curso, estudo_concluido=True)
        assert success is True
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade["estudo_concluido"] == 1

    def test_atualizar_atividade_revisao_finalizada(self, service):
        """Deve marcar a revisão como finalizada."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade", id_curso)
        success = service.update_atividade(id_atividade, None, id_curso, revisao_finalizada=True)
        assert success is True
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade["revisao_finalizada"] == 1

    def test_atualizar_atividade_com_curso_inexistente(self, service):
        """Deve retornar False ao atualizar com curso inexistente."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade", id_curso)
        success = service.update_atividade(id_atividade, None, 999)
        assert success is False

    def test_atualizar_atividade_inexistente(self, service):
        """Deve retornar False ao atualizar atividade inexistente."""
        success = service.update_atividade(999, "Nova Descrição", 1)
        assert success is False


class TestAtividadeDelete:
    """Testes de exclusão de atividades."""

    def test_deletar_atividade_existente(self, service):
        """Deve deletar a atividade."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade Temporária", id_curso)
        success = service.delete_atividade(id_atividade)
        assert success is True
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade is None

    def test_deletar_atividade_inexistente(self, service):
        """Deve retornar False ao deletar atividade inexistente."""
        success = service.delete_atividade(999)
        assert success is False


# ============================================================================
# Testes para métodos de status
# ============================================================================

class TestAtividadeStatus:
    """Testes para marcar atividade como concluída."""

    def test_concluir_estudo(self, service):
        """Deve marcar o estudo como concluído."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade", id_curso)
        success = service.concluir_estudo(id_atividade)
        assert success is True
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade["estudo_concluido"] == 1

    def test_concluir_estudo_inexistente(self, service):
        """Deve retornar False ao concluir estudo de atividade inexistente."""
        success = service.concluir_estudo(999)
        assert success is False

    def test_concluir_revisao(self, service):
        """Deve marcar a revisão como finalizada."""
        id_trilha = service.create_trilha("Trilha")
        id_curso = service.create_curso("Curso", id_trilha)
        id_atividade = service.create_atividade("Atividade", id_curso)
        success = service.concluir_revisao(id_atividade)
        assert success is True
        atividade = service.get_atividade_by_id(id_atividade)
        assert atividade["revisao_finalizada"] == 1

    def test_concluir_revisao_inexistente(self, service):
        """Deve retornar False ao finalizar revisão de atividade inexistente."""
        success = service.concluir_revisao(999)
        assert success is False
