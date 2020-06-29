# Librerias utilizadas
from configuracion import*      # Constantes de configuracion
from brokerData import *        #Informacion de la conexion
import paho.mqtt.client as mqtt # Libreria MQTT
import threading                # Concurrencia con hilos
import datetime                 # Para generar fecha/hora actual
import binascii                 # Conversion con binarios/ascii
import logging                  # Logging
import time                     # Retardos
import sys                      # Requerido para salir (sys.exit())
import os                       # Ejecutar comandos de terminal
#########################################################################################################
logging.basicConfig(                            #EAMA Configuracion inicial para logging.
    level = logging.DEBUG,                      #  logging.DEBUG muestra todo. ############## cambiar antes de entrega a .info
    format = '[%(levelname)s] %(message)s'
    )

class Cliente(object):
    def __init__(self):                                     # LFMV Configuracion inicial del cliente
        logging.info("Conexion exitosa cliente MQTT")       # LFMV Mensaje inicial
        
    def Suscribe(self):
        for i in range(len(self.Documento(SALAS))):             # WAIG Subscripcion a salas (topic,qos)
            sala=self.Documento(SALAS)[i].split("s")            # WAIG Separa el numero de grupo con el numero de sala
            topic=str("salas/"+str(sala[0])+"/s"+str(sala[1]))  # WAIG Concatena el topic
            client.subscribe((topic, qos))                      # WAIG Realiza la suscripcion al topic indicado
            logging.info("Suscripcion a: "+topic)               # WAIG Indica la sala suscrita

        for i in range(1,len(self.Documento(USUARIO))):             # WAIG Subscripcion a usuarios (topic,qos)
            topic=str("usuarios/"+str(self.Documento(USUARIO)[0]))  # WAIG Topic para comunicacion entre usuarios
            client.subscribe((topic, qos))                          # WAIG Suscribe al id del cliente
            logging.info("Suscripcion a: "+topic)                   # WAIG Indica la suscripcion del cliente
            #topic=str("comandos/"+str(Grupo)+"/"+str(self.Documento(USUARIO)[0]))  # WAIG Topic para comunicacion con el servidor
            #client.subscribe((topic, qos))                          # WAIG Suscribe al id del cliente
            #logging.info("Suscripcion a: "+topic)                   # WAIG Indica la suscripcion del cliente
        client.loop_start()                                         # LFMV inicia el hilo para la recepcion de mensajes de mqtt
    
    def Disconect(self):                                # LFMV Desconectar del broker
        print('\n')
        client.loop_stop()                              # LFMV Se mata el hilo que verifica los topics en el fondo
        client.disconnect()                             # LFMV Se desconecta del broker
        logging.info("Se ha desconectado del broker.")  # LFMV Indica al cliente que se desconecto del broker
        logging.info("Saliendo de la Aplicacion...")    # LFMV Indica al cliente que se esta saliendo de la aplicacion

    def publishData(self,topic, value, retain = False): # LFMV Funcion para publicar 
        client.publish(topic, value, QoS, retain)       # LFMV Publica el topic con las caracteristicas indicadas

    def sendALIVE(self,recibido=False, retain = False):              # EAMA Funcion para publicar ALIVE
        i = 0                                                   # EAMA Control de pulsos enviados
        send=True
        aux = 0                                                 # EAMA Contador de segundos transcurridos
        while send:
            topic='comandos/'+str(Grupo)+'/'+self.Documento(USUARIO)[0]  # EAMA topic para enviar Alive
            val=ALIVE+b'$'+self.Documento(USUARIO)[0].encode("utf-8")       # EAMA Concatena caracteres en binario
            client.publish(topic, val, QoS, retain)             # EAMA Publica el Alive en el topic indicado
            logging.debug("Alive Enviado. "+str(i))             # EAMA Indica en pantalla que se envio el Alive
            print(aux)
            if(recibido==True):                                 # EAMA si recibe un Ack
                time.sleep(ALIVE_PERIOD)                        # EAMA Delay normal de 2 segundos
                i=0                                             # Reinicia el contador de "pulsos"
            elif (i<3):                                         # EAMA Cuenta 3 periodos de Alive si no recibe ack
                time.sleep(ALIVE_PERIOD)                        # EAMA Delay normal de 2 segundos
                i+=1                                            # EAMA aumenta el contador de Alives
                aux+=ALIVE_PERIOD
            elif(i>=3 and i<203 and recibido ==False):          # EAMASi no recibio un Ack en 20 periodos continuos
                time.sleep(ALIVE_CONTINUO)                      # EAMA Delay de 0.1 segundos
                i+=1                                            # EAMA aumenta el contador de Alives
                aux+=ALIVE_CONTINUO
            else:                                               # EAMA  en caso de no recibir un Ack en 20 periodos continuos
                print('\n')
                logging.critical("No se puede establecer conexion con el servidor.")
                logging.critical("Saliendo de la Aplicacion...")
                #sys.exit()  # Matamos el hilo
                break
        sys.exit()    # EAMA Al utilizarlo el main principal sigue en ejecucion

    def sendFTR(Filsize, retain = False):                                           # LFMV Funcion para enviar archivo
        topic = 'comandos/'+str(Grupo)+'/'+usuario()[0]                             # LFMV Concatena el topic
        val = FTR+b'$'+usuario()[0].encode("utf-8")+b'$'+Filsize.encode("utf-8")    # LFMV Concatena el payload
        client.publish(topic, val, QoS, retain)                                     # LFMV Realiza la publicacion

    def Documento(self,fileName = 'salas.txt'): # WAIG Lectura de Usuario y Salas
        datos=[]
        archivo = open(fileName,'r')            # WAIG Abre el archivo en modo de LECTURA
        for i in archivo:                       # WAIG Lee cada linea del archivo
            linea = i                           # WAIG Separa cada dato luego de una coma
            linea = linea.replace('\n', '')     # WAIG Se remplaza el ultimo salto de linea
            datos.append(linea)                 # WAIG Se agrega el dato a la lista
        archivo.close()                         # WAIG Cerrar el archivo al finalizar
        return datos                            # WAIG Se regresa una lista con los archivos

