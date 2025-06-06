.. SimpleUI documentation master file, created by
   sphinx-quickstart on Sat May 16 14:23:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Локализация типовых решений
=================================

Можно разрабатывать решения, которые будут включать в себя мультиязычный интерфейс. Автоматизированному переводу подвергаются отображаемые названия процессов, экранов, любых надписей и визуальных элементов.

Пример к данной статье находится в https://github.com/dvdocumentation/simpleui_samples/tree/main/Sample%204%20localization

Для работы с несколькими словарями нужно создать и указать в свойстве конфигурации «Словари» JSON-строку примерно такого вида:

``{"en":{"ключ 1": "перевод 1 en", "ключ 2": "перевод 2 en"},{"ru":{"ключ 1": "перевод 1 ru", "ключ 2": "перевод 2 ru"}}``

Т.е. перечисляются словари – en,ru и т.д. , в интерфейсе указываются ключи, а в словарях переводы ключей

Так помимо простых экранных форм и надписей переводятся и сложные элементы, задаваемые в переменных (например таблицы, списки карточек, выпадающие списки и т.д.) то элементы перевода (например заголовков таблицы) должны быть включены в само значение такой переменной. Это достигается за счет шаблонизатора. Шаблоны задаются между квадратными скобками например тут Barcode и Qty выступают ключами в словарях и если в словарях будет перевод, то они будут переведены

.. code-block:: Python

  table  = {
    "type": "table",
    "textsize": "20",

    "columns": [
    {
        "name": "barcode",
        "header": "[Barcode]",
        "weight": "2"
    },
    {
        "name": "name",
        "header": "Name",
        "weight": "2"
    },
      {
        "name": "qty",
        "header": "[Qty]",
        "weight": "1"
    }
    ]
    }

Таким образом нужно задать все переводы ключей. Если перевод отсутствует, будет отображен просто ключ.

Также необходимо дать пользователю возможность самому выбрать интересующий интерфейс.

Для этого есть несколько команд:

**DEVICE_LOCALE** - константа в hashMap, в которой храниться язык, заданный в настройках системы на устройстве

**setLocale** - команда, задающая язык пользовательского интерфейса – т.е. указывающая приложению, какой словарь из списка словарей следует применить при загрузке. Например, ``hashMap.put("setLocale","en")``

