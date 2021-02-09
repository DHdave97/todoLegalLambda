# Librerias
from flask import Flask, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
import requests
from time import time, sleep

# URL DEL WEB HOOK
webhook_url = "https://webhook.site/14693700-0cce4ef4-9961-e927cf90c008"
# URL Dweet
dweet_url   = "https://dweet.io/get/latest/dweet/for/thecore"

app = Flask(__name__)

# URI database mongo by dave 
# El usuario '''tlegal''' estará disponible hasta mañana miercoles (24:00), despues será eliminado automáticamente de la BDD
app.config['MONGO_URI']='mongodb+srv://tlegal:tlegal@cluster0-yxxsk.mongodb.net/todoLegal'

# iniciar mongo
mongo = PyMongo(app)

timer = 0
max_time = 15

# Guardar tem y humidity
saveTH = lambda tem,hum:mongo.db.tems_hums.insert({"temperature":tem,"humidity":hum})
# Enviar webhook
sendWH = lambda response:requests.post(webhook_url, data=response,headers={'Content-Type': 'application/json'})

# OBTENER TEM Y HUMIDITY
def consult(): 
    res = requests.get(dweet_url)
    body = json.loads(res.content)
    return saveTH(body['with'][0]['content']['temperature'],body['with'][0]['content']['humidity'])

# OBTENER TODO
@app.route('/tems_hums', methods=['GET'])
def get_all():
    ths =  mongo.db.tems_hums.find()
    response = json_util.dumps(ths)
    return Response(response, mimetype="application/json")

# MAIN
while timer <= max_time:
    if timer >= max_time:
        res = sendWH(json_util.dumps(mongo.db.tems_hums.find()))
        print("WH response: ")
        print(res)
    else:
        id_saved = consult()
        print("guardado: "+str(id_saved))
    if timer < max_time - 1:
        sleep(60 - time() % 60)
    timer = timer + 1

if __name__ == "__main__":
    app.run(debug=True)
    
