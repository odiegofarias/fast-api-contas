from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List
from contas_a_pagar_e_receber.models.fornecedor_cliente_model import FornecedorCliente

from sqlalchemy.orm import Session

from shared.dependencies import get_db


router = APIRouter(prefix='/fornecedor-cliente')

class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


class FornecedorClienteResponse(BaseModel):
    nome: str = Field(min_length=3, max_length=255)


@router.get('', response_model = List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).offset(skip).limit(limit).all()