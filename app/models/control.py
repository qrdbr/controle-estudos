from pydantic import BaseModel, Field
from typing import Optional

# Modelos para Trilha
class TrilhaCreate(BaseModel):
    """Dados para criar uma trilha."""
    descricao_trilha: str = Field(..., min_length=3, max_length=255)

class TrilhaUpdate(BaseModel):
    """Dados para atualizar uma trilha."""
    descricao_trilha: Optional[str] = Field(None, min_length=3, max_length=255)

class TrilhaOut(BaseModel):
    """Retorno de uma trilha."""
    id_trilha: int
    descricao_trilha: str
    class Config:
        from_attributes = True

# Modelos para Curso
class CursoCreate(BaseModel):
    """Dados para criar um curso."""
    descricao_curso: str = Field(..., min_length=3, max_length=255)
    id_trilha: int = Field(..., gt=0)

class CursoUpdate(BaseModel):
    """Dados para atualizar um curso."""
    descricao_curso: Optional[str] = Field(None, min_length=3, max_length=255)
    id_trilha: Optional[int] = Field(None, gt=0)

class CursoOut(BaseModel):
    """Retorno de um curso."""
    id_curso: int
    id_trilha: int
    descricao_curso: str
    class Config:
        from_attributes = True

# Modelos para Atividades de Estudo
class AtividadesCreate(BaseModel):
    """Dados para criar uma atividade de estudo."""
    descricao_atividade: str = Field(..., min_length=3, max_length=255)
    id_curso: int = Field(..., gt=0)

class AtividadesUpdate(BaseModel):
    """Dados para atualizar uma atividade de estudo."""
    descricao_atividade: Optional[str] = Field(None, min_length=3, max_length=255)
    estudo_concluido: Optional[bool] = None
    revisao_finalizada: Optional[bool] = None
    id_curso: Optional[int] = Field(None, gt=0)

class AtividadesOut(BaseModel):
    """Retorno de uma atividade de estudo."""
    id_atividade: int
    id_curso: int
    descricao_atividade: str
    estudo_concluido: bool
    revisao_finalizada: bool
    class Config:
        from_attributes = True
