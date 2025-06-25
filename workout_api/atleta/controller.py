from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, status, Body, HTTPException, Query, Depends
from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from starlette.responses import JSONResponse
from workout_api import AtletaModel, CategoriaModel, CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaResumo
from fastapi_pagination import Page, paginate

router = APIRouter()

@router.post(path='/',summary='Criar novo atleta', status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DataBaseDependency, atleta_in:AtletaIn = Body(...)):
    categoria_name = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))).scalars().first()
    if not categoria:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = f'fCategoria {categoria_name} não foi encontrada')

    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'fCentro de treinamento {centro_treinamento_nome} não foi encontrado')

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id= centro_treinamento.pk_id
        try:
            db_session.add(atleta_model)
            await db_session.commit()
        except IntegrityError as e:
            await db_session.rollback()
            if 'cpf' in str(e.orig).lower():
                return JSONResponse(status_code=303, content={
                                    'detail':f'Cpf {atleta_in.cpf} já se encontra cadastrado no sistema'}
                                    )
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Erro de integridade no banco de dados')
    except Exception as e:
        print(f'erro:{e}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Ocorreu um erro ao inserir os dados no banco')
    return atleta_out

@router.get(
    path='/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaResumo]
)
async def query(
    db_session: DataBaseDependency,
    nome: str = Query(None),
    cpf: str = Query(None)
):
    query = select(AtletaModel).join(AtletaModel.categoria).join(AtletaModel.centro_treinamento)

    if nome:
        query = query.filter(func.lower(AtletaModel.nome).like(f"%{nome.lower()}%"))
    if cpf:
        query = query.filter(AtletaModel.cpf == cpf)

    result = (await db_session.execute(query)).scalars().all()

    atletas_resumo = [
        AtletaResumo(
            nome=atleta.nome,
            categoria=atleta.categoria.nome,
            centro_treinamento=atleta.centro_treinamento.nome
        )
        for atleta in result
    ]

    return paginate(atletas_resumo)

@router.get(path='/{id}', summary='Consultar atleta pelo id', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def get(id_atleta: UUID4, db_session: DataBaseDependency)->AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id_atleta))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe atleta relacionado a esse id{id}')
    return atleta

@router.patch(path='/{id}', summary='Consultar atleta pelo id', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def get(id_atleta: UUID4, db_session: DataBaseDependency, atleta_up:AtletaUpdate = Body(...))->AtletaOut:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id_atleta))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe atleta relacionado a esse id{id}')
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(path='/{id}', summary='Deletar atleta pelo id', status_code=status.HTTP_204_NO_CONTENT)
async def get(id_atleta: UUID4, db_session: DataBaseDependency)->None:
    atleta: AtletaOut = (await db_session.execute(select(AtletaModel).filter_by(id=id_atleta))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe atleta relacionado a esse id{id}')
    await db_session.delete(atleta)
    await db_session.commit()



