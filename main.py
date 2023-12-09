from fastapi import FastAPI
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
# from shared.database import Base, engine

from contas_a_pagar_e_receber.models.contas_pagar_receber_models import ContaPagarReceber


# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('')
def root() -> str:
    return {'message': 'Teste'}


app.include_router(contas_a_pagar_e_receber_router.router)