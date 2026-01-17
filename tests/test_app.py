from http import HTTPStatus


def test_root_deve_retornar_ola(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá amigos!'}
