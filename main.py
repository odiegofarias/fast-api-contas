from fastapi import FastAPI
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler


app = FastAPI()


@app.get('')
def root() -> str:
    return {'message': 'Teste'}


app.include_router(contas_a_pagar_e_receber_router.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

