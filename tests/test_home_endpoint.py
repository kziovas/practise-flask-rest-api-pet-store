import pytest
import aiohttp


@pytest.mark.asyncio
async def test_homepage():
    """This test assumes that the PetStore API service is running"""

    async with aiohttp.ClientSession() as session:
        async with session.get("http://localhost:8000/") as response:
            assert response.status == 200
