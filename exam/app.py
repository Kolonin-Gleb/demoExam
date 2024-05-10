# Тут код для генерации токенов для Авторизации
from fastapi import FastAPI, HTTPException, Request
from models import User, Vote, engine
from sqlmodel import Session, select
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi.staticfiles import StaticFiles

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "6ad196420b42472d0e7d6ef4aca0600c71543272401309c46e8f46babc603bfd"
# f713d3a591e4531b9a53b39cc79acf7a8bc7e92ace43407479ef89a852a7e7c2 ???
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

app.mount("/modeldoc", StaticFiles(directory="html\\app", html=True))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post('/user/')
async def create_user(name, pswd):
    user = User(name=name, password=pswd)
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

@app.get('/user/')
async def get_users():
    with Session(engine) as session:
        user = select(User)
        result = session.exec(user).all()
        return result

@app.post('/vote/', tags=["Vote"])
async def create_vote(name, id_user):
    vote = Vote(name=name, id_user=id_user)
    with Session(engine) as session:
        session.add(vote)
        session.commit()
        session.refresh(vote)
    return vote

@app.get('/vote/', tags=["Vote"])
async def get_votes():
    with Session(engine) as session:
        vote = select(Vote)
        result = session.exec(vote).all()
        return result

@app.get('/vote/{id_user}', tags=["Vote"])
async def get_vote_by_user(id: int):
    with Session(engine) as session:
        user = select(Vote).where(Vote.id_user == id)
        result = session.exec(user).one()
        return result

@app.put('/vote/', tags=["Vote"])
async def voting(name : str, id_user: int):
    try:
        with Session(engine) as session:
            statement = select(Vote).where(Vote.name == name, Vote.id_user == id_user, Vote.state == True)
            results = session.exec(statement)
            vote = results.one()
            # print("Vote:", vote)

            vote.voting_amount += 1
            session.add(vote)
            session.commit()
            session.refresh(vote)
            # print("Updated vote:", vote)
            return vote
    
    except: raise HTTPException(status_code=404, detail="Item not found")

@app.put('/vote/result', tags=["Vote"])
async def close_voting(id : str):
    with Session(engine) as session:
        statement = select(Vote).where(Vote.id == id, Vote.state == True)
        results = session.exec(statement)
        vote = results.one()

        vote.state = False
        session.add(vote)
        session.commit()
        session.refresh(vote)
        return vote

