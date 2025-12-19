from tortoise import models, fields

class User(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    name = fields.CharField(max_length=300, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name