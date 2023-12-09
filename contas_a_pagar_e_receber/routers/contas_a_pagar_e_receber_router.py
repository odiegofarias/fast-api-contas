from fastapi import APIRouter


router = APIRouter(prefix='/contas-a-pagar-e-receber')


@router.get('/')
def listar_contas() -> list:
    return [
        {'conta1': 'conta1'},
        {'conta1': 'conta1'},
        {'conta1': 'conta1'},
    ]