from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json


app = Flask(__name__)

MQTT_HOSTNAME = "localhost"
MQTT_PORT = 1883

INFLUXDB_HOSTNAME = "localhost"
INFLUXDB_PORT = 8086
INFLUXDB_ORGANISATION = "FTN"
INFLUXDB_BUCKET = "iot_bucket"
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
    print("connected")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))


def save_to_db(data):
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


if __name__ == '__main__':
    app.run(debug=True)
