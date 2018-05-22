import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import json
import ast
import requests
import sys
import base64
import hashlib


def on_connect(client, userdata, flags, rc):
    print("[+] Running: on_connect")
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print("[+] Running: on_message")
    print("client " + str(client))
    print("userdata " + str(userdata))
    print("msg " + str(msg))
    print("msg.payload " + str(msg.payload) + "\n")


def on_subscribe(client, userdata, mid, granted_qos):
    print("[+] Running: on_subcribe")
    print("client : " +str(client))
    print("userdata : " +str(userdata))
    print("mid : " +str(mid))
    print("granted_qos : " +str(granted_qos))

def on_publish(mosq, obj, mid):
    print("[+] Running: on_publish")
    print("mosq: " + str(mosq))
    print("obj: " + str(obj))
    print("mid: " + str(mid))

class MqttClient(object):
    """docstring for MqttClient."""
    def __init__(self, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.connect("localhost", 1883, 60)

    def get_actions_queue(self):
        return self.actions

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(self, message, topic):
         #print("Sending %s " % (message))
         publish.single(str(topic), message, hostname="localhost")
         return "Sending msg: %s " % (message)

# if __name__ == "__main__":
#     #print "Starting MQTT"
#     mqtt = MqttClient()
#     #mqtt.client.loop_start()
#     topic = raw_input("Topic: ") or "test/topic"
#     print("Subscribing to topic: " + str(topic))
#     time.sleep(5)
#     mqtt.client.subscribe(topic)
#     mqtt.client.loop_forever()

