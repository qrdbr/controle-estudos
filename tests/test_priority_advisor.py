import json
import pytest
from unittest.mock import MagicMock, patch
from app.services.priority_advisor import PriorityAdvisor


class TestPriorityAdvisor:
    """Testes para PriorityAdvisor."""

    @pytest.fixture
    def advisor(self):
        """Fixture para instância do PriorityAdvisor."""
        return PriorityAdvisor(api_timeout=1.0)

    @pytest.fixture
    def sample_activities(self):
        """Fixture com atividades de exemplo."""
        return [
            {
                "id_atividade": 1,
                "descricao_atividade": "Atividade 1",
                "estudo_concluido": 0,
                "revisao_finalizada": 0,
            },
            {
                "id_atividade": 2,
                "descricao_atividade": "Atividade 2",
                "estudo_concluido": 1,
                "revisao_finalizada": 0,
            },
            {
                "id_atividade": 3,
                "descricao_atividade": "Atividade 3",
                "estudo_concluido": 1,
                "revisao_finalizada": 1,
            },
            {
                "id_atividade": 4,
                "descricao_atividade": "Atividade 4",
                "estudo_concluido": 0,
                "revisao_finalizada": 1,
            },
        ]

    def test_local_heuristic_prioritizes_completed_study(self, advisor, sample_activities):
        """Testa heurística local priorizando atividades com estudo concluído."""
        with patch.dict("os.environ", {}, clear=True):
            result = advisor.suggest_proxima_atividade(sample_activities, use_llm=False)
        assert result["id_atividade"] == 3  # estudo_concluido=1, revisao_finalizada=1 (score 15)

    def test_local_heuristic_prioritizes_revision_completed(self, advisor, sample_activities):
        """Testa heurística local priorizando atividades com revisão finalizada."""
        # Ajustar atividades para testar
        activities = [
            {"id_atividade": 1, "estudo_concluido": 0, "revisao_finalizada": 0},
            {"id_atividade": 2, "estudo_concluido": 0, "revisao_finalizada": 1},
        ]
        with patch.dict("os.environ", {}, clear=True):
            result = advisor.suggest_proxima_atividade(activities, use_llm=False)
        assert result["id_atividade"] == 2  # revisao_finalizada=1 (score 5)

    def test_local_heuristic_avoids_incomplete(self, advisor):
        """Testa heurística local evitando atividades incompletas."""
        activities = [
            {"id_atividade": 1, "estudo_concluido": 0, "revisao_finalizada": 0},
            {"id_atividade": 2, "estudo_concluido": 1, "revisao_finalizada": 0},
        ]
        with patch.dict("os.environ", {}, clear=True):
            result = advisor.suggest_proxima_atividade(activities, use_llm=False)
        assert result["id_atividade"] == 2  # estudo_concluido=1 (score 10)

    def test_fallback_to_local_when_llm_fails(self, advisor, sample_activities):
        """Testa fallback para heurística local quando LLM falha."""
        advisor.api_key = "fake_key"
        with patch.object(advisor, '_call_llm', side_effect=Exception("API Error")):
            result = advisor.suggest_proxima_atividade(sample_activities, use_llm=True)
        assert result["id_atividade"] == 3  # Mesmo resultado da heurística local

    def test_llm_success_returns_suggested_activity(self, advisor, sample_activities):
        """Testa sucesso da LLM retornando atividade sugerida."""
        advisor.api_key = "fake_key"
        with patch.object(advisor, '_call_llm', return_value=sample_activities[1]):
            result = advisor.suggest_proxima_atividade(sample_activities, use_llm=True)
        assert result["id_atividade"] == 2

    def test_llm_invalid_response_falls_back(self, advisor, sample_activities):
        """Testa resposta inválida da LLM caindo para fallback."""
        advisor.api_key = "fake_key"
        with patch.object(advisor, '_call_llm', return_value=None):
            result = advisor.suggest_proxima_atividade(sample_activities, use_llm=True)
        assert result["id_atividade"] == 3  # Fallback

    def test_no_activities_returns_none(self, advisor):
        """Testa retorno None quando não há atividades."""
        result = advisor.suggest_proxima_atividade([], use_llm=False)
        assert result is None

    def test_use_llm_false_uses_local(self, advisor, sample_activities):
        """Testa que use_llm=False força uso da heurística local."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "fake_key"}):
            with patch("urllib.request.urlopen") as mock_urlopen:
                mock_urlopen.return_value.__enter__.return_value.read.return_value = json.dumps({"choices": []}).encode("utf-8")
                result = advisor.suggest_proxima_atividade(sample_activities, use_llm=False)
        assert result["id_atividade"] == 3  # Local, não chama API

    def test_no_api_key_uses_local(self, advisor, sample_activities):
        """Testa uso da heurística local quando não há API key."""
        with patch.dict("os.environ", {}, clear=True):
            result = advisor.suggest_proxima_atividade(sample_activities, use_llm=True)
        assert result["id_atividade"] == 3

    def test_timeout_handling(self, advisor, sample_activities):
        """Testa tratamento de timeout na chamada da API."""
        advisor.api_key = "fake_key"
        with patch.object(advisor, '_call_llm', side_effect=TimeoutError):
            result = advisor.suggest_proxima_atividade(sample_activities, use_llm=True)
        assert result["id_atividade"] == 3  # Fallback

    # Outros testes importantes:
    # - Testar parsing de resposta LLM com ID inexistente
    # - Testar resposta LLM sem choices
    # - Testar atividades com mesmo score (ordenação por ID)
    # - Testar inicialização com timeout customizado