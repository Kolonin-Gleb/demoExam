from sqlmodel import SQLModel, Field, create_engine, Session, select


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str
    password: str


postgresql_url = "postgresql://root:password@localhost:5432/vote_db"
engine = create_engine(postgresql_url, echo=True)
SQLModel.metadata.create_all(engine)


def create_user(name: str, password: 'str'):
    user = User(name=name, password=password)
    with Session(engine) as session:
        session.add(user)
        session.commit()


def get_user():
    with Session(engine) as session:
        user = select(User)
        result = session.exec(user)
        return result


print(get_user())
