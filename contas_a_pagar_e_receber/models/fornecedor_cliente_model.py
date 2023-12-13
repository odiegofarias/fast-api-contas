from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from shared.database import Base


class FornecedorCliente(Base):
    __tablename__ = "fornecedor_cliente"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255))

    # Caso precise acessar as contas com base no fornecedor
    #   conta_a_pagar_e_receber = relationship("ContaPagarReceber")