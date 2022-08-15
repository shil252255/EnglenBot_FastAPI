from tortoise.models import Model
from tortoise import fields, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


class Words(Model):
    word = fields.CharField(max_length=50, unique=True, index=True)
    transcription = fields.CharField(max_length=50, null=True)
    translation = fields.CharField(max_length=50)
    word_class = fields.ForeignKeyField('models.WordsClasses', related_name="class", null=True)

    def __str__(self):
        return self.word

    class Meta:
        ordering = ["word"]


class WordsClasses(Model):
    name = fields.CharField(max_length=10)


class Nouns(Model):
    word = fields.ForeignKeyField('models.Words')
    plural = fields.CharField(max_length=50, index=True, unique=True)


class Verbs(Model):
    word = fields.ForeignKeyField('models.Words')
    past = fields.CharField(max_length=50, unique=True, index=True)
    past_participle = fields.CharField(max_length=50, unique=True, index=True)


class Adjective(Model):
    word = fields.ForeignKeyField('models.Words')
    comparative = fields.CharField(max_length=50, unique=True, index=True)
    superlative = fields.CharField(max_length=50, unique=True, index=True)


Tortoise.init_models(["models"], "models")
WordsPydantic = pydantic_model_creator(Words)
WordsInPydantic = pydantic_model_creator(Words, name='WordsIn', exclude_readonly=True)
WordsClassesPydantic = pydantic_model_creator(WordsClasses, name='Class')
