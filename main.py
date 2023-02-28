import os
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from neo4j import GraphDatabase
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

uri = os.getenv("uri")
user = os.getenv("user")
pwd = os.getenv("pwd")

print(uri,user,pwd)
class LogDetails(BaseModel):
    userName: str
    password: str


def connection():
    driver = GraphDatabase.driver(uri=uri, auth=(user,pwd))
    return driver

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login_request(user_details:LogDetails):
    return user_details

@app.get("/count")
def get_node_count(name):
    driver_neo4j = connection()
    session = driver_neo4j.session()
    q1 = """
    match(s:Shop), (u:User) where u.name=$a return u
    """
    x = {"a": name}
    result = session.run(q1, x)

    return {"response":result}