from fastapi import FastAPI
from models import User, engine
from sqlmodel import Session, select


app = FastAPI()


@app.get('/user/')
def get_users():
    with Session(engine) as session:
        user = select(User)
        result = session.exec(user).all()
        return result


@app.get('/user/{id}')
def get_user_by_id(id: int):
    with Session(engine) as session:
        user = select(User).where(User.id == id)
        result = session.exec(user).one()
        return result


@app.post('/user/')
def create_user(name, pswd):
    user = User(name=name, password=pswd)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# Тут София реализовала нужные пользовательские команды
# Она планирует поделиться этим в инструкции


