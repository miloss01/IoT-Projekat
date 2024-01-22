from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
import json
from components.led import run_led


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
    mqtt_client.subscribe("DS1")
    mqtt_client.subscribe("DMS")
    print("connected")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))

dus1_values = []
persons = 0

def save_to_db(data):
    print(data)
    try:
        write_sensor_to_influx(data)
        sensor = data["name"]

        if sensor == "DL":
            handle_DL(data)

        if sensor == "DPIR1":
            handle_DPIR1(data)

        if sensor == "DUS1":
            handle_dus1(data)

    except:
        print("losa poruka")

def handle_DPIR1(data):
    socketio.emit('DPIR1', { "value": data["value"] })

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
    
    socketio.emit('DUS1', { "value": data["value"] })
    
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

# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
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
