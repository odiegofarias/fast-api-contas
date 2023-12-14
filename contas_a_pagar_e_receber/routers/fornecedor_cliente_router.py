from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import List
from contas_a_pagar_e_receber.models.contas_pagar_receber_models import ContaPagarReceber
from contas_a_pagar_e_receber.models.fornecedor_cliente_model import FornecedorCliente

from sqlalchemy.orm import Session

from shared.dependencies import get_db
from shared.exceptions import NotFound


router = APIRouter(prefix='/fornecedor-cliente')

class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=255)


@router.get('', response_model = List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).offset(skip).limit(limit).all()

@router.get('/{id}', response_model=FornecedorClienteResponse, status_code=200)
def detalhe_fornecedor_cliente(id: int, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    return busca_fornecedor_cliente_por_id(id, db)

@router.post('', response_model=FornecedorClienteResponse, status_code=201)
def criar_fornecedor_cliente(fornecedor_cliente_request: FornecedorClienteRequest, db: Session = Depends(get_db)) -> FornecedorClienteResponse:
    fornecedor_cliente = FornecedorCliente(
        **fornecedor_cliente_request.model_dump()
    )

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente

@router.put('/{id}', response_model=FornecedorClienteResponse, status_code=200)
def atualiza_fornecedor_cliente(
    id: int, fornecedor_cliente_request: FornecedorClienteRequest,
    db: Session = Depends(get_db)
) -> FornecedorClienteResponse:
    fornecedor_cliente = busca_fornecedor_cliente_por_id(id, db)
    fornecedor_cliente.nome = fornecedor_cliente_request.nome

    db.add(fornecedor_cliente)
    db.commit()
    db.refresh(fornecedor_cliente)

    return fornecedor_cliente

@router.delete('/{id}', status_code=204)
def exclui_fornecedor_cliente(id: int, db: Session = Depends(get_db)) -> None:
    fornecedor_cliente = busca_fornecedor_cliente_por_id(id, db)

    db.delete(fornecedor_cliente)
    db.commit()

def busca_fornecedor_cliente_por_id(id_fornecedor_cliente: int, db: Session):
    fornecedor_cliente: FornecedorCliente = db.query(FornecedorCliente).get(id_fornecedor_cliente)

    if fornecedor_cliente is None:
        raise NotFound('Fornecedor-cliente')
    
    return fornecedor_cliente