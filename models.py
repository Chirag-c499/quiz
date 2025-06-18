from peewee import *

db = SqliteDatabase("database.db")

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

class Quiz(BaseModel):
    title = CharField()

class Question(BaseModel):
    quiz = ForeignKeyField(Quiz, backref="questions")
    text = CharField()
    a = CharField()
    b = CharField()
    c = CharField()
    d = CharField()
    correct_answer = CharField()

class Result(BaseModel):
    user = ForeignKeyField(User, backref="results")
    quiz = ForeignKeyField(Quiz, backref="results")
    score = IntegerField()

