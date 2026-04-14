import pytest

@pytest.mark.asyncio
async def test_stats(client):
    await client.post("/mutant/", json={
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    })

    await client.post("/mutant/", json={
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATTT",
            "AGACGG",
            "GCGTCA",
            "TCACTG"
        ]
    })

    response = await client.get("/stats/")
    data = response.json()

    assert response.status_code == 200
    assert data["count_mutant_dna"] == 1
    assert data["count_humans_dna"] == 2