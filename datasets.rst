.. SimpleUI documentation master file, created by
   sphinx-quickstart on Sat May 16 14:23:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Датасеты
============


Датасеты – это механизм хранения и манипулирования данными, тесно связанный с UI-механизмами платформы (списками, ActiveCV и т.д.). Можно сказать, что это примитивная СУБД в памяти (или даже словарь в памяти), который если его наполнить данными обеспечивает сразу логику работы приложения. 

Датасет как объект имеет имя, имеет какие то настройки (индексы по полям, настройки полей поиска и т.д.) и содержит в себе данные, которые можно было бы назвать «массив объектов». В опциях можно настроить поведение датасета – как будут искаться данные, как будет отображаться конкретная запись на формах и т.д.

Ссылка на объект любого датасета в SimpleUI имеет вид ``<имя датасета>$<_id записи>``. Это универсальная ссылка в системе. Всегда можно получить запись любого датасета через ``DataSets.GetObjectStr(<ссылка>)`` или представление элемента через ``DataSets.GetView(<ссылка>)``.

В коде ниже: создадим датасет, заполним данными и сохраним.

.. code-block:: Python

 datasrv = CreateDataSet("goods") #создаем датасет goods

 #указываем hash-индексы, поля поиска по строке, шаблон представления записи
 datasrv.setOptions(json_to_str({"hash_keys":["article","barcode"],"search_keys":"name","view_template":"{name} , <b>{article}</b>"})) 

 #добавляем записи в датасет
 goods_list = []
 goods_list.append({"article":"AUD2071","name":"Стол","barcode":"4690626023178"})
 goods_list.append({"article":"AUD2075","name":"Стул","barcode":"6924922203797"})
 goods_list.append({"article":"AUD2076","name":"Лампа"})
 goods_list.append({"article":"AUD2076","name":"Барабан"})
 datasrv.put(json_to_str(goods_list))

 #записываем датасет на диск
 datasrv.save()

Использование датасета
------------------------

Таблицы и списки карточек
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Если у вас есть датасет то для того, чтобы разместить на экране список, достаточно просто указать ссылку на него через ~ . Вот пример переменной для Таблицы. Тут в качестве источника указан датасет "goods", а контейнер, в котором задается дизайн элементов списка - "list_3_lines"

.. code-block:: Python

 j = { "customtable":         {
         "layout": "^list_3_lines",
         "tabledata":"~goods"}
 }

 hashMap.put("table",json_to_str(j))
 

.. image:: _static/2025_dataset_4.png
       :scale: 55%
       :align: center


 Кстати, обычно для строк рисуется контейнер, но если не охота, то можно просто написать AUTO и он будет сгенерирован сам. Как видно на скиншоте, отображаются все поля, даже _id. Это может быть полезно на этапе разработки, форму карточки можно сделать потом.

.. code-block:: Python

 j = { "customtable":{
  "layout": "^AUTO",
  "tabledata":"~goods"
   }
  }
 

.. image:: _static/2025_dataset_5.png
       :scale: 55%
       :align: center


При нажатии генерируется событие CardsClick и в стеке переменных в selected_card_key появляется универсальная ссылка ``(<имя датасета>$<_id записи>)`` и также в **selected_card_data** – данные записи датасета в виде строки JSON

О поиске тоже можно не беспокоиться. Для датасета своя секция настроек поиска dataset_search в которой есть method(метод поиска), keys(поля поиска) и min_length (необязательно) минимальная длина с которой начинается поиск.

