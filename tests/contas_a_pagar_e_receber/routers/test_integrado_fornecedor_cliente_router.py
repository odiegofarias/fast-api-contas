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

    novo_fornecedor_cliente = {
        "nome": "CELPE"
    }    
    
    novo_fornecedor_cliente_copy = novo_fornecedor_cliente.copy()
    novo_fornecedor_cliente_copy['id'] = 1

    response = client.post('/fornecedor-cliente', json=novo_fornecedor_cliente)

    assert response.status_code == 201
    assert response.json() == novo_fornecedor_cliente_copy

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
    
    assert response_delete.status_code == 204
    
    response_get = client.get('/fornecedor-cliente')
 
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

def test_deve_retornar_erro_quando_o_nome_for_menor_que_3_ou_maior_que_255():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post1 = client.post('/fornecedor-cliente', json={'nome': 'cu'})

    data_json_maior_que_255 = 60 * 'teste'
    response_post2 = client.post('/fornecedor-cliente', json={'nome': data_json_maior_que_255})

    assert response_post1.status_code == 422
    assert response_post2.status_code == 422
    assert response_post1.json()['detail'][0]['msg'] == 'String should have at least 3 characters'
    assert response_post2.json()['detail'][0]['msg'] == 'String should have at most 255 characters'

def test_deve_retornar_nao_encontrado_para_id_inexistente_no_get_detail():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get('/fornecedor-cliente/999')

    assert response.status_code == 404
    assert response.json() == {'message': 'Oops! Fornecedor-cliente não encontrado(a).'}

def test_deve_retornar_nao_encontrado_para_id_inexistente_no_put():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.put('/fornecedor-cliente/999', json={'nome': 'TESTE_PUT'})

    assert response.status_code == 404
    assert response.json() == {'message': 'Oops! Fornecedor-cliente não encontrado(a).'}

def test_deve_retornar_nao_encontrado_para_id_inexistente_no_delete():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.delete('/fornecedor-cliente/999')

    assert response.status_code == 404
    assert response.json() == {'message': 'Oops! Fornecedor-cliente não encontrado(a).'}