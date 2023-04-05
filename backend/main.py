import inspect
import math
import os.path
import datetime
from typing import List

from fastapi import FastAPI, Depends, Body, Security, Query
from tortoise import Tortoise
from fastapi import HTTPException
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from fastapi.middleware.cors import CORSMiddleware

import config
from data_model.operation import OperationValue, Operation
from data_model.record import Record, recordOut, recordIn
from data_model.user import User, UserIn, create_user, UserOut, validate_user, get_current_user
import aiohttp

app = FastAPI(title="Arithmetic Calculator", description="LoanPro Arithmetic Calculator", version="0.1.0")
access_security_manager = JwtAccessBearer(
    secret_key=config.AUTH_SEC,
    algorithm=config.AUTH_ALGROR,
    access_expires_delta=datetime.timedelta(hours=1),
    auto_error=True
)
cors_origins = [
    'http://localhost:8080',
    'https://nvkou.dev'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nvkou.dev"], # todo move to env or env depending
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def register_tortoise(app):
    @app.on_event("startup")
    async def startup():
        await Tortoise.init(
            db_url="postgres://dba:qwerasdf@localhost:5432/loanpro",  # todo move to env
            modules={"models": ["data_model.record", "data_model.operation", "data_model.user"]}
        )
        await Tortoise.generate_schemas()

    @app.on_event("shutdown")
    async def shutdown():
        await Tortoise.close_connections()


register_tortoise(app)


@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/login")
async def login(user: UserIn):
    if await validate_user(user):
        token_dic = {"username": user.username}
        return {"token": access_security_manager.create_access_token(token_dic)}
    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/user")
async def get_user(credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    user = await get_current_user(credentials['username'])
    if not user:
        raise HTTPException(status_code=400, detail="user not active")
    last_record = await Record.filter(user=user).order_by('-updated_at').first()
    return {"username": user.username, "balance": last_record.user_balance}


@app.post("/register", response_model=UserOut)
async def register(user: UserIn):
    existing_user = await User.filter(username=user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return await create_user(user)


@app.get("/random")
async def get_random(num: int = 10, len: int = 8, digits: bool = True, upperalpha: bool = True, loweralpha: bool = True,
                     unique: bool = True, format: str = "plain", rnd: str = "new", credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    """
    :param num: quantity of random strings

    :param len: length of each string

    :param digits: allow digits or not

    :param upperalpha: allow upper case letters or not

    :param loweralpha: allow lower case letters or not

    :param unique: stritctly unique or not

    :param format: fixed to plain

    :param rnd: fixed to new

    :return: list of random strings as desired
    """
    digits = 'on' if digits else 'off'
    upperalpha = 'on' if upperalpha else 'off'
    loweralpha = 'on' if loweralpha else 'off'
    unique = 'on' if unique else 'off'
    user = await get_current_user(credentials['username'])
    result = await fetch_random(num=num, len=len, digits=digits, upperalpha=upperalpha,
                              loweralpha=loweralpha, unique=unique, format=format, rnd=rnd)

    await preform_operation(user=user, operation=OperationValue.RANDOM, amount=10, operation_result=result.pop())
    return result


###### operation part  ######

async def fetch_random(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.random.org/strings/", params=kwargs) as response:
            data = await response.text()
            data = data.splitlines()
    return data


@app.get("/add")
async def add(a: str = Query(min_length=1, max_length=100, title="First number", description="First number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              b: str = Query(min_length=1, max_length=100, title="Second number", description="Second number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    return await calculate(float(a), float(b), OperationValue.ADD, credentials)


@app.get("/sub")
async def sub(a: str = Query(min_length=1, max_length=100, title="First number", description="First number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              b: str = Query(min_length=1, max_length=100, title="Second number", description="Second number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    return await calculate(float(a), float(b), OperationValue.SUB, credentials)


@app.get("/mul")
async def mul(a: str = Query(min_length=1, max_length=100, title="First number", description="First number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              b: str = Query(min_length=1, max_length=100, title="Second number", description="Second number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    return await calculate(float(a), float(b), OperationValue.MUL, credentials)


@app.get("/div")
async def div(a: str = Query(min_length=1, max_length=100, title="First number", description="First number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              b: str = Query(min_length=1, max_length=100, title="Second number", description="Second number",
                             regex="^(\-|\+)?\d+(\.\d+)?$"),
              credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    return await calculate(float(a), float(b), OperationValue.DIV, credentials)


@app.get("/sqrt")
async def sqrt(a: str = Query(min_length=1, max_length=100, title="Target number", description="Target number",
                              regex="^(\-|\+)?\d+(\.\d+)?$"),
               credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    return await calculate(float(a), 0, OperationValue.SQRT, credentials)


###### operation part end  ######

###### User Record part  ######
@app.get("/user_records", response_model=List[recordOut])
async def get_user_records(
        page: int = Query(1, ge=1, title="Page number", description="Page number"),
        limit: int = Query(10, ge=1, le=100, title="Page size", description="Page size"),
        operation: OperationValue = Query(None, title="Operation", description="Operation"),
        operation_respond: str = Query(None, title="Operation respond", description="Operation respond"),
        credentials: JwtAuthorizationCredentials = Security(access_security_manager)
):
    """
    login required

    :param page: page number

    :param limit: page size

    :param operation: 1 -> add, 2-> sub, mul, div, sqrt, random, misc

    :param operation_respond: string of operation respond

    :return: list of login user records
    """
    user = await get_current_user(credentials['username'])
    assert user is not None  # possible if token is active but user is deleted
    query = Record.filter(user=user)
    if operation is not None:
        query = query.filter(operation=operation)
    if operation_respond is not None:
        query = query.filter(operation_respond=operation_respond)
    return await query.offset((page - 1) * limit).limit(limit).all().prefetch_related('operation')



@app.delete('/user_records/{record_id}', response_model=recordOut)
async def update_user_record(record_id: int, credentials: JwtAuthorizationCredentials = Security(access_security_manager)):
    """
    even this is delete method, but it is only act for soft delete

    :param record_id:
    :param credentials:
    :return:
    """
    user = await get_current_user(credentials['username'])
    assert user is not None
    record = await Record.filter(id=record_id, user=user).first()
    assert record is not None
    record.soft_delete = True
    await record.save()
    return record


async def calculate(a: float, b: float, operation: OperationValue, credentials: JwtAuthorizationCredentials):
    try:
        user = await get_current_user(credentials['username'])
        assert user is not None  # possible if token is active but user is deleted
        if operation == OperationValue.ADD:
            result = {"result": a + b}
        elif operation == OperationValue.SUB:
            result = {"result": a - b}
        elif operation == OperationValue.MUL:
            result = {"result": a * b}
        elif operation == OperationValue.DIV:
            result = {"result": a / b}
        elif operation == OperationValue.SQRT:
            result = {"result": math.sqrt(a)}
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        await preform_operation(user=user, operation=operation, amount=10.0, operation_result="processed")
    except Exception as e:
        raise e
    return result


async def preform_operation(user: User, operation: OperationValue, amount: float, operation_result: str) -> bool:
    try:
        operation_obj = await Operation.create(cost=amount, operation=operation)
        last_record = await Record.filter(user=user).filter(soft_delete=False).order_by('-updated_at').first()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not last_record:
        await Operation.delete(operation_obj)
        raise HTTPException(status_code=501, detail="User has no records")
    balance = last_record.user_balance
    if balance - amount >= 0:
        new_recored = await Record.create(user=user, amount=amount, user_balance=balance - amount,
                                          operation_respond=operation_result, operation=operation_obj)
        return True
    else:
        operation_obj.operation_respond = "failed"
        operation_obj.cost = 0
        await Operation.save(operation_obj)
        await Record.create(user=user, amount=0, user_balance=balance, operation=operation_obj,
                            operation_respond="failed")
        raise HTTPException(status_code=402, detail="User has insufficient funds")
