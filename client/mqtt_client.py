import json
import random
import time

import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print('on_publish')


def on_disconnect(mqttc, obj, mid):
    print('on_disconnect')


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)


def send_data_from_bound_device():
    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_disconnect = on_disconnect
    mqttc.on_subscribe = on_subscribe
    mqttc.connect("localhost", 1883, 65535)
    mqttc.loop_start()

    while 1:
        id_user = random.randint(0, 1000000)
        payload = {"id": id_user, "firstName": "Mai", "lastName": "Pham Thi Thu", "email": "mai@gmail.com"}
        data = {
            "schema": {
                "type": "struct",
                "fields": [
                    {
                        "type": "string",
                        "optional": True,
                        "field": "payload"
                    },
                    {
                        "type": "string",
                        "optional": True,
                        "field": "eventType"
                    },
                    {
                        "type": "string",
                        "optional": True,
                        "field": "id"
                    }
                ]
            },
            "payload": {
                "payload": str(payload),
                "eventType": "CustomerUpdated",
                "id": str(id_user)
            }
        }
        json_data = json.dumps(data)
        mqttc.publish("topic9", json_data, qos=0)
        print('Publishing message: \'{}\' to {}'.format(json_data, "topic9"))
        time.sleep(5)


send_data_from_bound_device()