Метод может быть:
 
 * text - для обычного поиска по вхождению строки
 * levenshtein - для нечеткого поиска по расстоянию Левенштейна (будут выведены результаты в порядке убывания точности, с отбором >75, сама точность добавляется в записи  в поле _confidence


Кстати теперь появилась опция search_submit. Если она включена то надо нажимать подтверждение ввода (символ поиска на клавиатуре), если не включена то поиск происходит при наборе каждого символа. Для длинных строк и сложных поисковых алгоритмов это более гуманное решение в плане нагрузки.

Пример переменной таблицы с настройкой поиска

.. code-block:: Python

 j = { "customtable":
 {
  "options":{
            "search_enabled":True,
	    "search_submit":True,
            "dataset_search":{"method":"text", "keys":"name"}
    	   },
  "layout": "^list_3_lines",
  "tabledata":"~big"
   }
 }

Пример с нечетким поиском

.. code-block:: Python

 j = { "customtable":
 {
  "options":{
            "search_enabled":True,
	    "search_submit":True,
            "dataset_search":{"method":"levenshtein", "keys":"name","min_length":3}
    	   },
  "layout": "^list_3_lines",
  "tabledata":"~big"
   }
 }



Про большие датасеты.
"""""""""""""""""""""""

По умолчанию всегда включена пагинация, она невидимая, плавная. По умолчанию размер страницы – 100 записей. Но можно поставить свой размер - через числовую опцию page_size. Соответственно, чтобы отключить пагинацию туда надо записать большое число. Но не стоит торопиться ее отключать – с ней списки готовы вмещать миллионы записей без каких-либо признаков задержек. Ни малейшей задержки. Вот видео с 1 миллионом записей в датсете.
 
Поля датасетов
~~~~~~~~~~~~~~~~

Можно разместить на экране ссылочные поля ввода данных, содержащие ссылки на записи датасетов
 
Вы просто указывает переменную в которой храниться или будет храниться значение поля в виде ссылки и датасет в значении. И всё. Пользователь просто выбирает запись из списка, пользуется поиском если надо. При выборе в переменную также попадает универсальная ссылка.

Для такого случая у датасета желательно в опциях определить 2 вещи:

 * Представление записи – опция **view_template**. Можно использовать html. Имена полей указываются в фигурных скобках. Можно разместить в представлении несколько полей. Например {name}, {barcode}. Можно использовать html. Например ``{name}:<b>{article}</b>``
 * Можно указать форму элементов списка list_layout – имя контейнера (по умолчанию AUTO)

Пример создания и указания опций датасета:

.. code-block:: Python

 datasrv = CreateDataSet("goods")
 datasrv.setOptions(json_to_str({"list_layout":"item","view_template":"{name} , <b>{article}</b>"})) 

Можно использовать конструкцию с | чтобы разместить поле с заголовком


.. image:: _static/2025_dataset_1.png
       :scale: 55%
       :align: center



Для задания настройки полей есть упрощенный вариант и вариант с настройками. Упрощенный вариант приведен выше, а для настроек необходимо указать JSON-настройки (обычно - через переменную)
 
 * dataset (обязательно) – имя датасета
 * inline – поиск по строке непосредственно в поле
 * select – кнопка выбора из списка
 * spinner – выбор из списка (аналог выпадающего списка) заменяет опцию inline
 * hint - подсказка
 
Примеры различной настройки полей датасетов:


.. image:: _static/2025_dataset_2.png
       :scale: 55%
       :align: center



Выбранные и предустановленные значения
""""""""""""""""""""""""""""""""""""""""

Везде используется универсальная ссылка - как результат пользовательского выбора, так и для установки предопределенных значений.
Например, создадим датасет nds:

.. code-block:: Python

 datasrv = CreateDataSet("nds")
 datasrv.setOptions(json_to_str({"view_template":"Ставка - {name}"})) 

 nds_list = []
 nds_list .append({"name":"10%","_id":"НДС10"})
 nds_list .append({"name":"20%","_id":"НДС20"})
 nds_list .append({"name":"0%","_id":"НДС0"})
 datasrv.put(json_to_str(nds_list))

И на экране в onStart установим НДС по умолчанию

.. code-block:: Python

 hashMap.put("nds","nds$НДС20")

Тогда, при открытии, увидим результат:
 

.. image:: _static/2025_dataset_3.png
       :scale: 55%
       :align: center


Прямая связь элементов экрана с полями датасета
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. image:: _static/2025_dataset_6.png
       :scale: 55%
       :align: center



Если есть универсальная ссылка на датасет, то можно на экране связать обычные поля ввода с конкретной записью датасета. Тогда то, что пользователь вводит в поля будет писаться сразу в запись непосредственно. Причем писаться сразу как только меняются данные (вы только написали одну букву - данные сразу записались в поле датасета, без вызова события).
 
Когда меняешь текст в поле ввода, происходит прямая запись


Для этого нужно в значении указать переменную, в которой будет находиться ссылка на запись (универсальная ссылка), а в переменную надо поместить имя поля записи.


.. image:: _static/2025_dataset_7.png
       :scale: 55%
       :align: center


 
В current_order храниться ссылка, name - поле записи

.. note:: Для того, чтобы система корректно распознала такие поля, в Значении должна быть ссылка, поэтому, если ссылки пока нет (например при открытии), нужно поместить пустую ссылку <имя датасета>$)

