from getgauge.python import step 
from selenium import webdriver
import requests

base_url = "https://reqres.in/"
#driver = webdriver.Chrome()

headers = {
    "x-api-key": "reqres-free-v1"
}

@step("Test response status code")
def endpoint_response():
    r = requests.get(base_url + "api/users?page=2")
    print(r.status_code)
   # driver.get(base_url)
    assert "page" in r.json()
    assert r.status_code == 200


@step("Create new user")
def create_user():
    payload = {
        "name": "Sen",
        "job": "QA"
    }
    r = requests.post(base_url + "api/users", json=payload, headers=headers)
    data = r.json()
    print(data)
    print(r.status_code)

    assert data["name"] == "Sen"
    assert "id" in data
    assert r.status_code == 201

@step("Delete a user")
def delete_user():
    r = requests.delete(base_url + "api/2", headers=headers)
    print(r.status_code)

    assert r.status_code == 204

@step("Successful login")
def success_login():
    creds = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    r = requests.post(base_url + "api/register", json=creds, headers=headers)

    assert r.status_code == 200
    assert "id" and "token" in r.json()
    

@step("Unsuccessful login")
def failed_login():
    r = requests.post(base_url + "api/login", json={"email": "sen@hayag"}, headers=headers)
    print(r.json())

    assert "error" in r.json()
    assert r.json()['error'] == "Missing password"

@step("Check response of unknown user")
def not_found():
    r = requests.get(base_url + "api/unknown/23", headers=headers)
    
    assert r.status_code == 404

@step("Verify a user's data")
def verify_data():
    r = requests.get(base_url + "api/unknown/2", headers=headers)
    data = r.json()
    print(len(data))
    print(data)
    print(data['data'])

    assert r.status_code == 200
    assert len(data) == 2
    assert "support" in data
    assert data['data']['id'] == 2
    assert data['data']['year'] == 2001

@step("Test patch")
def patch_test():
    r = requests.patch(base_url + "api/users/2", headers=headers, json={"name": "Sen"})
    data = r.json()

    assert r.status_code == 200
    assert data['name'] == "Sen"

@step("User not found")
def not_found():
    r = requests.get(base_url+"api/users/23", headers=headers)
    
    assert r.status_code == 404