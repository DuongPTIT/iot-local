import paho.mqtt.client as mqtt
import time
import json
from random import seed
from random import randint
seed(1)

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print('on_publish')


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def send_data_from_bound_device():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.connect("localhost", 1883, 60)
    mqttc.loop_start()

    dataindata = {
        "may01": {"status": "RUN", "period": randint(0, 1000), "product": randint(0, 1000),
                  "power": randint(0, 1000)},
        "may02": {"status": "OFF", "period": randint(0, 1000), "product": randint(0, 1000),
                  "power": randint(0, 1000)},
        "may03": {"status": "ON", "period": randint(0, 1000), "product": randint(0, 1000),
                  "power": randint(0, 1000)},
        "may04": {"status": "ON", "period": randint(0, 1000), "product": randint(0, 1000),
                  "power": randint(0, 1000)}
    }

    data = {
        'messagetype': 3,
        "factory_id": "rostek",
        "timestamp": int(time.time()),
        "data": dataindata
    }
    payload = json.dumps(data)
    while 1:
        mqttc.publish("topic", payload, qos=0)
        print('Publishing message: \'{}\' to {}'.format(payload, "topic"))
        time.sleep(1)


send_data_from_bound_device()