Прямая запись возможна с элементами:
 
 * Поле ввода строка
 * Поле ввода число
 * Поле ввода пароля
 * Галочка
 * Дата
 * Многострочный текст
 * Надпись



Валидаторы OCR и штрихкодов в ActiveCV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Также датасеты используются как опорные выборки (валидаторы) при распознавании текста (OCR) и для валидации штрихкодов. Дело в том, что они очень быстрые и безусловно, этот вариант работы наиболее предпочтителен при оптическом распознавании.

Валидаторы – это опорные выборки для OCR или при сканировании штрихкодов. Когда оптическое распознавание находит объект, оно возвращает запись. Все что надо сделать – указать датасет для валидатора (в датасете обязательно нужно указать по каким полям будут индексы). Т.е. да, можно проверять найденный тест или 
штрихкод в обработчике, но дело в том что через валидатор это происходит в разы быстрее и писать ничего не надо. Подробнее о валидаторах - в разделе ActiveCV.

Датасет как источник данных
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Датасет это хранилище данных резидентное в памяти. И к этим данным можно обратиться. Можно получить все записи датасета all(), страницы записей getPage(from,to). Можно быстро получить запись по _id или индексируемому полю. Например если вы идете по штрихкоду но не используете ActiveCV, а используете обычный сканер и у вас есть датасет – «список товаров с штрихкодами» то вы можете его использовать как обычную БД:

.. code-block:: Python

 goods = GetDataSet("goods")
 res = goods.get("barcode","4690626023178")
 toast(res)

Создание и наполнение датасетов, манипуляции с данными.
---------------------------------------------------------

Датасет создается командой ``CreateDataSet(<имя датасета>)`` либо ``CreateDataSet(<имя датасета>,<опции>)`` либо опции можно установить отдельно после создания объекта датасета setOptions(<опции>). Опции это json-объект вида ``{"hash_keys":[<ключи>,…],”key”:[<ключи>,]}``. Все опции необязательны.

Возможные опции датасета:

 * search_keys - ключи (через запятую) по которым осуществляется поиск в списке
 * view_template - представление элемента в поле датасета. Ключи задаются в формате {<ключ>}, возможно использование html-тегов
 * list_layout - контейнер для списка выбора из полей датасетов
 * hash_keys - массив имен полей, по которым будет создан hash-индекс.
 * key - можно задать список полей из которых будет формироваться ключ id если он не задан, либо можно прjсто указывать id в записи, либо, если не указан id в запили и не указан key то id будет сгенерирован автоматически.

Также можно получить датасет копированием из другого датасета, тогда его опции будут скопированы. Команда ``copy(<имя нового датасета>)`` либо ``copy(<имя нового датасета>,<начальная строка>,<конечная строка>)``

.. code-block:: Python

 my = big.copy("my")

Датасеты пополняются командой put где в качестве параметра передается строка с JSON-массивом

А откуда берутся данные для массива в put? Приведу несколько примеров

Пример 1. *Просто в онлайн-обработчике*. Теперь в SimpleUI онлайн-обработчики есть двух видов – через HTTP-запрос (online) и через веб-сокеты + скрипт-шину о чем писал тут. И собственно можно вызвать онлайн обработчик и положить данные в датасет через put. Но данных может быть много за раз и через обработчик они будут передаваться долго. Посмотрим другие примеры.

В примере ниже язык - Python, но это может быть онлайн-обработчик в бек-системе и язык будет например, 1С:

.. code-block:: Python

 hashMap.put("CreateDataSets",json_to_str({"goods_online":{"hash_keys":["article","barcode"]}}))
 data = {"goods_online":[{"article":"EZ9F34132","name":"SE 32A, 4500", "barcode":"3606480586873"},
 {"article":"EZ9F34116","name":"SE 16A, 4500", "barcode":"3606480586842"},
 {"article":"EZ9F34110","name":"SE 10A, 4500", "barcode":"3606480586835"}
 ]}
 hashMap.put("PutDataSets",json_to_str(data))

Пример 2. *Мы выгрузили данные из 1С в CSV и не хотим делать REST или ODATA, просто положили их в файлик на Яндекс-диске*. В этом примере задействуется несколько механизмов. Сначала python-обработчик работает с API Яндекса для получения внутренней ссылки, потом запускается воркер для скачивания (котрый докачает файл, даже после перезагрузки девайса и с выключенным приложением), потом, когда файл скачала читаем CSV и пишем наконец в датасет. Бррр… сложно? Ну зато файлик просто лежит на Яндекс – диске, не надо поднимать сервер. В этот же пример можно записать вариации – файл не csv а сразу JSON-массив, не на яндекс-диске а на сервере с прямой ссылкой на скачивание. Воркер не обязательно использовать – это для больших файлов.

