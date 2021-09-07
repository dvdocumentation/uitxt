.. SimpleUI documentation master file, created by
   sphinx-quickstart on Sat May 16 14:23:51 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Про отладку
=============

Отладка в он-лайн режиме
--------------------------

Онлайн режим означает что код обработчиков выполняется на стороне бека, то есть на сервере. Соотвественно без труда можно задействовать отладку средствами сервера. Например если в качестве бек-системы используется 1С то для отладки надо:

 * В серверном общем модуле (например ОтладкаПроцессов) вынести код обработчиков в отдельные процедуры. Например ``Обработчик1(Переменные,ТаблицаСтрок,Ошибка,СообщениеОбОшибке) Экспорт``
 * В соотвествующих обработчиках добавить вызов этой процедуры ``ОтладкаПроцессов .Обработчик1(Переменные,ТаблицаСтрок,Ошибка,СообщениеОбОшибке)``
 * Включить режим отладки на сервере, включить Автоматическое подключение к HTTP-сервисы и пройти обработчик в режиме отладки

Также для понимания работы и того что передается Ингода нелишним может быть перехватывать обработчик метода set_input HTTP-сервиса SimpleWMS – там можно посмотреть какие данные приходят кроме переменных в ответе JSON

Отладка в самостоятельном режиме
------------------------------------

Разработка оффлайн скриптов предполагает использование нескольких инструментов и методик для просмотра содержимого переменных, СУБД и отладки.

Консоль запросов
~~~~~~~~~~~~~~~~~

Прежде всего, если для хранения используется SQL СУБД, для просмотра содержимого таблиц, проверки работы запросов, которые используются в скриптах рекомендуется использовать «Консоль SQL запросов». Устройство и вызывающая обработка должны использовать одну подсеть, так как отправка запросов идет на веб-сервис приложения. В запросах можно передать параметры. Можно использовать все возможности SQLlite – служебные таблицы и т.д.

Логирование
~~~~~~~~~~~~

Для получения промежуточных данных можно использовать логирование и выводить тосты особым способом (внутри кода обработчика). Таким образом можно получать как значения переменных так и напрмиер логировать датасеты запросов не в начале/конце обработчика а именно внутри кода. 
Записи логов отправляются http-запросами, в демо базе есть сервис python_debug и регистр сведений scЛогPython куда пишутся значения.
Вот пример общего модуля сервисных процедур для этого:

