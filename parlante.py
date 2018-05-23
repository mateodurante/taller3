
#from playsound import playsound
#playsound('sonidos/big bang.mp3')
import time
from mqtt_reducido import MqttClient
import sys

class Parlante:

    def __init__(self, numero):
        self.path_sonidos = 'sonidos/'
        self.sonidos = [""]

        self.mqtt = MqttClient()
        self.mqtt.client.on_message = self.on_message
        self.mqtt.client.subscribe("parlante"+str(numero))

        self.vlc = None

        self.modo = None
        self.sonido = None

    def on_message(self, client, userdata, msg):
        # hay un cambio
        print(str(msg.payload))
        modo, sonido = str(msg.payload).split(':')
        self.analizar_mensaje(modo, sonido)

    def analizar_mensaje(self, modo, sonido):
        self.modo = modo
        self.sonido = sonido
        if modo:
            if "bajo" in modo:
                self.set_vol(0.3)
            elif "alto" in modo:
                self.set_vol(0.8)
            self.play(sonido)

    def set_vol(self, vol):
        self.vlc.mixer.music.set_volume(vol)

    def play(self, sonido):
        self.vlc = vlc.MediaPlayer(self.path_sonidos+sonido)
        self.vlc.play()


if __name__ == "__main__":
    nro = raw_input('Que parlante sos? Ingresa un numero: ')
    p = Parlante(nro)
    p.mqtt.client.loop_forever()
