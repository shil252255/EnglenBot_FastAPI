# Бот по изучению английского.

Очередная попытка написать телеграм бот или даже полноценный сервис для изучения английского языка.

### В этой итерации буду использовать:

- FastAPI
- TortoiseORM
- Aiogram

_Также при использовании GIT руководствуюсь: https://www.conventionalcommits.org/en/v1.0.0/_

## Модели.
Слова....

Если у меня есть только слово и перевод то все просто, но нет у меня не только слово и перевод.
В зависимости от того какая это часть речи у каждого слова есть несколько форм.

Так например:
- Существительное - единственное и множественное число.
- глагол разное время 2-я и 3-я форма неправильных глаголов.
- Прилагательное сравнительные формы.

Также есть сокращения или разговорные формы.
Также есть всякие модификаторы вроде принадлежности 's и прочее
ладно тогда для начала возьмем 3 основные части речи
существительное глагол прилагательное и допустив прочее не определенно

Тогда очевидно нужна табличка __Words__

В которой будут основные формы слов якорные так сказать, перевод и обозначение части речи,
а дальше в теории должны быть таблички с альтернативными формами этих слов
своя для глаголов, для существительных и для прилагательных