.. code-block:: Python

 import requests
 from urllib.parse import urlencode
 from ru.travelfood.simple_ui import SimpleUtilites as su
 import os
 import csv
  
 
 
 base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
 public_key = 'https://disk.yandex.ru/d/U6YrMsXQmMbfOA'  

 # Получаем загрузочную ссылку
 final_url = base_url + urlencode(dict(public_key=public_key))
 response = requests.get(final_url)
 download_url = response.json()['href']
 
 # Вариант 1 - для маленьких файлов
 #download_response = requests.get(download_url)
 #with open(su.get_downloads_dir()+os.sep+'p_menu.txt', 'wb') as f:   # Здесь укажите нужный путь к файлу
 #    f.write(download_response.content) 

 # Вариант 2 - для больших файлов
 def after_download_1():
     import csv
     with open(hashMap.get("DownloadedFile"), encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter="\t")
        dataset = list(reader)
        goods =GetDataSet("goods_load")
        goods.put(json_to_str(dataset)) 
        hashMap.put("RefreshScreen","")    
        toast("Загрузили...")
	
 postExecute = json_to_str([{"action": "run", "type": "pythonscript","method":get_body(after_download_1) }])
 su.download(download_url,None,None,'goods.txt',postExecute)

Пример 3. *Мы опубликовали из 1С автоматический интерфейс aData в несколько кликов и просто получаем данные из него напрямую**. Как в таком случае выглядит заполнение датасета:

.. code-block:: Python

 import requests
 from requests.auth import HTTPBasicAuth
 
 orders = GetDataSet("orders_load")
 if orders == None:
    orders = CreateDataSet("orders_load")
    orders.setOptions(json_to_str({"view_template":"{Number}", "list_layout":"order", "search_keys":"Number"}))

    url = "http://192.168.1.41:2312/kademo/odata/standard.odata/Document_ЗаказКлиента?$format=json"
    r = requests.get(url,auth=HTTPBasicAuth('usr', ''))
    result = r.json()
    records = []
    for record_1c in result["value"]:
        new_record = record_1c
        new_record["_id"] = record_1c['Ref_Key']
        records.append(new_record)

    orders.put(json_to_str(records)) 
    hashMap.put("RefreshScreen","")    
    toast("Загрузили...")
    
Манипуляция с данными
------------------------

Копирование
~~~~~~~~~~~~

.. code-block:: Python

 my = big.copy("goods") #копирует полностью 

 #или  
 
 my = big.copy("big",0,3) #копирует с 0 по 3 позицию 

Отбор
~~~~~~~

Датасет можно отфильтровать по условию используя метод filter(<условие>), где условие задается в том же синтаксисе что и для Pelican/SimpleBase или MongoDB https://simplebase.readthedocs.io/en/latest/querys.html

Сортировка

.. code-block:: Python
 
 my.sort("-name") #по убыванию по полю name 
 my.sort("name") #по возрастанию по полю name 

Обрезка
~~~~~~~~~~~
.. code-block:: Python

 my.cut(0,3)

Очистка
~~~~~~~~~

.. code-block:: Python

 my.clear()


Нечеткий поиск
~~~~~~~~~~~~~~~~~~~~

У датасета доступен метод  **findTextLevenshtein(String text,int confidence)** в который передается поисковая строка и требуемая точность. 

.. code-block:: Python
 
 ds = GetDataSet("goods") #берем датасет с товарами
 goods_select = CreateDataSet("goods_select") #создаем новый датасет для результатов поиска
 results = ds.findTextLevenshtein("name",hashMap.get("voice_text"),75) #вызываем нечеткий поиск, точность 75
 goods_select.put(results) #записываем результаты в новый датасет

В результате будут выданы записи для датасета, подходящей точности, отсортированные по точности в порядке убывания. В каждом элементе датасета будет добавлено поле точности **_confidence**. 


Хранение/загрузка
-------------------
У объекта датасета 2 метода без параметров **save()** и **load()**. Кроме того у датасета есть метод **isSaved()** который возвращает Истину если датасет был записан и **last_saved()**, который возвращает дату последнего сохранения. 

