from pydantic import BaseModel

class DnaCreate(BaseModel):
    dna: list[str]