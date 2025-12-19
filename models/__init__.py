from tortoise import Tortoise

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models.users', 'models.contents']}
    )
    await Tortoise.generate_schemas()