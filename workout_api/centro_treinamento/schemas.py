from typing import Annotated
from pydantic import Field, UUID4
from workout_api.contrib.schemas import BaseSchema

class CentroTreinamento(BaseSchema):
     nome: Annotated[str, Field(description="Nome do centro de treinamento", examples=["CT king"], max_length=20)]
     endereco: Annotated[str, Field(description="Endereço do CT", examples=["Rua X, Q02"], max_length=60)]
     proprietario: Annotated[str, Field(description="Nome do proprietario do CT", examples=['Raul'], max_length=30)]

class CentroTreinamentoIn(CentroTreinamento):
     pass

class CentroTreinamentoAtleta(BaseSchema):
     nome: Annotated[str, Field(description='Nome do centro de treinamento', examples=['CT King'], max_length=20)]

class CentroTreinamentoOut(CentroTreinamentoIn):
     id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]