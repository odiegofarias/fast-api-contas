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

    novo_fornecedor = {
        'nome': 'BBG TELECOM'
    }

    client.post('/fornecedor-cliente', json=novo_fornecedor)

    nova_conta_1 = {
        "descricao": "Curso de Python",
        "valor": 1350.99,
        "tipo": "PAGAR",
        "fornecedor_cliente_id": 1
    }

    response = client.post('/contas-a-pagar-e-receber', json=nova_conta_1)

    assert response.status_code == 201
    assert response.json() == {'id': 1, 'descricao': 'Curso de Python', 'valor': '1350.9900000000', 'tipo': 'PAGAR', 'fornecedor': {'id': 1, 'nome': 'BBG TELECOM'}}


