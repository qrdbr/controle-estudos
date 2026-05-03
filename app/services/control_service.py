from typing import Optional, Dict, Any, List
from app.repositories.control_repository import ControlRepository
from app.services.priority_advisor import PriorityAdvisor

class ControlService:
    """Camada de serviço para regras de negócio de trilha, curso e atividades."""
    def __init__(self, repository: Optional[ControlRepository] = None, advisor: Optional[PriorityAdvisor] = None):
        self.repository = repository or ControlRepository()
        self.advisor = advisor or PriorityAdvisor()

    # --- Trilhas ---
    def create_trilha(self, descricao_trilha: str) -> int:
        return self.repository.create_trilha(descricao_trilha)

    def list_trilhas(self) -> List[Dict[str, Any]]:
        return self.repository.list_trilhas()

    def get_trilha_by_id(self, id_trilha: int) -> Optional[Dict[str, Any]]:
        return self.repository.get_trilha_by_id(id_trilha)

    def update_trilha(self, id_trilha: int, descricao_trilha: Optional[str] = None) -> bool:
        trilha = self.repository.get_trilha_by_id(id_trilha)
        if not trilha:
            return False
        new_descricao = descricao_trilha if descricao_trilha is not None else trilha["descricao_trilha"]
        return self.repository.update_trilha(id_trilha, new_descricao)

    def delete_trilha(self, id_trilha: int) -> bool:
        return self.repository.delete_trilha(id_trilha)

    # --- Cursos ---
    def create_curso(self, descricao_curso: str, id_trilha: int) -> Optional[int]:
        # Verificar se trilha existe
        if not self.repository.get_trilha_by_id(id_trilha):
            return None
        return self.repository.create_curso(descricao_curso, id_trilha)

    def list_cursos(self) -> List[Dict[str, Any]]:
        return self.repository.list_cursos()

    def get_curso_by_id(self, id_curso: int) -> Optional[Dict[str, Any]]:
        return self.repository.get_curso_by_id(id_curso)

    def update_curso(self, id_curso: int, descricao_curso: Optional[str] = None, id_trilha: Optional[int] = None) -> bool:
        curso = self.repository.get_curso_by_id(id_curso)
        if not curso:
            return False
        new_descricao = descricao_curso if descricao_curso is not None else curso["descricao_curso"]
        new_id_trilha = id_trilha if id_trilha is not None else curso["id_trilha"]
        # Verificar se nova trilha existe
        if not self.repository.get_trilha_by_id(new_id_trilha):
            return False
        return self.repository.update_curso(id_curso, new_descricao, new_id_trilha)

    def delete_curso(self, id_curso: int) -> bool:
        return self.repository.delete_curso(id_curso)

    # --- Atividades ---
    def create_atividade(self, descricao_atividade: str, id_curso: int) -> Optional[int]:
        # Verificar se curso existe
        if not self.repository.get_curso_by_id(id_curso):
            return None
        return self.repository.create_atividade(descricao_atividade, id_curso)

    def list_atividades(self) -> List[Dict[str, Any]]:
        return self.repository.list_atividades()

    def get_atividade_by_id(self, id_atividade: int) -> Optional[Dict[str, Any]]:
        return self.repository.get_atividade_by_id(id_atividade)

    def update_atividade(self, id_atividade: int, descricao_atividade: Optional[str] = None, id_curso: Optional[int] = None, estudo_concluido: Optional[bool] = None, revisao_finalizada: Optional[bool] = None) -> bool:
        atividade = self.repository.get_atividade_by_id(id_atividade)
        if not atividade:
            return False
        new_descricao = descricao_atividade if descricao_atividade is not None else atividade["descricao_atividade"]
        new_id_curso = id_curso if id_curso is not None else atividade["id_curso"]
        # Verificar se novo curso existe
        if not self.repository.get_curso_by_id(new_id_curso):
            return False
        new_estudo = estudo_concluido if estudo_concluido is not None else atividade["estudo_concluido"]
        new_revisao = revisao_finalizada if revisao_finalizada is not None else atividade["revisao_finalizada"]
        return self.repository.update_atividade(id_atividade, new_descricao, new_id_curso, new_estudo, new_revisao)

    def delete_atividade(self, id_atividade: int) -> bool:
        return self.repository.delete_atividade(id_atividade)

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
