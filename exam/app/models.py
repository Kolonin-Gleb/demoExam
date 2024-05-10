from sqlmodel import SQLModel, Field, create_engine, Session, select

class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    user_name: str
    password: str
    disabled: bool | None = None

class Vote(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    voting_amount: int = Field(default = 0)
    state: bool = Field(default = True)
    id_user: int

postgresql_url = "postgresql://root:password@localhost:5432/vote_db"
engine = create_engine(postgresql_url, echo=True)
SQLModel.metadata.create_all(engine)
