from typing import Optional, Dict, Any, List
from app.repositories.control_repository import ControlRepository
from app.services.priority_advisor import PriorityAdvisor

class ControlService:
    """Camada de serviço para regras de negócio de trilha, curso e atividades."""
    def __init__(self, repository: Optional[ControlRepository] = None, advisor: Optional[PriorityAdvisor] = None):
        self.repository = repository or ControlRepository()
        self.advisor = advisor or PriorityAdvisor()

    # --- Atividades de Estudo ---
    def concluir_estudo(self, id_atividade: int) -> bool:
        atividade = self.repository.get_atividade_by_id(id_atividade)
        if not atividade:
            return False
        atividade["estudo_concluido"] = True
        return self.repository.update_atividade(
            id_atividade=id_atividade,
            descricao_atividade=atividade["descricao_atividade"],
            id_curso=atividade["id_curso"],
            estudo_concluido=True,
            revisao_finalizada=atividade["revisao_finalizada"]
        )

    def concluir_revisao(self, id_atividade: int) -> bool:
        atividade = self.repository.get_atividade_by_id(id_atividade)
        if not atividade:
            return False
        atividade["revisao_finalizada"] = True
        return self.repository.update_atividade(
            id_atividade=id_atividade,
            descricao_atividade=atividade["descricao_atividade"],
            id_curso=atividade["id_curso"],
            estudo_concluido=atividade["estudo_concluido"],
            revisao_finalizada=True
        )

    def sugerir_proxima_atividade(self, use_llm: bool = True) -> Optional[Dict[str, Any]]:
        atividades = self.repository.list_atividades()
        return self.advisor.sugerir_proxima_atividade(atividades, use_llm=use_llm)

    # Métodos CRUD podem ser expostos conforme necessidade, delegando ao repository
