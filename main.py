from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Tading App")

db_users = [
    {"id": 1, "role": "admin", "name": "Sherlock"},
    {"id": 2, "role": "investor", "name": "Himeko"},
    {"id": 3, "role": "trader", "name": "Lumin"},
    {"id": 4, "role": "investor", "name": "Tartaglia", "degree": [
        {"id": 1, "created_at": "2020-09-01T00:00:00", "type_degree": "expert"}
    ]}

]

db_users1 = [
    {"id": 1, "role": "admin", "name": "Sherlock"},
    {"id": 2, "role": "investor", "name": "Himeko"},
    {"id": 3, "role": "trader", "name": "Lumin"},

]

db_trades = [
    {"id": 1, "user_id": 1, "currency": "EPH", "side": "buy", "price": 123, "amount": 2.1},
    {"id": 2, "user_id": 1, "currency": "EPH", "side": "sell", "price": 125, "amount": 2.1}
]

# почему-то не работает :/
# @app.exception_handlers(ValidationError) # обработка ошибок валидации и вывод их для клиента
# async def validation_sxception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()})
#     )


@app.get("/")
async def root():
    return {"message": "Hello World"}


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []  # если нет званий, то по дефолту будет пустой список


@app.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: int):
    return [user for user in db_users if user.get("id") == user_id]


@app.get("/trades")
async def get_trades(limit: int = 1, offset: int = 0):
    return db_trades[offset:][:limit]


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/users/{user_id}")
async def change_username(user_id: int, new_name: str):
    curr_user = list(filter(lambda user: user.get("id") - - user_id, db_users1))[0]
    curr_user["name"] = new_name
    return {"status": 200, "data": curr_user}  # 200 - значит все окей


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float = Field(ge=0)


@app.post("/trades")
async def add_trades(trades: List[Trade]):
    db_trades.append(trades)
    return {"status": 200, "data": db_trades}
