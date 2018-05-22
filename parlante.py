
#from playsound import playsound
#playsound('sonidos/big bang.mp3')
import pygame
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

        self.pygame = pygame
        self.pygame.init()

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
        self.pygame.mixer.music.set_volume(vol)
            
    def play(self, sonido):
        self.pygame.mixer.music.load(self.path_sonidos+sonido)
        self.pygame.mixer.music.play()


if __name__ == "__main__":
    p = Parlante(sys.argv[1])
    p.mqtt.client.loop_forever()
