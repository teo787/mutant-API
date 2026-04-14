from services.dna_service import isMutant

def test_mutant_service():
    dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]

    assert isMutant(dna) is True