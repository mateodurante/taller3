import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import json
import ast
import requests
import Queue
import sys
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

qmsg = Queue.Queue()

class AESCipher(object):

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

key = "1234567890ABCDEF"
key += sys.argv[1] #SSID PASSWORD FOR SALT KEY ENCRYPTION
print key
cipher=AESCipher(key)

def decrypt_aes256(encypted_msg):
    try:
        encypted_msg = encypted_msg.decode("utf-8")
        msg_aes256 = cipher.decrypt(encypted_msg)
        #print("MSG decrypted TYPE: {}".format(type(msg_aes256)))
        #print("MSG decrypted STR: {}".format(str(msg_aes256)))
        return msg_aes256
    except Exception as e:
        print("Exception i decrypt_aes256: {}".format(str(e)))
        #raise

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
        actions = Queue.Queue()

    def get_actions_queue(self):
        return self.actions

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(message, topic):
         #print("Sending %s " % (message))
         publish.single(str(topic), message, hostname="localhost")
         return "Sending msg: %d " % (message)

if __name__ == "__main__":
    #print "Starting MQTT"
    mqtt = MqttClient()
    #mqtt.client.loop_start()
    topic = raw_input("Topic: ") or "test/topic"
    print("Subscribing to topic: " + str(topic))
    time.sleep(5)
    mqtt.client.subscribe(topic)
    mqtt.client.loop_forever()

