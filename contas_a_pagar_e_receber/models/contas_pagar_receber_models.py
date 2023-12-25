from shared.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship


class ContaPagarReceber(Base):
    __tablename__ = "contas_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(40))
    valor = Column(Numeric)
    tipo = Column(String(10))
    data_baixa = Column(DateTime())
    valor_baixa = Column(Numeric)
    esta_baixada = Column(Boolean, default=False)

    fornecedor_cliente_id = mapped_column(ForeignKey("fornecedor_cliente.id"))
    fornecedor = relationship("FornecedorCliente")