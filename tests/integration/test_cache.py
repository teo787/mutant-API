import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_cache_hit(client):
    dna = {
        "dna": [
            "ATGCGA",
            "CAGTGC",
            "TTATGT",
            "AGAAGG",
            "CCCCTA",
            "TCACTG"
        ]
    }

    r1 = await client.post("/mutant/", json=dna)
    r2 = await client.post("/mutant/", json=dna)

    assert r1.json() == r2.json()


@pytest.mark.asyncio
async def test_cache_hit_avoids_recalculation(client):
    dna = {
        "dna": [
            "ATGCGA","CAGTGC","TTATGT",
            "AGAAGG","CCCCTA","TCACTG"
        ]
    }

    await client.post("/mutant/", json=dna)

    with patch("services.dna_service.isMutant") as mock:
        response = await client.post("/mutant/", json=dna)

        mock.assert_not_called()
        assert response.status_code == 200