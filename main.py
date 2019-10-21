from typing import List

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from user import User
from auth import Auth
from database import Database

# App and Database
app = FastAPI()
database = Database()
auth = Auth()

# CORS Policy Configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Used for get jwt token from request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# @app.post("/users")
# def save_user(user: User):
#     _user = database.getUser(user)
#     if not _user:
#         database.saveUser(user)    
#     return _user

# @app.get("/api/users")
# def get_user():
#     users = database.getUsers()
#     return users

@app.get("/api/public")
def public():
    response = "Hello from a public endpoint! You don't need to be authenticated to see this."
    return response

# This needs authentication
@app.get("/api/private")
def private(token: str = Depends(oauth2_scheme)):
    if auth.verify_jwt_token(token) is None:
        return
    response = "Hello from a private endpoint! You need to be authenticated to see this."
    return response

# This needs authorization
@app.get("/api/private-scoped")
def private_scoped(token: str = Depends(oauth2_scheme)):
    if auth.verify_jwt_token(token) is None:
        return
    if auth.requires_scope("create:messages", token):
        response = "Hello from a private endpoint!",
        "You need to be authenticated and have a scope of create:messages to see this."
        return response
    raise HTTPException(403, "You don't have access to this resource")

# The user resources fetched through JWT
@app.get("/api/resources")
def resource(token: str = Depends(oauth2_scheme)):
    payload = auth.verify_jwt_token(token)
    if payload == None or not (len(payload) > 0):
        return "Empty Payload"

    user_id = payload["sub"].split("|")[1]

    resources = database.getResourcesOfUser(user_id)
    return resources

# Add new resources to user through JWT
@app.post("/api/resources/")
def resource(keyword: str = None, token: str = Depends(oauth2_scheme)):
    payload = auth.verify_jwt_token(token)
    if payload == None or not (len(payload) > 0):
        return "Empty Payload"

    user_id = payload["sub"].split("|")[1]
    database.addResourcesToUser(user_id, keyword)
    return "Success"

# The user infos fetched from JWT and also /{user_id}
@app.get("/api/private/{user_id}")
def private(user_id: str, token: str = Depends(oauth2_scheme)):
    payload = auth.verify_jwt_token(token)
    if payload == None or not (len(payload) > 0):
        return "Empty Payload"

    user_id_payload = payload["sub"].split("|")[1]

    if(user_id == user_id_payload):
        resources = database.getResourcesOfUser(user_id)
    else:
        resources = "You are trying to access resources of another user!"

    return resources

# The user infos fetched from JWT and also query parameter
@app.get("/api/private-resources")
def request_resources(user_id: str, token: str = Depends(oauth2_scheme)):
    payload = auth.verify_jwt_token(token)
    if payload == None or not (len(payload) > 0):
        return "Empty Payload"

    user_id_payload = payload["sub"].split("|")[1]

    if(user_id == user_id_payload):
        resources = database.getResourcesOfUser(user_id)
    else:
        resources = "You are trying to access resources of another user!"

    return resources
