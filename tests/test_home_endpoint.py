import pytest
import aiohttp
import time


@pytest.mark.asyncio
async def test_homepage():
    """This test assumes that the PetStore API service is running"""

    # Give some time to the app to start up
    time.sleep(2)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://0.0.0.0:8000/") as response:
            assert response.status == 200
