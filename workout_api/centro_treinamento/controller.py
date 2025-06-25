from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from sqlalchemy.future import select

router = APIRouter()

@router.post(path='/',
             summary='Criar um novo CT',
             status_code=status.HTTP_201_CREATED,
             response_model=CentroTreinamentoOut
             )
async def post(db_session: DataBaseDependency, ct_in :CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    ct_out = CentroTreinamentoOut(id=uuid4(), **ct_in.model_dump())
    ct_model = CentroTreinamentoModel(**ct_out.model_dump())
    db_session.add(ct_model)
    await db_session.commit()
    return ct_out

@router.get(path='/',
            summary='Consultar todos os centros de treinamentos',
            status_code=status.HTTP_200_OK,
            response_model=list[CentroTreinamentoOut]
            )
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centro_treinamentos: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return centro_treinamentos

@router.get(path='/{id}',
            summary='Consultar CT pelo id',
            status_code=status.HTTP_200_OK,
            response_model=CentroTreinamentoOut)
async def get(id_ct: UUID4, db_session: DataBaseDependency) -> CentroTreinamentoOut:
    ct: CentroTreinamentoOut = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id_ct))).scalars().first()
    if not ct:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'CT não encontrado no id{id}')
    return ct

