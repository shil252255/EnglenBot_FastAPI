# Парсер слов для словаря.

https://www.babla.ru/английский-русский/

Мне приглянулся этот сайт так как на нем есть обозначение части речи и простой перевод.

Очень может быть что это не оптимальное решение, его поиск у меня занял не больше 5 минут, но пока сойдет.

## Реализация.

- открываем сайт
- парсим адреса букв
- переходим на букву
- ...
- НЕТ
- Адреса страничек генерируются просто и логично
  
  сайт/буква/страничка если номер больше то просто отображается последняя страничка изи
- Парсим слова + ссылка, только те что с маленькой буквы и одним словом
- На страничке выдергиваем первый перевод и часть речи и дальше посмотрим