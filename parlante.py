
#from playsound import playsound
#playsound('sonidos/big bang.mp3')
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import sys
from vlc import Instance
import os

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
        self.mqtt.client.subscribe("parlante"+str(numero), qos=1)

        self.instance = Instance()
        self.mediaplayer = None
        self.media = None

        self.modo = None
        self.sonido = None

    def on_message(self, client, userdata, msg):
        # hay un cambio
        print(str(msg.payload))
        comando, modo, volumen, sonido = str(msg.payload).split(':')
        self.analizar_mensaje(comando, modo, sonido, volumen)
    
    def cambiar_era(self):
        self.play("Cambio.mp3", 30)
        time.sleep(3)
        self.stop()
        self.play(self.sonido, self.volumen)

    def analizar_mensaje(self, comando, modo, sonido, volumen):
        if comando:
            self.comando = comando
            self.modo = modo
            self.sonido = sonido
            self.volumen = volumen
            if comando == 'set_volume':
                self.set_vol(volumen)
            elif comando == 'cambio_era':
                self.cambiar_era()
            elif comando == 'reset':
                self.stop()
            elif comando == 'loop':
                self.play(self.sonido, self.volumen, loop=True)

    def set_vol(self, vol):
        if self.mediaplayer:
            #self.vlc.audio_set_volume(int(vol))
            self.mediaplayer.audio_set_volume(50)

    def stop(self):
        if self.mediaplayer:
            self.mediaplayer.stop()

    def play(self, sonido, volumen, loop=False): # HACER LOOP
        if self.mediaplayer:
            self.mediaplayer.stop()
        #self.vlc = vlc.MediaPlayer(self.path_sonidos+sonido)
        self.mediaplayer = self.instance.media_player_new()
        self.media = self.instance.media_new(self.path_sonidos+sonido)
        self.mediaplayer.set_media(self.media)
        self.set_vol(volumen)
        self.mediaplayer.play()


if __name__ == "__main__":
    config_file = 'config.txt'
    if os.path.exists(config_file):
        f = open(config_file,"r")
        ip, nro = f.read().split(' ')
        parlante = str(int(nro))
        print("usando ip",ip)
        print("soy parlante", int(parlante))
    else:
        ip = raw_input('Que IP es el servidor? Ingresa la IP: ')
        parlante = raw_input('Que parlante sos? Ingresa un numero: ')
    p = Parlante(parlante, MqttClient(ip))
    p.mqtt.client.loop_forever()