.. code-block:: Python

  import sqlite3
  from sqlite3.dbapi2 import Error
  import requests
  import json
  import java
  from requests.auth import HTTPBasicAuth
  from com.chaquo.python import Python

  # Процедуры для отадки python-скриптов
  def query_to_json(query, args=()):
      conn = sqlite3.connect('//data/data/ru.travelfood.simple_ui/databases/SimpleWMS')
      cursor =  conn.cursor()
      cursor.execute(query, args)
      r = [dict((cursor.description[i][0], value) \
                 for i, value in enumerate(row)) for row in cursor.fetchall()]
      cursor.connection.close()
      return r
  
  def send_debug_msg(hashMap,tag,message):
      username=hashMap.get("WS_USER")
      password=hashMap.get("WS_PASS")
      url = hashMap.get("WS_URL")
  
      py_toast( url)
  
      r = requests.get(url+"/python_debug?tag="+tag+"&message="+message, auth=HTTPBasicAuth(username, password),
	     headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
  
  def send_debug_query(hashMap,tag,message,query, args):
      username=hashMap.get("WS_USER")
      password=hashMap.get("WS_PASS")
      url = hashMap.get("WS_URL")
  
      r = requests.get(url+"/python_debug?tag="+tag+"&message="+message, auth=HTTPBasicAuth(username, password),
  	   headers={'Content-type': 'application/json', 'Accept': 'text/plain'},data=json.dumps(query_to_json(query, args=())))
  
  
  def py_toast( msg):
          from android.widget import Toast
          Toast.makeText(Python.getPlatform().getApplication(), msg,
                         Toast.LENGTH_SHORT).show()
  
  Описание:

**send_debug_msg** – отсылает сообщения в лог

**send_debug_query** – выполняет произвольный запрос с параметрами, результат упаковывает в датасет JSON

**py_toast** – выводит тост внутри скрипта средствами Android SDK. Работает только из обработчиков Python

Пример использования:

.. code-block:: Python

  import sys
  sys.path.append("/data/user/0/ru.travelfood.simple_ui/files")
  import ui_global
  import json
  a = 2
  hashMap.put("a","1")
  ui_global.py_toast(hashMap.get("a"))
  ui_global.send_debug_msg(hashMap,"line 3",str(a))
  a+=1
  ui_global.send_debug_msg(hashMap,"line 4",str(a))
  ui_global.send_debug_query(hashMap,"sql","SELECT * FROM goods_bp","SELECT * FROM goods_bp",None)
  
Разработка и отладка через HTTP сервис
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Идея очень простая – писать и отлаживать в IDE Python (PyCharm, Thonny, Studio Code и др.) через HTTP разработку – Flask, FastAPI и т.п. То есть исполнять python-скрипты в онлайн режиме, а потом просто перенести их на оффлайн-закладки. При этом доступны события устройства, текущий стек переменных, отладка ну и прочие средства IDE (контроль синтаксиса и т.д.)

Порядок работы такой:

1.В оффлайн обработчике (пустом) нужно установить флаги, которые перенаправят запросы онлайн-обработчиков на ваш Flask-сервис


.. code-block:: Python

	hashMap.put("py_online_url","http://192.168.1.143:2075");
	hashMap.put("py_online_user","usr");
	hashMap.put("py_online_password","");
	hashMap.put("py_function","test_on_start");

где в первых 3-х строчках указываются параметры доступа к вашему Flask -сервису, в 4й строке указывается произвольное название функции которая будет выполняться на стороне сервера

2. Пишется и запускается скрипт с Flask-сервисом шаблона, приведенного ниже. Поясню содержимое скрипта: запускается Flask сервер в режиме отладки с опубликованной командой POST /set_input/<method>, ваши скрипты (название которого указываются в обработчиках) пишутся и отлаживаются в функциях с соответствующими именами, класс hashMap имитирует аналогичный Java-класс в реальных обработчиках, остальное – парсинг и упаковка ответов в том виде, который требуется Simple UI


.. code-block:: Python


	from flask import Flask
	from flask import request
	import json
	app = Flask(__name__)
	def test_on_start():
	    #тело обработчика
    	
	    b = int(hashMap.get('a'))
	    b = b+5550
	    hashMap.put('online_a',str(b))
	
	def test_on_input():
	    #тело обработчика
    	
	    b = hashMap.get('barcode')
	    b+=' - это штрихкод'
	    hashMap.put('online_barcode',str(b))    
	
  	
	@app.route('/set_input/<method>', methods=['POST']) 
	def set_input(method):
	    func = request.args.get('function')
	    jdata = json.loads(request.data.decode("utf-8"))
	    f = globals()[func]
	    hashMap.d=jdata['hashmap']
	    f()
	    jdata['hashmap'] = hashMap.export()
	    jdata['stop'] =False
	    jdata['ErrorMessage']=""
	    jdata['Rows']=[]
	
	    return json.dumps(jdata)
	
	class hashMap:
	    d = {}
	    def put(key,val):
	        hashMap.d[key]=val
	    def get(key):
	        return hashMap.d.get(key)
	    def remove(key):
	        if key in hashMap.d:
	            hashMap.d.pop(key)
	    def containsKey(key):
	        return  key in hashMap.d  
	    def export():
	        ex_hashMap = []
	        for key in hashMap.d.keys():
	            ex_hashMap.append({"key":key,"value":hashMap.d[key]})
	        return ex_hashMap     
	
	if __name__ == '__main__':
	    app.run(host='0.0.0.0', port=2075,debug=True)    

3.	Далее по событиям в приложении запускаются нужные функции, их можно проходить в отладке и довести до кондиции. Потом перенести на закладки обработчиков

.. note:: Кстати, эту конструкцию можно использовать не только для отладки а например для того чтобы сделать **общий для всех устройств сервер на Python**, для исполнения онлайн, совместной работы, API к совместному хранилищу и другие применения 