def on_connect(client, userdata, flags, rc):    # Handler si sucede la conexion con el broker MQTT
    print('\n')
    connectionText = "CONNACK recibido del broker con codigo: " + str(rc)   
    logging.debug(connectionText)

def on_publish(client, userdata, mid):          # Handler si se publica satisfactoriamente
    publishText = "Publicacion satisfactoria."
    logging.debug(publishText)

def on_message(client, userdata, msg):          # Handler si se recibe un mensaje
    print('\n')
    menm = str(msg.payload)
    topic_recibido = 'Mensaje entrante del topic ' + str(msg.topic) + ': ' +  menm.replace("b","")
    logging.info(topic_recibido)
    logging.info("El contenido del mensaje es: " + str(msg.payload)) #LFMV Muestra el mensaje de texto recibido

client = mqtt.Client(clean_session=True)            # LFMV Nueva instancia de cliente
client.on_connect = on_connect                      # LFMV Se configura la funcion "Handler" cuando suceda la conexion
client.on_message = on_message                      # LFMV Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.on_publish = on_publish                      # LFMV Se configura la funcion "Handler" que se activa al publicar algo
client.username_pw_set(MQTT_USER, MQTT_PASS)        # LFMV Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT)    # LFMV Conectar al servidor remoto
##########################################################################################################
class OutputError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return str("No hay elementos en la lista de datos")

    def __repr__(self):
        return self.__str__()   



#               Configuracion HILOS
"""
class Grabar(threading.Thread):
    def __init__(self, name,tiempo):
        threading.Thread.__init__(self)
        self.name = name
        self.tiempo = tiempo
 
    def run(self):
        print("\n")
        logging.info('Iniciando grabacion')
        os.system('arecord -d '+str(self.tiempo)+' -f U8 -r 8000  '+self.name+'.wav')
        logging.info('Grabacion finalizada. Iniciando envio.')

class Reproducir(threading.Thread): # Hilo para reproduccion de audio
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
  
    def run(self):
        print("\n")
        logging.info('Iniciando reproduccion de audio')
        os.system('aplay '+self.name+'.wav')
        logging.info('El mensaje se ha terminado de reproducir.')

nombre = str(datetime.datetime.now().ctime())    # Nombre de audio con timestamp
nombre = nombre.replace(" ","_")  # Eliminando espacios del nombre
t=Grabar(nombre,5)
t.start()
t.join()
y=Reproducir(nombre)
y.start() 
"""


###################################################################################################3
#               HILO PRINCIPAL
#recibido = False
#AliveTh = threading.Thread(name = 'ALIVE',
#                        target = sendALIVE,
#                        args = (recibido,),
#                        daemon = False
#                        )


