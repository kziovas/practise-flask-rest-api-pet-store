import pytest
import aiohttp
import time


@pytest.mark.asyncio
async def test_homepage():
    """This test assumes that the PetStore API service is running"""

    # Give some time to the app to start up
    time.sleep(4)

    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/") as response:
            assert response.status == 200
