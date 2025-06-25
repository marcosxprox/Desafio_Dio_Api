from typing import Annotated, Optional
from pydantic import Field
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin


class Atleta(BaseSchema):

    nome: Annotated[str, Field(description="Nome atleta", examples=["Marcos", "Stephanie"], max_length=50)]
    cpf: Annotated[str, Field(description="cpf atleta", examples=["01234567890"], max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", examples=[25, 30])]
    peso: Annotated[float, Field(description="Peso do Atleta", examples=[75.5, 80.0], gt=0)]
    altura: Annotated[float, Field(description="Altura do atleta", examples=[1.80, 1.70], gt=0)]
    sexo: Annotated[str, Field(description="Genero do atleta", examples=["M", "F"], max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]


class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome atleta", examples=["Marcos", "Stephanie"], max_length=50)]
    idade: Annotated[Optional[int], Field(None, description="Idade do atleta", examples=[25, 30])]

class AtletaResumo(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description="Nome atleta", examples=["Marcos", "Stephanie"], max_length=50)]
    centro_treinamento: Annotated[Optional[str], Field(description='Centro de treinamento do atleta')]
    categoria: Annotated[Optional[str], Field(description='categoria do atleta')]
