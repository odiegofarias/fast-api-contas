from fastapi.testclient import TestClient
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from shared.database import Base
from shared.dependencies import get_db


client = TestClient(app)

SQLALCHEMY_DATABASE_URL = 'sqlite:///sqlite3.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        'check_same_thread': False,
    },
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def test_deve_retornar_as_contas_associadas_a_um_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    novo_fornecedor_1 = {
        'nome': 'BBG TELECOM'
    }
    novo_fornecedor_2 = {
        'nome': 'BBG TELECOM'
    }

    client.post('/fornecedor-cliente', json=novo_fornecedor_1)
    client.post('/fornecedor-cliente', json=novo_fornecedor_2)

    nova_conta_1 = {
        "descricao": "Curso de Python",
        "valor": 1350.99,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1
    }
    nova_conta_2 = {
        "descricao": "Curso de FastAPI",
        "valor": 459.99,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1
    }
    nova_conta_3 = {
        "descricao": "Curso de Investimentos",
        "valor": 997.97,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 2
    }

    response_conta_1 = client.post('/contas-a-pagar-e-receber', json=nova_conta_1)
    response_conta_2 = client.post('/contas-a-pagar-e-receber', json=nova_conta_2)
    response_conta_3 = client.post('/contas-a-pagar-e-receber', json=nova_conta_3)


    response_get = client.get('/fornecedor-cliente/1/contas-a-pagar-e-receber')

    assert response_conta_1.status_code == 201
    assert response_conta_2.status_code == 201
    assert response_conta_3.status_code == 201

    assert response_get.json() == [
            {'id': 1, 'descricao': 'Curso de Python', 'valor': '1350.9900000000', 'tipo': 'PAGAR', 'fornecedor': {'id': 1, 'nome': 'BBG TELECOM'}, 'data_baixa': None, 'valor_baixa': None, 'esta_baixada': False}, 
            {'id': 2, 'descricao': 'Curso de FastAPI', 'valor': '459.9900000000', 'tipo': 'PAGAR', 'fornecedor': {'id': 1, 'nome': 'BBG TELECOM'}, 'data_baixa': None, 'valor_baixa': None, 'esta_baixada': False}
        ]
    assert len(response_get.json()) == 2
    
def test_deve_retornar_lita_vazia_pois_nao_tem_o_fornecedor_nao_tem_contas_vinculadas():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    novo_fornecedor_1 = {
        'nome': 'BMW'
    }

    client.post('/fornecedor-cliente', json=novo_fornecedor_1)

    nova_conta_1 = {
        "descricao": "Curso de Python",
        "valor": 1350.99,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1
    }

    client.post('/contas-a-pagar-e-receber', json=nova_conta_1)

    response = client.get('/fornecedor-cliente/2/contas-a-pagar-e-receber')

    assert response.status_code == 200
    assert response.json() == []




    

