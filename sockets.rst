.. SimpleUI documentation master file, created by
   sphinx-quickstart on Sat May 16 14:23:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Веб-сокеты
========================


Команды
------------

**ConnectWebSocket** – соединиться с веб сокетом. Пример: ``hashMap.put("ConnectWebSocket","ws://192.168.1.41:8765")``

**WSOnConnectHandlers** – подключить обработчики события успешного соединения с сокетом в формате архитектуры 2.0. 

Пример: ``hashMap.put("WSOnConnectHandlers",json.dumps([{"action":"run","type":"python","method":"ws_connect"}] ))``

**WSOnMessageHandlers** - подключить обработчики события получения сообщения в формате архитектуры 2.0. Само сообщение приходит в переменной  *WebSocketMessage*

**WSOnCloseHandlers** -  подключить обработчики события нормального завершения соединения  в формате архитектуры 2.0.

**WSOnFailureHandlers** -   подключить обработчики события потери соединения  в формате архитектуры 2.0.

**WebSocketSend** – команда отправки сообщения в сокет. 

**CloseWebSocket** – команда завершения соединения. Также можно закрывать соединения со стороны сервера например.

Особенности работы.
---------------------

 1. При разрыве соединения автоматически происходит переподключение каждую секунду. Чтобы остановить попытки надо удалить переменную *ConnectWebSocket*

 2. При начальном соединении автоматически посылается сообщение в формате ``id:<AndroidID>`` . Это можно использовать для идентификации пользователей например

