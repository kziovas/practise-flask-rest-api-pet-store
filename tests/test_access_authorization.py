from wsgiref import headers
import pytest
import aiohttp
import time
from http import HTTPStatus
from faker import Faker

@pytest.mark.asyncio
async def test_unauthorized_request():
    """This test assumes that the PetStore API service is running.
        It makes a GET request without a valid access token in headers.
        The service should return a FORBIDDEN code"""

    # Give some time to the app to start up
    time.sleep(2)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://0.0.0.0:8000/pets/") as response:
            assert response.status == HTTPStatus.FORBIDDEN

@pytest.mark.asyncio
async def test_authorized_request():
    """This test assumes that the PetStore API service is running.
        It first acquires a valid token and then makes a GET request.
        The token is included in the requets headers.
        The service should return an OK code"""

    fake = Faker()
    access_token = ""
    user_name = fake.name()
    user_pass = "Alrighty!"
    user_data = { "USER-ID":user_name, "USER-PASSWORD":user_pass}

    async with aiohttp.ClientSession() as session:

        #Add new user
        async with session.post(url="http://0.0.0.0:8000/users/", json=user_data) as response:
            assert response.status == HTTPStatus.OK 


        #Get access token
        async with session.post(url="http://0.0.0.0:8000/users/access/", json=user_data) as response:
            assert response.status == HTTPStatus.OK 

            response_data = await response.json()
            assert response_data

            access_token = response_data.get("New token created")
            assert access_token

        valid_headers={"USER-ID":user_name,"TOKEN":access_token}
        async with session.get("http://0.0.0.0:8000/pets/", headers=valid_headers) as response:
            assert response.status == HTTPStatus.OK
