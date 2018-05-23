
#from playsound import playsound
#playsound('sonidos/big bang.mp3')
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import sys
import vlc

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
    def __init__(self, ip, client=mqtt.Client()):
        super(MqttClient, self).__init__()
        self.client = client
        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.ip = ip
        self.client.connect(self.ip, 1883, 60)

    def get_actions_queue(self):
        return self.actions

    def get_client(self):
        return self.client

    def set_on_connect(self, func):
        self.on_connect = func

    def publish(self, message, topic):
         #print("Sending %s " % (message))
         publish.single(str(topic), message, hostname=self.ip)
         return "Sending msg: %s " % (message)


class Parlante:

    def __init__(self, numero, mqtt):
        self.path_sonidos = 'sonidos/'
        self.sonidos = [""]

        self.mqtt = mqtt
        self.mqtt.client.on_message = self.on_message
        self.mqtt.client.subscribe("parlante"+str(numero))

        self.vlc = None

        self.modo = None
        self.sonido = None

    def on_message(self, client, userdata, msg):
        # hay un cambio
        print(str(msg.payload))
        modo, volumen, sonido = str(msg.payload).split(':')
        self.analizar_mensaje(modo, sonido, volumen)

    def analizar_mensaje(self, modo, sonido, volumen):
        self.modo = modo
        self.sonido = sonido
        self.volumen = int(volumen)
        if modo:
            self.play(sonido, volumen)

    def set_vol(self, vol):
        if self.vlc:
            self.vlc.audio_set_volume(int(vol))

    def play(self, sonido, volumen):
        self.vlc = vlc.MediaPlayer(self.path_sonidos+sonido)
        self.set_vol(volumen)
        self.vlc.play()


if __name__ == "__main__":
    ip = raw_input('Que IP es el servidor? Ingresa la IP: ')
    nro = raw_input('Que parlante sos? Ingresa un numero: ')
    p = Parlante(nro, MqttClient(ip))
    p.mqtt.client.loop_forever()
