from typing import Optional

from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.context import CryptContext
from fastapi import HTTPException

from data_model.operation import OperationValue, Operation
from data_model.record import Record


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, index=True, unique=True, null=False)
    password = fields.CharField(max_length=126, null=False)
    email = fields.CharField(max_length=20, unique=True, index=True, null=False)
    status = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


UserIn = pydantic_model_creator(User, name="UserIn", exclude_readonly=True, exclude=("id", "created_at", "updated_at", "status"))
UserOut = pydantic_model_creator(User, name="UserOut", exclude=("password", "created_at", "updated_at"))
#UserDBSchema = pydantic_model_creator(User, name="User", exclude=("created_at", "updated_at"))

pwd_util = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user: UserIn) -> UserOut:
    user.password = pwd_util.hash(user.password)

    try:
        user_obj = await User.create(**user.dict(exclude_unset=True))
        operation_obj = await Operation.create(cost=0.0, operation=OperationValue.MISC)
        init_balance = await Record.create(user=user_obj, amount=0.0, user_balance=100.0,
                                           operation_respond="Initial Balance", operation=operation_obj)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return await UserOut.from_tortoise_orm(user_obj)


async def validate_user(user: UserIn) -> bool:
    user_obj = await User.filter(username=user.username).first()
    if user_obj:
        return pwd_util.verify(user.password, user_obj.password)
    return False


async def get_current_user(user_name: str) -> Optional[User]:
    return await User.filter(username=user_name, status=True).first()