Пояснение к использованию датасетов в SimpleUI в аспекте локального хранения. В каких случая от СУБД можно и нужно отказаться в пользу датасета.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Давайте более пристально всмотримся в потоки данных, которые фигурируют в мобильном решении. SimpleUI – это фреймворк для бизнес приложений и так или иначе, решения на нем – это некое приложение или расширение функций бек-систем (ERP, MES, WMS и т.д.) Т.е. это своеобразный фронт. Даже если конфигурация «самостоятельная» и работает локально, она скорее всего в какие то моменты взаимодействует с бек-системой – забирает или отдает данные. Т.е. решение может быть онлайн с бек системой, оффлайн, и то что я называю «псевдо-онлайн» (когда данные пишутся локально и отправляются по возможности так быстро как смогут), но так или иначе его существование имеет смысл только если он обменивается данными с одной или несколькими системами для которых он работает.
 
Разные классы данных в мобильном приложении
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Что же за данные приходят и уходят? Я разделил их на классы, для того чтобы понять как удобнее всего работать с разными классами данных.

Разделив данные, я сделал предположение, что для разных классов данных нужны разные подходы, что какой-то одной супер-СУБД для мобильного решения не существует (по совокупности критериев) и что нужен дифференцированный подход для выбора инструмента хранения в зависимости от жизненного цикла данных. Именно жизненный 
цикл внутри приложения определяет требования к инструменту хранения.

И датасеты - это прежде всего данные, которые приходят на мобильное устройство извне, из бек-системы. Это прежде всего справочники, но также и документы, задания, распоряжения. Т.е. то, что в мобильном приложении не меняется, а просто существует для чтения и как правило имеет ссылки на объекты внешних систем. Так 
ли нужна СУБД для того, что не меняется? Ведь нет перезаписи в критические для производительности моменты – когда с UI работает пользователь, нет удаления. Для этой цели вполне бы подошел просто файл CSV или JSON. Да при 1 млн записей загрузка большого JSON займет 0,5 сек, но эта загрузка происходит в фоне в определенные моменты времени и не мешает работе.

.. note:: Когда речь идет о решениях, связанных с товарами или оборудованием/основными средствами, я рекомендую использовать принцип плоской таблицы (1NF) т.е. например если товар идентифицируется по штрихкоду, то и соберите таблицу Штрихкод-Артикул-Название товара-Единица-Ссылка товара-Ссылка единицы. Да, можно сделать несколько таблиц в реляционной СУБД с внешними связями? А зачем? Когда товар сканируется (или ищется по артикулу) то вы мгновенно получаете все данные по товару. На фронте больше ничего и не надо.

Что и как мы выигрываем с датасетами? И за счет каких принципов?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Первый принцип** – глубокая интеграция в механизмы платформы. Например, достаточно поместить данные в датасет и мы уже получаем отображение в виде списков с нужным дизайном (дизайн задается контейнерами). Как происходит с любой СУБД – данные надо выбрать, сформировать список записей и поместить в адаптер списка (тут еще надо не забывать про преобразования JSON). А тут не надо ничего этого делать – список на уровне приложения берет данные из датасета. На видео выше видно как работает список с 1 млн. записей. Это следствие принципа интеграции. Тоже самое с OCR – когда в видеопотоке мелькает текст, нужно очень-очень быстро делать get к данным, иначе все будет не плавно.

**Второй принцип** – отсутствие необходимости поддержания данных. Датасет – это просто put, сохранить/загрузить в основном (нет, есть и get и выборки и манипуляции по желанию). Он может пополняться в режиме upsert по ключу, но по большому счету он существует как просто список который можно сохранить/загрузить. Не нужно Insert/Update/Delete и выборки. Это просто список висящий в памяти, который можно сохранить/загрузить. Это не СУБД.

Место датасета в архитектуре хранения. Дифференцированный подход к хранению.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

В SimpleUI существует целая палитра СУБД. Можно было бы все данные хранить в JSON-ориентированной noSQL Pelican. Но рекомендуется условно поделить данные на классы. Тогда можно для каждого класса подобрать более простые инструменты:

 * key-value для констант, настроек, кеширования пользовательского ввода, логов
 * данные внешних систем (справочники, документы, ссылки) - датасеты
 * данные, создаваемые в приложении, документы, объекты локального учета - Pelican, в котором опять же используются универсальные ссылки датасетов например.

Вот такое разделение подходов предлагается разработчику. Например, в поле датасета выбрали товар (получили универсальную ссылку), там же на экране указали количество. И записали это все в СУБД Pelican

.. code-block:: Python

 db = Pelican("samples_db1")
 db["orders"].insert({"sku":"goods$100","qty":10})




