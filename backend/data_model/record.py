from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Record(models.Model):
    id = fields.IntField(pk=True)
    operation = fields.ForeignKeyField('models.Operation', related_name='operations')
    user = fields.ForeignKeyField('models.User', related_name='users')
    amount = fields.FloatField(null=False)
    user_balance = fields.FloatField(null=False)
    operation_respond = fields.CharField(max_length=100, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)  # using create and update time to represent date
    updated_at = fields.DatetimeField(auto_now=True)
    soft_delete = fields.BooleanField(default=False)


recordOut = pydantic_model_creator(Record, name="RecordOut", exclude=("created_at", "user"))
recordIn = pydantic_model_creator(Record, name="RecordIn", exclude_readonly=True, exclude=("created_at", "updated_at"))

async def get_records():
    return await recordOut.from_queryset(Record.all())


async def get_record(id: int) -> recordOut:
    return await recordOut.from_queryset_single(Record.get(id=id))
