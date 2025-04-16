from peewee import *

db = SqliteDatabase('leaddit.db')

class BaseModel(Model):
    class Meta:
        database = db

class Lead(BaseModel):
    id = AutoField()
    name = CharField()
    persona = CharField()
    score = IntegerField()

db.connect()
db.create_tables([Lead], safe=True)