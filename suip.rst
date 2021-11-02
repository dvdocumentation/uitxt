.. SimpleUI documentation master file, created by
   sphinx-quickstart on Sat May 16 14:23:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Файлы-процессы .suip
======================

.. image:: _static/suip_scheme.PNG
       :scale: 19%
       :align: center



Платформа Simple UI поддерживает разные варианты хранения и транспортировки данных – в SQL устройства, в NoSQL устройства, в документах и непосредственно на сервере при он-лайн варианте работы (хранение) и различные виды запросов, он-лайн команды, обмен файлами, документами (транспорт). Сейчас добавляется новый вид хранения/транспортировки – «файлы-процессы».  Это текстовый файл, состоящий из JSON-строки который включает в себя все необходимое для работы:

 * Структуру процесса, со всеми обработчиками и т.д.
 * Данные процесса, которыми он может пользоваться и менять, записываю туда же – в файл
 * Необходимую информацию для отображения внутри системы – дата последнего изменения, обложка и т.д.

То есть данные и механизмы ввода и обработки данных инкапсулированы в одном объекте.

Таким образом – это как бы самостоятельная мини-конфигурация сразу с данными и всем необходимым в виде suip-файла которую можно послать получателю, который не имеет доступа к вашему веб-сервису и каки либо других настроек, а просто может открыть, поработать и закрыть файл сохраним в свою очередь свои данные и отправить пользуясь инфраструктурой своего устройства. Это можно сравнить с Excel с макросами или PDF-формами и чем то подобным, но с возможностями Simple UI – работа с оборудованием, питоном, дополненной реальностью, AI-штуками и т.д. 
Использование существующей инфраструктуры хранения и доставки – это главное удобство такой архитектуры. Например можно использовать мессенджеры или почту где помимо самого suip-файла может быть в произвольном виде описаны пояснения по работе процесса, получена обратная связь
Файлы можно передавать различными способами – как через Интернет, так и например через Bluetooth, при этом не надо пробрасывать вебсервис основной системы наружу.

Работа с suip-файлами
----------------------

В файлы процессы можно паковать как обычный процесс (с экранами) так и ActiveCV процесс

Регламентируется наличие двух обязательных объектов в корне JSON:

 * **SimpleUIProcess** – структура процесса
 * **data** - все данные


Также в файл сами добавляются поля **last_update** и **last_update_millis** – даты последнего изменения файла, а также можно задать html обложку caption для отображения в программе на закладке «документы». Если ее не задать в файле она будет сгенерирована автоматически по корневым полям объекта data. Эти поля касаются отображения в списке последних открытых файлов и необязательны.

Файл можно создать предварительно из бек-системы или «открепить» обычный процесс, сохраним данные в data.

В конструкторе в Процессе и Операции ActiveCV предусмотрены кнопки «Выгрузить основу процесса». Она копируют в буфер обмена JSON- содержимое которое должно быть в SimpleUIProcess и остается его только вставить в макет обработки. Примеры мекетов обработок прилагаются в комплекте разработчика. Эти обработки записывают поля секции data и затем компонуется файл из SimpleUIProcess и data.

.. note::  При открытии файл-процесса содержимое data копируется сразу в Переменные (или hashMap) при этом сам объект data доступен в pyton- обработчиках сразу как словарь _data т.е. его не нужно доставать из строки в json и пистаь обратно. Поэтому для анного примера достаточно сразу определить объекты green_list и object_info_list – они просто сразу запишутся в переменные и будут прочитаны ActiveCV. Получается для данного примера программирования со стороны обработчиков не нужно – только подготовка файла.


Пример содержимого suip-файла


