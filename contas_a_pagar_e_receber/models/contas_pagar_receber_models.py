from shared.database import Base
from sqlalchemy import Column, Integer, Numeric, String


class ContaPagarReceber(Base):
    __tablename__ = "contas_a_pagar_e_receber"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(40))
    valor = Column(Numeric)
    tipo = Column(String(10))