from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import json
import threading
import time
from components.buzz import change_buzz, run_buzz
# from components.LCD1602 import set_text, loop
from settings import load_settings


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883

INFLUXDB_HOSTNAME = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_ORGANISATION = "FTN"
INFLUXDB_BUCKET = "iot_bucket"
# INFLUXDB_TOKEN_D = "9MShUWSH6ZXieeLFpRTUiBMl83Y37xyRmmC9w1O6hZN0PEUgDB3l_-LrLaVMoIMVgiQNXikIuhcQadR5bqUqXw=="
INFLUXDB_TOKEN_M = "O-rpPmvuYpaFJYp2kiJE15pGlRQqta80KCbUL13sdjD5MbAnjoBZn9HHrGT9EDVoAygtjxnVCQ_4mb4xlfMbZA=="

# InfluxDB Configuration
token = INFLUXDB_TOKEN_M
org = INFLUXDB_ORGANISATION
url = f"http://{INFLUXDB_HOSTNAME}:{INFLUXDB_PORT}"
bucket = INFLUXDB_BUCKET
influxdb_client = InfluxDBClient(url=url, token=token, org=org)


# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_HOSTNAME, MQTT_PORT, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe("Temperature")
    mqtt_client.subscribe("Humidity")
    mqtt_client.subscribe("LED")
    mqtt_client.subscribe("Buzz")
    mqtt_client.subscribe("PIR")
    mqtt_client.subscribe("UDS")
    mqtt_client.subscribe("DS")
    mqtt_client.subscribe("DMS")
    mqtt_client.subscribe("B4SD")
    print("connected")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))

dus1_values = []
persons = 0
alarm = False
PIN = "1234"
active = False
APIN = "1234"

settings = load_settings()

def activate():
    time.sleep(6)
    global active
    active = True
    socketio.emit('active', { "value": active })

def save_to_db(data):
    print(data)
    try:
        write_sensor_to_influx(data)
        sensor = data["name"]
        global active
        print(f"activeee {active}")
        if active == False and sensor != "DMS":
            return
        elif active == False and sensor == "DMS":
            pin = data["value"]
            
            if pin != APIN:
                return
            else:
                active = True
                active_thread = threading.Thread(target=activate)
                active_thread.start()
        else:
            if sensor == "DL":
                handle_DL(data)
            if sensor == "DPIR1":
                handle_DPIR1(data)
            if sensor == "DUS1":
                handle_dus1(data)
            if sensor == "DS1" or sensor == "DS2":
                handle_ds(data)
            if sensor == "DMS":
                handle_dms(data)
            if sensor in ["RPIR1", "RPIR2", "RPIR3", "RPIR4"]:
                handle_rpir(data)
            if sensor == "GDHT":
                handle_gdht(data)
            if sensor == "B4SD":
                handle_b4sd(data)

    except:
        print("losa poruka")

def handle_DPIR1(data):

    if data["value"] == 0:
        return
    
    global dus1_values
    global persons

    last_three = dus1_values[-3:]
    print(dus1_values)
    print(last_three)

    asc = all(last_three[i] < last_three[i + 1] for i in range(len(last_three) - 1))
    desc = all(last_three[i] > last_three[i + 1] for i in range(len(last_three) - 1))

    if asc:
        print("POVECAOOOO")
        persons += 1
    if desc:
        persons -= 1

    socketio.emit('DPIR1', { "value": data["value"] })
    socketio.emit('persons', { "value": persons })

def handle_DL(data):
    socketio.emit('DL', { "value": data["value"] })

def handle_dus1(data):
    value = data["value"]
    global dus1_values

    if len(dus1_values) == 0:
        dus1_values = [value, value, value]
    else:
        dus1_values.append(value)
    
    socketio.emit('DUS1', { "value": value })

def handle_ds(data):
    value = data["value"]
    name = data["name"]
    global alarm
    global settings

    if value > 4.5 and alarm == False:
        alarm = True
        change_buzz(True, False)
        socketio.emit("DB", { "value": 1 })
        print("POSLAO")
        run_buzz(settings["DB"])
        # treba da se doda za BB

        socketio.emit(name, { "value": value })
        socketio.emit("alarm", { "value": alarm })
        write_alarm_to_influx({ "value": 1 })

def handle_dms(data):
    pin = data["value"]
    global alarm

    if pin == PIN:
        alarm = False
        socketio.emit("alarm", { "value": alarm })
        write_alarm_to_influx({ "value": 0 })
        change_buzz(False, True)
        socketio.emit("DB", { "value": 0 })

def handle_rpir(data):
    value = data["value"]
    name = data["name"]
    global alarm
    global settings
    global persons

    if alarm == False and value == 1 and persons == 0:
        print("u alaram")
        alarm = True
        change_buzz(True, False)
        socketio.emit("DB", { "value": 1 })
        run_buzz(settings["DB"])
        # treba da se doda za BB

        socketio.emit(name, { "value": value })
        socketio.emit("alarm", { "value": alarm })
        write_alarm_to_influx({ "value": 1 })

def handle_gdht(data):
    value = data["value"]
    measurement = data["measurement"]
    if measurement == "Temperature":
        socketio.emit("GDHT-temp", { "value": value })
        # set_text(f"T-{value}") # za dodavanje na pravi LCD. ne znam da li radi
    if measurement == "Humidity":
        socketio.emit("GDHT-hum", { "value": value })
        # set_text(f"H-{value}")

def handle_b4sd(data):
    value = data["value"]
    socketio.emit("B4SD", { "value": value })
    
def write_sensor_to_influx(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("pi", data["pi"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)

def write_alarm_to_influx(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point("alarm")
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)
    
def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10mo)"""
    return handle_influx_query(query)

@app.route('/proba', methods=['GET'])
def proba():
    socketio.emit('probaSaServera', {"kljuc": "podaci"})
    return jsonify({"status": "success"})

@app.route('/alarm_pin', methods=['POST'])
def alarm_pin():
    request_data = request.get_json()
    pin = request_data["pin"]

    global alarm
    global active

    if pin == PIN:
        alarm = False
        active = False
        socketio.emit("alarm", { "value": alarm })
        socketio.emit("active", { "value": active })
        write_alarm_to_influx({ "value": 0 })
        change_buzz(False, True)
        socketio.emit("DB", { "value": 0 })

    return jsonify({"status": "success"})

@app.route('/activate_pin', methods=['POST'])
def activate_pin():
    request_data = request.get_json()
    pin = request_data["pin"]

    global active

    if pin == APIN:
        active = True
        socketio.emit("active", { "value": active })

    return jsonify({"status": "success"})


@socketio.on('connect')
def on_connect():
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print("User disconnected")

@socketio.on('probaNaServer')
def messaging(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False, port=8088)
    socketio.run(app, debug=True, use_reloader=False)
