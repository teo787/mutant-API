import pytest

@pytest.mark.asyncio
async def test_mutant_endpoint_true(client):
    response=await client.post("/mutant/", json={
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    })

    assert response.status_code==200
    assert response.json()["is_mutant"] is True


@pytest.mark.asyncio
async def test_mutant_endpoint_false(client):
    response = await client.post("/mutant/", json={
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATTT",
            "AGACGG",
            "GCGTCA",
            "TCACTG"
        ]
    })

    assert response.status_code == 403
    assert response.json()["is_mutant"] is False