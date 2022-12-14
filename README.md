### Сервис

Сервис рекомендует товары (itemid) по номеру пользователя (visitorid). Если пользователя нет в базе - рекомендуется топ 3 самых продаваемых itemid.


### Входные данные

events csv - данные о посетителях сайта и их взаимодействии
- 'timestamp' - временная метка события (unix-time)
- 'visitorid' - id посетителя
- 'event' - тип события: view, addtocart и transaction
-  'itemid' - id товара
- 'transactionid' - id транзакции

item_properties_part(1, 2).csv - данны о свойствах товаров
- 'timestamp' - временная метка присвоения свойства
- 'itemid' - id товара
- 'property' - закодированное название свойства
-  'value' - закодированное значение свойства

category-tree.csv - дополнительные данные о соответствии категории товара (categoryid) и надкатегории (parentid)


### Трансформации, обучение, валидация

Для реализации рекоммендаций на основе LightFM необходимо создать объект Dataset из библиотеки LightFM (чтобы не заниматься переводом данных в sparse массивы).
В данный датасет нужно загрузить все имеющиеся в events.csv уникальные visitorid и itemid.
Далее в данные датасет нужно вгрузить train и test выборки (для этого предварительно нужно разбить данные events.csv на train/test, где test - последние 30% записей событий) в этот Dataset с помощью метода build_interactions. Таким образом получается 2 объекта Dataset - для обучения и для валидации.

Далее модель LightFM обучается и проверяется значение ключевой метрики precision at 3 на валидационном Dataset.


### Выбранная модель

Были проведеные эксперименты с контекстными, матричными методами и использованием решающих деревьев с градиентным бустингом (XGBoost). Контекстные методы показали Precision@3 на уровне ~0.1%. Коллаборативная фальтрация на LightFM показала результат 0.93%. XGBoost в задаче классификации транзация/не транзакция ввиду колоссального дисбаланса классов с задачей не справился.

Эксперименты с гиперпараметрами LightFM:
loss='bpr', no_componenst=30 - 0.13%
loss='warp', no_components=30 - 1.0%
loss='warp', no_components=50 - 1.03%
loss='warp', no_components=100 - 0.99%

Таким образом, выбрана модель с гиперпараметрами loss='warp', no_components=50.


### Описание API

Сервис работает через отправку GET запроса с параметром visitorid, равным visitorid пользотеля, которому нужно сделать рекоммендации.
Сервис доступен по адресу 0.0.0.0:5000/
Endpoint для снятия рекомендаций в формате JSON - 0.0.0.0:5000/recomm/
Для получения рекомендаций необходимо сделать запрос с параметром visitorid, куда необходимо передать visitorid пользователя, которому нужно предложить рекомендации.
Например:
0.0.0.0:5000/?visitorid=3 - текстовый вывод рекомендаций
0.0.0.0:5000/recomm/?visitorid=3 - endpoint c JSON


### Быстрый запуск модели

Вместе с запуском докер контейнера необходимо свзязать порт 5000 внутри контейнера и докер образ на конкретной машине.
`sudo docker run -d -p 5000:5000 final_project`
