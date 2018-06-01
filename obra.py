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
            '1-moderno.mp3',
            '2-guerra.mp3',
            '3-revolucion.mp3',
            '4-medieval.mp3',
            '5-dino.mp3',
            '6-bigbang.mp3',
        ]
        self.sonido_glitch1 = "Glitch.mp3"
        self.sonido_glitch2 = "Glitch 2.mp3"
        self.sonido_cambio = "Cambio.mp3"
        

    def on_message(self, client, userdata, msg):
        # hay un cambio
        print(str(msg.payload))
        camara, estado = str(msg.payload).split(':')
        print(camara, type(camara))
        print(estado, type(estado))
        if '0' == estado:
            # es estado apagado
            pass
        elif '1' == estado:
            self.mov_en(int(camara))
        elif 'reset' == camara:
            self.__init__()
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
        self.set_parlantes(self.parlantes[1:]+self.parlantes[:1], comando="cambio_era")
    
    def set_estado_regresion_desde_inicial(self):
        self.era = 0
        self.estado = "regresion"
        self.set_parlantes(["ruido_bajo","sonido_bajo","sonido_alto","ruido_alto"], comando="cambio_era")

    def sonido_en(self, modo_sonido):
        if modo_sonido in ["ruido_bajo", "ruido_alto"]:
            return self.sonido_glitch1
        elif modo_sonido in ["sonido_alto", "sonido_bajo"]:
            return self.eras[self.era]
    
    def volumen_en(self, modo_sonido):
        if modo_sonido in ["ruido_bajo", "sonido_bajo"]:
            return 30
        elif modo_sonido in ["sonido_alto", "ruido_alto"]:
            return 70

    def set_parlantes(self, p, comando="reset"):
        self.parlantes = p
        for i in range(0,4):
            self.mqtt.publish(
                "%s:%s:%s:%s" % (
                    comando,
                    self.parlantes[i],
                    self.volumen_en(self.parlantes[i]),
                    self.sonido_en(self.parlantes[i])
                ), "parlante%d" % i)
    
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
            #if self.usuario_en == self.regresion_perdida_en:
            #    self.set_estado_regresion_desde_avance()
            if self.usuario_en == (self.regresion_perdida_en + 1)%4:
                self.estado = "regresion"
                self.set_siguiente_era()
            #else:
            #    self.potenciar_avance()
    
    def mostrar_estados(self):
        self.mqtt.publish("%s\n%s, %s, %s" % (self.estado, self.usuario_en, self.usuario_viene_de, self.regresion_perdida_en), "estado")
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
