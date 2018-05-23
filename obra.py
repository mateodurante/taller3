from mqtt_reducido import MqttClient


class Obra:

    def __init__(self):
        self.estado = "inicial"
        self.usuario_en = -1
        self.usuario_viene_de = -1

        self.regresion_perdida_en = -1

        self.camaras   = [0,0,0,0]

        self.mqtt = MqttClient()
        self.mqtt.client.on_message = self.on_message
        self.mqtt.client.subscribe("camaras")
        self.set_parlantes(["","","",""])


        self.era = -1
        self.eras = [
            '2da guerra mundial.mp3',
            'big bang.mp3',
            'ciudad moderna.mp3',
            'computadora futurista.mp3',
            'construccion antigua.mp3',
            'construccion moderna.mp3',
            'dinosaurios.mp3',
            'discurso peron.mp3',
            'guerra medieval.mp3',
            'hittler.mp3',
            'primera civilizacion charla prehistorica.mp3',
        ]
        self.glitch = "glitchs varios.mp3"

    def on_message(self, client, userdata, msg):
        # hay un cambio
        print(str(msg.payload))
        camara, estado = str(msg.payload).split(':')
        print(camara, type(camara))
        print(estado, type(estado))
        if '0' == estado:
            # es estado apagado
            pass
        else:
            self.mov_en(int(camara))
        print(camara, estado)

        self.mostrar_estados()
            
    def mov_en(self, nro_cam):
        if self.usuario_en != nro_cam:
            self.usuario_viene_de = self.usuario_en
            self.usuario_en = nro_cam
            self.procesar_cambio_de_zona()
    
    def set_siguiente_era(self):
        if self.era < len(self.eras):
            self.era += 1
            self.do_rotacion()

    def do_rotacion(self):
        self.set_parlantes(self.parlantes[1:]+self.parlantes[:1])
    
    def set_estado_regresion_desde_inicial(self):
        self.era = 0
        self.estado = "regresion"
        self.set_parlantes(["ruido_bajo","sonido_bajo","sonido_alto","ruido_alto"])

    def sonido_en(self, modo_sonido):
        if modo_sonido in ["ruido_bajo", "ruido_alto"]:
            return self.glitch
        elif modo_sonido in ["sonido_alto", "sonido_bajo"]:
            return self.eras[self.era]
    
    def volumen_en(self, modo_sonido):
        if modo_sonido in ["ruido_bajo", "sonido_bajo"]:
            return 30
        elif modo_sonido in ["sonido_alto", "ruido_alto"]:
            return 70

    def set_parlantes(self, p):
        self.parlantes = p
        self.mqtt.publish(
            "%s:%s:%s" % (
                self.parlantes[0],
                self.volumen_en(self.parlantes[0]),
                self.sonido_en(self.parlantes[0])
            ), "parlante0")
        self.mqtt.publish(
            "%s:%s:%s" % (
                self.parlantes[1],
                self.volumen_en(self.parlantes[1]),
                self.sonido_en(self.parlantes[1])
            ), "parlante1")
        self.mqtt.publish(
            "%s:%s:%s" % (
                self.parlantes[2],
                self.volumen_en(self.parlantes[2]),
                self.sonido_en(self.parlantes[2])
            ), "parlante2")
        self.mqtt.publish(
            "%s:%s:%s" % (
                self.parlantes[3],
                self.volumen_en(self.parlantes[3]),
                self.sonido_en(self.parlantes[3])
            ), "parlante3")
    
    def set_estado_regresion_desde_avance(self):
        self.regresion_perdida_en = -1
        self.estado = "regresion"
    
    def procesar_cambio_de_zona(self):
        if self.estado == "inicial":
            if self.usuario_en == 0:
                # Creemos que entro por el lado correcto, comienza la obra
                self.set_estado_regresion_desde_inicial()
        elif self.estado == "regresion":
            if self.usuario_en == (self.usuario_viene_de + 1)%4:
                # el usuario avanzo a la siguiente zona, hago rotacion y cambio de ERA
                self.set_siguiente_era()
            else:
                self.regresion_perdida_en = self.usuario_viene_de
                self.estado = "avance"
        elif self.estado == "avance":
            if self.usuario_en == self.regresion_perdida_en:
                self.set_estado_regresion_desde_avance()
            #else:
            #    self.potenciar_avance()
    
    def mostrar_estados(self):
        print("estado:",self.estado)
        print("usuario_en:",self.usuario_en)
        print("usuasrio_viene_de:",self.usuario_viene_de)
        print("regresion_perdida_en",self.regresion_perdida_en)
        print("camaras:",self.camaras)
        print("parlantes:",self.parlantes)
        print("era:",self.era)
        print("eras:",self.eras)


if __name__ == "__main__":
    o = Obra()
    o.mqtt.client.loop_forever()
