from fastapi import APIRouter, status, Depends, Request
from fastapi.responses import JSONResponse
from db.db import SessionDep
from models.dna_model import DNA
from sqlmodel import select, func
from services.dna_service import isMutant
from schemas.dna_schema import DnaCreate
import json
from core.cache import CacheService, get_cache
from core.rate_limit import limiter

router=APIRouter()

@router.post("/mutant/")
@limiter.limit("10/minute")
async def isMutantAnalyze(dna: DnaCreate, request: Request, session: SessionDep, cache: CacheService = Depends(get_cache)):
    dna_string = json.dumps(dna.dna)
    CACHE_KEY = f"dna:{dna_string}"

    cached = await cache.get(CACHE_KEY)
    if cached is not None:
        return JSONResponse(cached, status_code=200 if cached["is_mutant"] else 403)

    dna_db = session.exec(select(DNA).where(DNA.dna == dna_string)).first()

    if not dna_db:
        analysis = isMutant(dna.dna)
        dna_new = DNA(dna=dna_string, is_mutant=analysis)
        session.add(dna_new)
        session.commit()

        result = {"is_mutant": analysis}

        await cache.set(CACHE_KEY, result, ttl=300)

        await cache.delete("stats:dna")

        return JSONResponse(result, status_code=200 if analysis else 403)

    result = {"is_mutant": dna_db.is_mutant}

    await cache.set(CACHE_KEY, result, ttl=300)

    return JSONResponse(result, status_code=200 if dna_db.is_mutant else 403)


@router.get("/stats/")
@limiter.limit("10/minute")
async def stats(session: SessionDep, request: Request, cache: CacheService = Depends(get_cache)):    
    CACHE_KEY = "stats:dna"
    CACHE_TTL = 30

    cached = await cache.get(CACHE_KEY)
    if cached is not None:
        return JSONResponse(cached, status_code=status.HTTP_200_OK)

    total_humans = session.exec(select(func.count(DNA.id))).one()
    total_mutants = session.exec(select(func.count(DNA.id)).where(DNA.is_mutant == True)).one()
    ratio = total_mutants / total_humans if total_humans > 0 else 0

    data = {
        "count_mutant_dna": total_mutants,
        "count_humans_dna": total_humans,
        "ratio": ratio,
    }

    await cache.set(CACHE_KEY, data, ttl=CACHE_TTL)

    return JSONResponse(data, status_code=status.HTTP_200_OK)