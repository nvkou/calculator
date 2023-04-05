from fastapi import HTTPException
from tortoise import fields, models
from enum import IntEnum


class OperationValue(IntEnum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    SQRT = 5
    RANDOM = 6
    MISC = 7


class Operation(models.Model):
    id = fields.IntField(pk=True)
    operation = fields.IntEnumField(enum_type=OperationValue, null=False)
    cost = fields.FloatField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