.. code-block:: JSON

    {
    "SimpleUIProcess": {
        "type": "Process",
        "ProcessName": "Приемка по заказу файл-процесс",
        "PlanFactHeader": "План-факт",
        "DefineOnBackPressed": false,
        "hidden": false,
        "login_screen": false,
        "SC": true,
        "Operations": [
        {
            "type": "Operation",
            "Name": "Приемка по заказу начало",
            "Timer": false,
            "hideToolBarScreen": false,
            "noScroll": false,
            "handleKeyUp": false,
            "noConfirmation": false,
            "hideBottomBarScreen": false,
            "onlineOnStart": false,
            "send_when_opened": false,
            "onlineOnInput": false,
            "PythonOnCreate": "77u/aWYgbm90ICdzY2FubmVkJyBpbiBfZGF0YToNCiAgICBfZGF0YVsnc2Nhbm5l\r\nZCddPVtd",
            "PythonOnInput": "77u/aW1wb3J0IGpzb24NCg0KaWYgaGFzaE1hcC5nZXQoImxpc3RlbmVyIik9PSJi\r\nYXJjb2RlIjoNCiAgICBfZGF0YVsnc2Nhbm5lZCddLmFwcGVuZChoYXNoTWFwLmdl\r\ndCgiYmFyY29kZSIpKSAj0L/RgNC+0YHRgtC+INC70L7QsyDQstGB0LXQs9C+INC+\r\n0YLRgdC60LDQvdC40YDQvtCy0LDQvdC90L7Qs9C+DQoNCiAgICBoYXNoTWFwLnB1\r\ndCgiU2hvd0RpYWxvZyIsItCU0LjQsNC70L7QsyDQstCy0L7QtNCwINC60L7Qu9C4\r\n0YfQtdGB0YLQstCwIikNCiAgICBoYXNoTWFwLnB1dCgiU2hvd0RpYWxvZ1N0eWxl\r\nIiwieyAgIiJ0aXRsZSIiOiAiItCS0LLQtdC00LjRgtC1INC60L7Qu9C40YfQtdGB\r\n0YLQstC+IiIsICAgIiJ5ZXMiIjogIiLQodC+0YXRgNCw0L3QuNGC0YwiIiwgICAi\r\nIm5vIiI6ICIi0J7RgtC80LXQvdCwIiIgfSIpDQoNCg0KICAgIGZvdW5kPUZhbHNl\r\nDQogICAgZm9yIGxpbmVfdGFibGUgaW4gX2RhdGFbJ3RhYmxlJ11bJ3Jvd3MnXToN\r\nCiAgICAgICAgaWYgbGluZV90YWJsZVsnYmFyY29kZSddPT1oYXNoTWFwLmdldCgi\r\nYmFyY29kZSIpOg0KICAgICAgICAgICAgaGFzaE1hcC5wdXQoIm9iamVjdCIsbGlu\r\nZV90YWJsZVsnbm9tJ10pDQogICAgICAgICAgICBoYXNoTWFwLnB1dCgiU2hvd0Rp\r\nYWxvZyIsItCU0LjQsNC70L7QsyDQstCy0L7QtNCwINC60L7Qu9C40YfQtdGB0YLQ\r\nstCwIikNCiAgICAgICAgICAgIGhhc2hNYXAucHV0KCJTaG93RGlhbG9nU3R5bGUi\r\nLCJ7ICAiInRpdGxlIiI6ICIi0JLQstC10LTQuNGC0LUg0LrQvtC70LjRh9C10YHR\r\ngtCy0L4iIiwgICAiInllcyIiOiAiItCh0L7RhdGA0LDQvdC40YLRjCIiLCAgICIi\r\nbm8iIjogIiLQntGC0LzQtdC90LAiIiB9IikNCg0KICAgICAgICAgICAgbGluZV90\r\nYWJsZVsncXR5X2ZhY3QnXT1saW5lX3RhYmxlWydxdHknXQ0KICAgICAgICAgICAg\r\nZm91bmQ9VHJ1ZQ0KICAgICAgICAgICAgYnJlYWsNCiAgICBpZiBub3QgZm91bmQ6\r\nDQogICAgICAgIGhhc2hNYXAucHV0KCJ0b2FzdCIsItCo0YLRgNC40YXQutC+0LQg\r\n0L3QtSDQvdCw0LnQtNC10L0iKSAgICANCiAgICAgICAgaGFzaE1hcC5wdXQoImJl\r\nZXAiLCIiKSAgICANCiAgICBoYXNoTWFwLnB1dCgidGFibGUiLGpzb24uZHVtcHMo\r\nX2RhdGFbJ3RhYmxlJ10pKSAgIA0KDQppZiBoYXNoTWFwLmdldCgibGlzdGVuZXIi\r\nKT09ICJvblJlc3VsdFBvc2l0aXZlIjogI9C30LDQv9C40YHRi9Cy0LDQtdC8INC6\r\n0L7Qu9C40YfQtdGB0YLQstC+INCyINC00L7QutGD0LzQtdC90YINCiAgICBmb3Ig\r\nbGluZV90YWJsZSBpbiBfZGF0YVsndGFibGUnXVsncm93cyddOg0KICAgICAgICBp\r\nZiBsaW5lX3RhYmxlWydiYXJjb2RlJ109PWhhc2hNYXAuZ2V0KCJiYXJjb2RlIik6\r\nDQogICAgICAgICAgICBsaW5lX3RhYmxlWydxdHlfZmFjdCddPWhhc2hNYXAuZ2V0\r\nKCdxdHknKQ0KICAgICAgICAgICAgYnJlYWsNCg==",
            "DefOnlineOnCreate": "",
            "DefOnlineOnInput": "",
            "Elements": [
            {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "Сканируйте товар",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "20",
                    "TextColor": "#ffffff",
                    "TextBold": true,
                    "TextItalic": false,
                    "BackgroundColor": "#4682B4",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 0
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "Заказ",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "20",
                    "TextColor": "#4682B4",
                    "TextBold": false,
                    "TextItalic": false,
                    "BackgroundColor": "",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 0,
                    "gravity_horizontal": "center"
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@order",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "20",
                    "TextColor": "#8B008B",
                    "TextBold": true,
                    "TextItalic": false,
                    "BackgroundColor": "",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 1,
                    "gravity_horizontal": "left"
                },
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "Требуется принять товары:",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "20",
                    "TextColor": "#4682B4",
                    "TextBold": false,
                    "TextItalic": false,
                    "BackgroundColor": "",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 0,
                    "gravity_horizontal": "center"
                },
                {
                    "type": "TableLayout",
                    "show_by_condition": "",
                    "Value": "@table",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "0",
                    "TextColor": "",
                    "TextBold": false,
                    "TextItalic": false,
                    "BackgroundColor": "",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 0,
                    "gravity_horizontal": "center"
                }
                ]
            },
            {
                "type": "barcode",
                "show_by_condition": "",
                "Value": "",
                "Header": "",
                "document_type": "",
                "mask": "",
                "Variable": "barcode"
            }
            ]
        },
        {
            "type": "Operation",
            "Name": "Диалог ввода количества",
            "Timer": false,
            "hideToolBarScreen": false,
            "noScroll": false,
            "handleKeyUp": false,
            "noConfirmation": false,
            "hideBottomBarScreen": false,
            "onlineOnStart": false,
            "send_when_opened": false,
            "onlineOnInput": false,
            "PythonOnCreate": "77u/",
            "PythonOnInput": "77u/",
            "DefOnlineOnCreate": "",
            "DefOnlineOnInput": "",
            "Elements": [
            {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [
                {
                    "type": "TextView",
                    "show_by_condition": "",
                    "Value": "@object",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "",
                    "TextSize": "15",
                    "TextColor": "#4682B4",
                    "TextBold": true,
                    "TextItalic": true,
                    "BackgroundColor": "",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 0,
                    "gravity_horizontal": "center"
                },
                {
                    "type": "EditTextNumeric",
                    "show_by_condition": "",
                    "Value": "",
                    "NoRefresh": false,
                    "document_type": "",
                    "mask": "",
                    "Variable": "qty",
                    "TextSize": "0",
                    "TextColor": "",
                    "TextBold": false,
                    "TextItalic": false,
                    "BackgroundColor": "",
                    "width": "match_parent",
                    "height": "wrap_content",
                    "weight": 0,
                    "gravity_horizontal": "center"
                }
                ]
            }
            ]
        }
        ]
    },
    "data": {
        "docNumber": "АВ00-000040",
        "order": "Заказ №АВ00-000040",
        "table": {
        "type": "table",
        "textsize": "25",
        "hidecaption": "true",
        "hideinterline": "true",
        "columns": [
            {
            "name": "nom",
            "header": "Товар",
            "weight": "2"
            },
            {
            "name": "qty",
            "header": "Кол.план",
            "weight": "1"
            },
            {
            "name": "qty_fact",
            "header": "Кол.факт",
            "weight": "1"
            }
        ],
        "rows": [
            {
            "nom": "Шина монтажная без герметика FP 30*0.6",
            "qty": 10500,
            "qty_fact": 0,
            "barcode": "4690216127378"
            },
            {
            "nom": "EFA 10*100 F Дюбель фасадный, шг, Нейлон (50 шт.)",
            "qty": 5,
            "qty_fact": 0,
            "barcode": ""
            }
        ]
        },
        "goods": [
        {
            "nom": "Шина монтажная без герметика FP 30*0.6",
            "qty": 10500,
            "fact_qty": 0,
            "barcode": "4690216127378"
        },
        {
            "nom": "EFA 10*100 F Дюбель фасадный, шг, Нейлон (50 шт.)",
            "qty": 5,
            "fact_qty": 0,
            "barcode": ""
        }
        ]
    }
    }


