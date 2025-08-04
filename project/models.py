from sqlmodel import SQLModel, Field, Relationship


# API models


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: None | int = Field(default=None)
    team_id: None | int = Field(default=None)


# ORM models


class Team(SQLModel, table=True):
    id: None | int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")


class Hero(HeroCreate, table=True):
    id: None | int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: None | int = Field(default=None, index=True)

    team_id: None | int = Field(default=None, foreign_key="team.id")
    team: None | Team = Relationship(back_populates="heroes")
