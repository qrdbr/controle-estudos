from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.control import (
    TrilhaCreate, TrilhaUpdate, TrilhaOut,
    CursoCreate, CursoUpdate, CursoOut,
    AtividadesCreate, AtividadesUpdate, AtividadesOut
)
from app.services.control_service import ControlService

router = APIRouter()
service = ControlService()

# --- Trilhas ---
@router.post("/trilhas", response_model=TrilhaOut, status_code=status.HTTP_201_CREATED, summary="Criar trilha", tags=["Trilhas"])
def create_trilha(trilha: TrilhaCreate):
    """Cria uma nova trilha."""
    id_trilha = service.create_trilha(trilha.descricao_trilha)
    return TrilhaOut(id_trilha=id_trilha, descricao_trilha=trilha.descricao_trilha)

@router.get("/trilhas", response_model=List[TrilhaOut], summary="Listar trilhas", tags=["Trilhas"])
def list_trilhas():
    """Lista todas as trilhas."""
    trilhas = service.list_trilhas()
    return [TrilhaOut(**t) for t in trilhas]

@router.get("/trilhas/{id_trilha}", response_model=TrilhaOut, summary="Obter trilha por ID", tags=["Trilhas"])
def get_trilha(id_trilha: int):
    """Obtém uma trilha pelo ID."""
    trilha = service.get_trilha_by_id(id_trilha)
    if not trilha:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trilha não encontrada")
    return TrilhaOut(**trilha)

@router.put("/trilhas/{id_trilha}", response_model=TrilhaOut, summary="Atualizar trilha", tags=["Trilhas"])
def update_trilha(id_trilha: int, trilha_update: TrilhaUpdate):
    """Atualiza uma trilha."""
    success = service.update_trilha(id_trilha, trilha_update.descricao_trilha)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trilha não encontrada")
    updated = service.get_trilha_by_id(id_trilha)
    return TrilhaOut(**updated)

@router.delete("/trilhas/{id_trilha}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletar trilha", tags=["Trilhas"])
def delete_trilha(id_trilha: int):
    """Deleta uma trilha."""
    success = service.delete_trilha(id_trilha)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trilha não encontrada")

# --- Cursos ---
@router.post("/cursos", response_model=CursoOut, status_code=status.HTTP_201_CREATED, summary="Criar curso", tags=["Cursos"])
def create_curso(curso: CursoCreate):
    """Cria um novo curso."""
    id_curso = service.create_curso(curso.descricao_curso, curso.id_trilha)
    if id_curso is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Trilha não encontrada")
    return CursoOut(id_curso=id_curso, id_trilha=curso.id_trilha, descricao_curso=curso.descricao_curso)

@router.get("/cursos", response_model=List[CursoOut], summary="Listar cursos", tags=["Cursos"])
def list_cursos():
    """Lista todos os cursos."""
    cursos = service.list_cursos()
    return [CursoOut(**c) for c in cursos]

@router.get("/cursos/{id_curso}", response_model=CursoOut, summary="Obter curso por ID", tags=["Cursos"])
def get_curso(id_curso: int):
    """Obtém um curso pelo ID."""
    curso = service.get_curso_by_id(id_curso)
    if not curso:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    return CursoOut(**curso)

@router.put("/cursos/{id_curso}", response_model=CursoOut, summary="Atualizar curso", tags=["Cursos"])
def update_curso(id_curso: int, curso_update: CursoUpdate):
    """Atualiza um curso."""
    success = service.update_curso(id_curso, curso_update.descricao_curso, curso_update.id_trilha)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso ou trilha não encontrada")
    updated = service.get_curso_by_id(id_curso)
    return CursoOut(**updated)

@router.delete("/cursos/{id_curso}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletar curso", tags=["Cursos"])
def delete_curso(id_curso: int):
    """Deleta um curso."""
    success = service.delete_curso(id_curso)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

# --- Atividades ---
@router.post("/atividades", response_model=AtividadesOut, status_code=status.HTTP_201_CREATED, summary="Criar atividade", tags=["Atividades"])
def create_atividade(atividade: AtividadesCreate):
    """Cria uma nova atividade."""
    id_atividade = service.create_atividade(atividade.descricao_atividade, atividade.id_curso)
    if id_atividade is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Curso não encontrado")
    return AtividadesOut(
        id_atividade=id_atividade,
        id_curso=atividade.id_curso,
        descricao_atividade=atividade.descricao_atividade,
        estudo_concluido=False,
        revisao_finalizada=False
    )

@router.get("/atividades", response_model=List[AtividadesOut], summary="Listar atividades", tags=["Atividades"])
def list_atividades():
    """Lista todas as atividades."""
    atividades = service.list_atividades()
    return [AtividadesOut(**a) for a in atividades]

@router.get("/atividades/{id_atividade}", response_model=AtividadesOut, summary="Obter atividade por ID", tags=["Atividades"])
def get_atividade(id_atividade: int):
    """Obtém uma atividade pelo ID."""
    atividade = service.get_atividade_by_id(id_atividade)
    if not atividade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atividade não encontrada")
    return AtividadesOut(**atividade)

@router.put("/atividades/{id_atividade}", response_model=AtividadesOut, summary="Atualizar atividade", tags=["Atividades"])
def update_atividade(id_atividade: int, atividade_update: AtividadesUpdate):
    """Atualiza uma atividade."""
    success = service.update_atividade(
        id_atividade,
        atividade_update.descricao_atividade,
        atividade_update.id_curso,
        atividade_update.estudo_concluido,
        atividade_update.revisao_finalizada
    )
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atividade ou curso não encontrada")
    updated = service.get_atividade_by_id(id_atividade)
    return AtividadesOut(**updated)

@router.delete("/atividades/{id_atividade}", status_code=status.HTTP_204_NO_CONTENT, summary="Deletar atividade", tags=["Atividades"])
def delete_atividade(id_atividade: int):
    """Deleta uma atividade."""
    success = service.delete_atividade(id_atividade)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atividade não encontrada")