# Sheep.Fish test task
Генерація карток відбувається за допомогою manage.py команди `generate_cards`

Є два файли з fixtures. Завантажувати в наступному порядку:

`python manage.py loaddata fixtures/cards.json`

`python manage.py loaddata fixtures/activities.json`

Функціонал активації/деактивації та видалення картки реалізовано в адміністративній частині сайту
