from fastapi import APIRouter, Depends
from typing import List
from contas_a_pagar_e_receber.models.contas_pagar_receber_models import ContaPagarReceber

from sqlalchemy.orm import Session
from contas_a_pagar_e_receber.routers.contas_a_pagar_e_receber_router import ContaPagarReceberResponse
from shared.dependencies import get_db


router = APIRouter(prefix='/fornecedor-cliente')


@router.get('/{id}/contas-a-pagar-e-receber', response_model=List[ContaPagarReceberResponse], status_code=200)
def detalhe_fornecedor_cliente(id: int, db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).filter_by(fornecedor_cliente_id=id).all()