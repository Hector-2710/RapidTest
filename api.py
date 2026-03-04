from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends
from typing import Annotated
import uuid

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    id: uuid.UUID
    name: str
    email : str
    age: int
    password: str

users = [User(id="2734e76d-de18-4930-8531-54c39b3abe05", name="caja", email="caja", age=30, password="caja")]

def get_user_db(token: str = Depends(oauth2_scheme)):
    for user in users:
        if user.email == token:
            return user
    return None

# GET
@app.get("/", status_code=status.HTTP_200_OK)
def get_hello():
    return {"message": "Correctly initialized!"}

@app.get("/me", status_code=status.HTTP_200_OK)
def get_user(current_user : Annotated[User, Depends(get_user_db)]):
    return current_user

@app.get("/users", status_code=status.HTTP_200_OK)
def get_users(use_email: str):
    for user in users:
        if user.email == use_email:
            print("User found:", user)
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@app.get("/users/{email}", status_code=status.HTTP_200_OK)
def get_users(email: str):
    for user in users:
        if user.email == email:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# POST
@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    users.append(user)
    return user

@app.post("/token", status_code=status.HTTP_200_OK)
def login(form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    for user in users:
        if user.email == form_data.username and user.password == form_data.password:
            return {"access_token": user.email, "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")  

# PUT
@app.put("/user/{user_id}", status_code=status.HTTP_200_OK)
def update_user(user_id: uuid.UUID, user: User):
    for i, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users[i] = user
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# PATCH
@app.patch("/user/{user_id}", status_code=status.HTTP_200_OK)
def patch_user(user_id: uuid.UUID, age: int):
    for i, existing_user in enumerate(users):
        if existing_user.id == user_id:
            updated_user = existing_user.copy(update={"age": age})
            users[i] = updated_user
            return updated_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

# DELETE
@app.delete("/user/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def delete_user(user_id: uuid.UUID):
    for i, existing_user in enumerate(users):
        if existing_user.id == user_id:
            del users[i]
            return {"message": "User deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")