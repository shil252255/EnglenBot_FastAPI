from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError

from models import *


app = FastAPI()


@app.get('/words', response_model=list[WordsPydantic])
async def get_words():
    return await WordsPydantic.from_queryset(Words.all())


@app.post('/words', response_model=WordsPydantic)
async def create_word(word: WordsInPydantic):
    word_obj = await Words.create(**word.dict(exclude_unset=True))
    return await WordsPydantic.from_tortoise_orm(word_obj)

register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

