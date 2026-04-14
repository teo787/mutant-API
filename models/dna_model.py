from sqlmodel import SQLModel, Field

class DNA(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    dna: str = Field(unique=True, index=True)
    is_mutant: bool = Field(default=False)