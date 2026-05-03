import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.models.control import TrilhaOut, CursoOut, AtividadesOut


@pytest.fixture
def client():
    """Fixture para TestClient."""
    return TestClient(app)


class TestControlRoutes:
    """Testes para as rotas de controle usando TestClient."""

    # --- Trilhas ---

    def test_create_trilha_success(self, client):
        """Testa criação de trilha com sucesso (201)."""
        data = {"descricao_trilha": "Trilha de Teste"}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.create_trilha.return_value = 1
            response = client.post("/api/v1/trilhas", json=data)
            assert response.status_code == 201
            assert response.json() == {"id_trilha": 1, "descricao_trilha": "Trilha de Teste"}
            mock_service.create_trilha.assert_called_once_with("Trilha de Teste")

    def test_list_trilhas_success(self, client):
        """Testa listagem de trilhas (200)."""
        mock_trilhas = [
            {"id_trilha": 1, "descricao_trilha": "Trilha 1"},
            {"id_trilha": 2, "descricao_trilha": "Trilha 2"}
        ]
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.list_trilhas.return_value = mock_trilhas
            response = client.get("/api/v1/trilhas")
            assert response.status_code == 200
            assert response.json() == mock_trilhas
            mock_service.list_trilhas.assert_called_once()

    def test_get_trilha_success(self, client):
        """Testa obtenção de trilha por ID (200)."""
        mock_trilha = {"id_trilha": 1, "descricao_trilha": "Trilha 1"}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.get_trilha_by_id.return_value = mock_trilha
            response = client.get("/api/v1/trilhas/1")
            assert response.status_code == 200
            assert response.json() == mock_trilha
            mock_service.get_trilha_by_id.assert_called_once_with(1)

    def test_get_trilha_not_found(self, client):
        """Testa obtenção de trilha inexistente (404)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.get_trilha_by_id.return_value = None
            response = client.get("/api/v1/trilhas/999")
            assert response.status_code == 404
            assert response.json() == {"detail": "Trilha não encontrada"}

    def test_update_trilha_success(self, client):
        """Testa atualização de trilha (200)."""
        data = {"descricao_trilha": "Trilha Atualizada"}
        mock_updated = {"id_trilha": 1, "descricao_trilha": "Trilha Atualizada"}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.update_trilha.return_value = True
            mock_service.get_trilha_by_id.return_value = mock_updated
            response = client.put("/api/v1/trilhas/1", json=data)
            assert response.status_code == 200
            assert response.json() == mock_updated
            mock_service.update_trilha.assert_called_once_with(1, "Trilha Atualizada")

    def test_update_trilha_not_found(self, client):
        """Testa atualização de trilha inexistente (404)."""
        data = {"descricao_trilha": "Trilha Atualizada"}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.update_trilha.return_value = False
            response = client.put("/api/v1/trilhas/999", json=data)
            assert response.status_code == 404
            assert response.json() == {"detail": "Trilha não encontrada"}

    def test_delete_trilha_success(self, client):
        """Testa exclusão de trilha (204)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.delete_trilha.return_value = True
            response = client.delete("/api/v1/trilhas/1")
            assert response.status_code == 204
            mock_service.delete_trilha.assert_called_once_with(1)

    def test_delete_trilha_not_found(self, client):
        """Testa exclusão de trilha inexistente (404)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.delete_trilha.return_value = False
            response = client.delete("/api/v1/trilhas/999")
            assert response.status_code == 404
            assert response.json() == {"detail": "Trilha não encontrada"}

    # --- Cursos ---

    def test_create_curso_success(self, client):
        """Testa criação de curso com sucesso (201)."""
        data = {"descricao_curso": "Curso de Teste", "id_trilha": 1}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.create_curso.return_value = 1
            response = client.post("/api/v1/cursos", json=data)
            assert response.status_code == 201
            assert response.json() == {"id_curso": 1, "id_trilha": 1, "descricao_curso": "Curso de Teste"}
            mock_service.create_curso.assert_called_once_with("Curso de Teste", 1)

    def test_create_curso_trilha_not_found(self, client):
        """Testa criação de curso com trilha inexistente (400)."""
        data = {"descricao_curso": "Curso de Teste", "id_trilha": 999}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.create_curso.return_value = None
            response = client.post("/api/v1/cursos", json=data)
            assert response.status_code == 400
            assert response.json() == {"detail": "Trilha não encontrada"}

    def test_list_cursos_success(self, client):
        """Testa listagem de cursos (200)."""
        mock_cursos = [
            {"id_curso": 1, "id_trilha": 1, "descricao_curso": "Curso 1"},
            {"id_curso": 2, "id_trilha": 1, "descricao_curso": "Curso 2"}
        ]
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.list_cursos.return_value = mock_cursos
            response = client.get("/api/v1/cursos")
            assert response.status_code == 200
            assert response.json() == mock_cursos

    def test_get_curso_success(self, client):
        """Testa obtenção de curso por ID (200)."""
        mock_curso = {"id_curso": 1, "id_trilha": 1, "descricao_curso": "Curso 1"}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.get_curso_by_id.return_value = mock_curso
            response = client.get("/api/v1/cursos/1")
            assert response.status_code == 200
            assert response.json() == mock_curso

    def test_get_curso_not_found(self, client):
        """Testa obtenção de curso inexistente (404)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.get_curso_by_id.return_value = None
            response = client.get("/api/v1/cursos/999")
            assert response.status_code == 404
            assert response.json() == {"detail": "Curso não encontrado"}

    def test_update_curso_success(self, client):
        """Testa atualização de curso (200)."""
        data = {"descricao_curso": "Curso Atualizado", "id_trilha": 1}
        mock_updated = {"id_curso": 1, "id_trilha": 1, "descricao_curso": "Curso Atualizado"}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.update_curso.return_value = True
            mock_service.get_curso_by_id.return_value = mock_updated
            response = client.put("/api/v1/cursos/1", json=data)
            assert response.status_code == 200
            assert response.json() == mock_updated

    def test_update_curso_not_found(self, client):
        """Testa atualização de curso inexistente (404)."""
        data = {"descricao_curso": "Curso Atualizado", "id_trilha": 1}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.update_curso.return_value = False
            response = client.put("/api/v1/cursos/999", json=data)
            assert response.status_code == 404

    def test_delete_curso_success(self, client):
        """Testa exclusão de curso (204)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.delete_curso.return_value = True
            response = client.delete("/api/v1/cursos/1")
            assert response.status_code == 204

    def test_delete_curso_not_found(self, client):
        """Testa exclusão de curso inexistente (404)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.delete_curso.return_value = False
            response = client.delete("/api/v1/cursos/999")
            assert response.status_code == 404

    # --- Atividades ---

    def test_create_atividade_success(self, client):
        """Testa criação de atividade com sucesso (201)."""
        data = {"descricao_atividade": "Atividade de Teste", "id_curso": 1}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.create_atividade.return_value = 1
            response = client.post("/api/v1/atividades", json=data)
            assert response.status_code == 201
            expected = {
                "id_atividade": 1,
                "id_curso": 1,
                "descricao_atividade": "Atividade de Teste",
                "estudo_concluido": False,
                "revisao_finalizada": False
            }
            assert response.json() == expected

    def test_create_atividade_curso_not_found(self, client):
        """Testa criação de atividade com curso inexistente (400)."""
        data = {"descricao_atividade": "Atividade de Teste", "id_curso": 999}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.create_atividade.return_value = None
            response = client.post("/api/v1/atividades", json=data)
            assert response.status_code == 400

    def test_list_atividades_success(self, client):
        """Testa listagem de atividades (200)."""
        mock_atividades = [
            {"id_atividade": 1, "id_curso": 1, "descricao_atividade": "Atividade 1", "estudo_concluido": False, "revisao_finalizada": False},
            {"id_atividade": 2, "id_curso": 1, "descricao_atividade": "Atividade 2", "estudo_concluido": True, "revisao_finalizada": False}
        ]
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.list_atividades.return_value = mock_atividades
            response = client.get("/api/v1/atividades")
            assert response.status_code == 200
            assert response.json() == mock_atividades

    def test_get_atividade_success(self, client):
        """Testa obtenção de atividade por ID (200)."""
        mock_atividade = {"id_atividade": 1, "id_curso": 1, "descricao_atividade": "Atividade 1", "estudo_concluido": False, "revisao_finalizada": False}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.get_atividade_by_id.return_value = mock_atividade
            response = client.get("/api/v1/atividades/1")
            assert response.status_code == 200
            assert response.json() == mock_atividade

    def test_get_atividade_not_found(self, client):
        """Testa obtenção de atividade inexistente (404)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.get_atividade_by_id.return_value = None
            response = client.get("/api/v1/atividades/999")
            assert response.status_code == 404

    def test_update_atividade_success(self, client):
        """Testa atualização de atividade (200)."""
        data = {"descricao_atividade": "Atividade Atualizada", "estudo_concluido": True, "revisao_finalizada": True, "id_curso": 1}
        mock_updated = {"id_atividade": 1, "id_curso": 1, "descricao_atividade": "Atividade Atualizada", "estudo_concluido": True, "revisao_finalizada": True}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.update_atividade.return_value = True
            mock_service.get_atividade_by_id.return_value = mock_updated
            response = client.put("/api/v1/atividades/1", json=data)
            assert response.status_code == 200
            assert response.json() == mock_updated

    def test_update_atividade_not_found(self, client):
        """Testa atualização de atividade inexistente (404)."""
        data = {"descricao_atividade": "Atividade Atualizada", "estudo_concluido": True, "revisao_finalizada": True, "id_curso": 1}
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.update_atividade.return_value = False
            response = client.put("/api/v1/atividades/999", json=data)
            assert response.status_code == 404

    def test_delete_atividade_success(self, client):
        """Testa exclusão de atividade (204)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.delete_atividade.return_value = True
            response = client.delete("/api/v1/atividades/1")
            assert response.status_code == 204

    def test_delete_atividade_not_found(self, client):
        """Testa exclusão de atividade inexistente (404)."""
        with patch('app.api.control_routes.service') as mock_service:
            mock_service.delete_atividade.return_value = False
            response = client.delete("/api/v1/atividades/999")
            assert response.status_code == 404