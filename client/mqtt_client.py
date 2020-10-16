import random
import paho.mqtt.client as mqtt
import time
import json

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
        data = {"may01": {"status": "RUN", "period": random.randint(0, 100), "product": random.randint(0, 100), "power": random.randint(0, 100)}}
        payload = json.dumps(data)
        mqttc.publish("topic4", payload, qos=0)
        print('Publishing message: \'{}\' to {}'.format(payload, "topic4"))
        time.sleep(5)


send_data_from_bound_device()
