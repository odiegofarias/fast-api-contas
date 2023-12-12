from fastapi.testclient import TestClient
from sqlalchemy import create_engine
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


def test_deve_criar_funcionario_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/fornecedor-cliente', json={
        'nome': 'CELPE'
    })

    assert response.status_code == 201
    assert response.json()['id'] == 1
    assert response.json() == {'id': 1, 'nome': 'CELPE'}

def test_deve_listar_fornecedores_clientes():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/fornecedor-cliente', json={
        'nome': 'BBG TELECOM'
    })

    client.post('/fornecedor-cliente', json={
        'nome': 'TIM SA'
    })

    response = client.get('/fornecedor-cliente')

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == [
        {'id': 1, 'nome': 'BBG TELECOM'},
        {'id': 2, 'nome': 'TIM SA'}
    ]

def test_deve_atualizar_fornecedor_cliente_corretamente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    data_json = {
        'nome': 'VIVO SA'
    }

    response_post = client.post('/fornecedor-cliente', json=data_json)

    id_fornecedor_cliente = response_post.json()['id']

    response_put = client.put(f'/fornecedor-cliente/{id_fornecedor_cliente}', json={
        'nome': 'BBG TELECOM'
    })

    assert response_put.status_code == 200
    assert response_put.json()['nome'] == 'BBG TELECOM'

def test_deve_remover_fornecedor_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    data_json = {'nome': 'VIVO SA'}

    response_post = client.post('/fornecedor-cliente', json=data_json)

    id_fornecedor_cliente = response_post.json()['id']

    response_delete = client.delete(f'/fornecedor-cliente/{id_fornecedor_cliente}')

    response_get = client.get('/fornecedor-cliente')
    assert response_delete.status_code == 204
    assert response_get.json() == []


def test_exibe_detalhe_do_funcionario_cliente():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    data_json = {'nome': 'TESTE'}

    response_post = client.post('/fornecedor-cliente', json=data_json)

    id_fornecedor_cliente = response_post.json()['id']

    response_get = client.get(f'/fornecedor-cliente/{id_fornecedor_cliente}')

    assert response_get.status_code == 200
    assert response_get.json()['nome'] == 'TESTE'
    assert response_get.json() == {'id': 1, 'nome': 'TESTE'}