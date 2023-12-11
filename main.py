from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router
from shared.exceptions import NotFound


app = FastAPI()


@app.get('')
def root() -> str:
    return {'message': 'Teste'}


app.include_router(contas_a_pagar_e_receber_router.router)


@app.exception_handler(NotFound)
async def unicorn_exception_handler(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"Oops! {exc.name} não encontrado(a)."},
    )