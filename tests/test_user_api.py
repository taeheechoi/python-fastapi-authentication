import pytest
from fastapi.testclient import TestClient
from main import app
import pdb 

client = TestClient(app)

@pytest.fixture
def authorization_headers():
    return {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiTXkgVGVzdCIsInVzZXJfZW1haWwiOiJteXRlc3RAbXl0ZXN0LmNvbSIsInJvbGUiOiJhZG1pbiIsImV4cGlyZXMiOjE2ODk2OTUwMjQuNDc0NjgyNn0.iou2Tj4M5a7YyjTvQ0qxgrNKSBnfD6ih3rAf0AvO9r8'
    }


@pytest.fixture
def sign_up_info():
    return {
        'fullname': 'Test Chizi',
        'email': 'tetchizik@gmail.com',
        'password': 'ChiziKarogwaTena',
        'role': 'admin'
    }


@pytest.fixture
def sample_update_payload():
    return {
        'fullname': 'Updated mytest3',
        'email': 'mytest3@mytest.com',
        'password': 'this is an updated field',
        'role': 'user'
    }


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok 👍 '} 

# this test will fail is user with the same email as in the test file is already registered
def test_user_creation(sign_up_info):
    response = client.post('/signup/', json=sign_up_info)

    assert response.status_code == 201


def test_user_login(sign_up_info):
    response = client.post('/login/', json={'email': sign_up_info['email'], 'password': sign_up_info['password']})
   
    assert response.status_code == 200
    assert response is not None
    assert 'access_token' in response.json()
    assert response.json()['access_token'] != ''


def test_get_users(authorization_headers):
    response = client.get('/users/', headers=authorization_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for element in response.json():
        assert isinstance(element, dict)
        assert all(key in element for key in ['id', 'fullname', 'email', 'role', 'date', 'time'])


# this test will fail is the user with the id is not found in the database
def test_update_users(authorization_headers, sample_update_payload):
    user_id = 4 # this could be any user id existing in the database
    response = client.put(f'/users/{user_id}', headers=authorization_headers, json=sample_update_payload)
    assert response.status_code == 200

    expected_elements = {
        'id': user_id,
        **sample_update_payload
        }
    # pdb.set_trace() 
    response_json = response.json()
    # assert all(key in response_json for key in expected_elements)

    for key, value in expected_elements.items():
        if key in ['id', 'fullname', 'email', 'role', 'date', 'time']:
            assert response_json[key] == value


# # this test will fail is the user with the user_id is not found in the database
def test_delete_user(authorization_headers):
    user_id = 6 # this could be any user id existing in the database
    response = client.delete(f'/users/{user_id}', headers=authorization_headers)
    assert response.status_code == 200
    assert response.json() == {'status': 'Success', 'message': 'User deleted successfully'}