from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categoria
from workout_api.centro_treinamento.controller import router as centro_treinamento
from fastapi_pagination import add_pagination

api_router = APIRouter()
api_router.include_router(atleta, prefix='/atletas', tags=['atletas'])
api_router.include_router(categoria, prefix='/categoria', tags=['categorias'])
api_router.include_router(centro_treinamento, prefix='/centro_treinamento', tags=['centro_treinamentos'])
api_router = add_pagination(api_router)



