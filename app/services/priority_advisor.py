import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


class PriorityAdvisor:
    """Componente de priorização com heurística local e fallback seguro para LLM."""

    def __init__(self, api_timeout: float = 3.0) -> None:
        self.api_timeout = api_timeout
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"

    def suggest_proxima_atividade(
        self,
        atividades: List[Dict[str, Any]],
        use_llm: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """Sugere a próxima atividade usando LLM opcional ou heurística local."""
        if not atividades:
            return None

        if use_llm and self.api_key:
            try:
                suggestion = self._call_llm(atividades)
                if suggestion:
                    return suggestion
            except Exception:
                pass

        return self._local_heuristic(atividades)

    def _local_heuristic(self, atividades: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Escolhe a próxima atividade com base em regras locais simples."""
        prioridade = []
        for atividade in atividades:
            concluido = bool(atividade.get("estudo_concluido", False))
            revisao = bool(atividade.get("revisao_finalizada", False))
            score = 0
            if concluido:
                score += 10
            if revisao:
                score += 5
            if not concluido and not revisao:
                score -= 5
            prioridade.append((score, atividade))

        prioridade.sort(key=lambda item: (item[0], item[1].get("id_atividade", 0)))
        return prioridade[0][1] if prioridade else None

    def _call_llm(self, atividades: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Chama a API OpenAI para obter uma sugestão de prioridade."""
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente que sugere a próxima atividade de estudo mais urgente "
                        "com base no status de conclusão e revisão." 
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Atividades: " + json.dumps(atividades, ensure_ascii=False) + "\n"
                        "Retorne apenas o id_atividade da melhor escolha no formato JSON: {\"id_atividade\": 123}."
                    ),
                },
            ],
            "max_tokens": 64,
            "temperature": 0.0,
        }

        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.api_timeout) as response:
                body = response.read().decode("utf-8")
                data = json.loads(body)
                return self._parse_llm_response(data, atividades)
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, TimeoutError):
            return None

    def _parse_llm_response(
        self, data: Dict[str, Any], atividades: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Extrai atividade sugerida da resposta da LLM."""
        choices = data.get("choices")
        if not choices:
            return None

        text = choices[0].get("message", {}).get("content", "")
        try:
            parsed = json.loads(text.strip())
            atividade_id = int(parsed.get("id_atividade"))
            for atividade in atividades:
                if atividade.get("id_atividade") == atividade_id:
                    return atividade
        except (ValueError, TypeError, json.JSONDecodeError):
            return None

        return None
