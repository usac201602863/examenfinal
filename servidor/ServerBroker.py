# Librerias utilizadas
from configuracion import*      # EAMA Constantes de configuracion
from brokerData import *        # EAMA Informacion de la conexion
import paho.mqtt.client as mqtt # Libreria MQTT
import threading                # Concurrencia con hilos
import datetime                 # Para generar fecha/hora actual
import binascii                 # Conversion con binarios/ascii
import logging                  # Logging
import time                     # Retardos
import sys                      # Requerido para salir (sys.exit())
import os                       # Ejecutar comandos de terminal
import socket                   # Libreria TCP
###########################################################################################################
#               EAMA Configuracion Broker
logging.basicConfig(    #Configuracion inicial de logging
    level = logging.INFO,   #INFO
    format = '[%(levelname)s] %(message)s'
    )

class Servidor(object):
    def __init__(self):                                     # LFMV Configuracion inicial del cliente
        users=[]
        self.users = users                                  # EAMA Lista que contiene los usuarios activos
        self.client = mqtt.Client(clean_session=True)            # LFMV Nueva instancia de cliente
        self.client.on_connect = self.on_connect                      # LFMV Se configura la funcion "Handler" cuando suceda la conexion
        self.client.on_message = self.on_message                      # LFMV Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
        self.client.on_publish = self.on_publish                      # LFMV Se configura la funcion "Handler" que se activa al publicar algo
        self.client.username_pw_set(MQTT_USER, MQTT_PASS)        # LFMV Credenciales requeridas por el broker
        self.client.connect(host=MQTT_HOST, port = MQTT_PORT)    # LFMV Conectar al servidor remoto
        self.TCPConfig(SERVER, TCP_PORT)                           #LFMV Credenciales requeridas por el sockect TCP
        logging.info("Conexion exitosa cliente MQTT")       # LFMV Mensaje inicial 

    def Suscribe(self):
        for i in range(len(self.Documento(SALAS))):             # WAIG Subscripcion a salas (topic,qos)
            sala=self.Documento(SALAS)[i][0].split("s")         # WAIG Separa el numero de grupo con el numero de sala
            topic=str("salas/"+str(sala[0])+"/s"+str(sala[1]))  # WAIG Concatena el topic
            self.client.subscribe((topic, qos))                      # WAIG Realiza la suscripcion al topic indicado
            logging.info("Suscripcion a: "+topic)               # WAIG Indica la suscripcion al cliente

        for i in range(len(self.Documento(USUARIOS))):      # WAIG Subscripcion a usuarios (topic,qos)
            topic=str('comandos/'+str(Grupo)+'/'+str(self.Documento(USUARIOS)[i][0]))    # WAIG Concatena el topic
            self.client.subscribe((topic, qos))                  # WAIG Realiza la suscripcion al topic indicado
            logging.info("Suscripcion a: "+topic)           # WAIG Infforma al cliente de la suscripcion
        self.client.loop_start()                                 # LFMV inicia el hilo para la recepcion de mensajes de mqtt
    
    def Documento(self,fileName = 'salas'):                  # EAMA Lectura del archivo
        datos=[]
        archivo = open(fileName,'r')                    # WAIG Abre el archivo en modo de LECTURA
        for i in archivo:                               # WAIG Lee cada linea del archivo
            linea=i.split(',')                          # WAIG Separa cada dato luego de una coma
            linea[-1] = linea[-1].replace('\n', '')     # WAIG Se remplaza el ultimo salto de linea
            datos.append(linea)                         # WAIG Se agrega el dato a la lista
        archivo.close()                                 # WAIG Cerrar el archivo al finalizar
        return datos                                    # WAIG Se regresa una lista con los datos del archivo
    
    def Disconect(self):                                # LFMV Desconectar del broker
        print('\n')
        self.client.loop_stop()                              # LFMV Se mata el hilo que verifica los topics en el fondo
        self.client.disconnect()                             # LFMV Se desconecta del broker
        logging.info("Se ha desconectado del broker.")  # LFMV Indica al cliente que se desconecto del broker
        logging.info("Saliendo de la Aplicacion...")    # LFMV Indica al cliente que se esta saliendo de la aplicacion

    def publishData(self,topic, value, retain = False): # LFMV Funcion para publicar 
        self.client.publish(topic, value, QoS, retain)       # LFMV Publica el topic con las caracteristicas indicadas
    
    def on_message(self,client, userdata, msg):         # LFMVCallback que se ejecuta cuando llega un mensaje al topic suscrito
        mensaje=msg.payload.split("$".encode("utf-8"))  # EAMA Se divide la informacion por el caracter especial
        if(mensaje[0]==ALIVE):                          # EAMA Recibe en la trama un ALIVE
            mensaje[1]=mensaje[1].decode("utf-8")       # EAMA Codifica el mensje a modo que pueda ser interpretdo
            logging.debug("Ha llegado el mensaje al topic: " + str(msg.topic))  # EAMA Indica el topic del que llego
            logging.debug("ALIVE recibido de: " + mensaje[1])                   # EAMA Indica la instruccion recibida
            
            topic = "comandos/"+str(Grupo)+"/"+mensaje[1]   # EAMA Topic para enviar ACK de respuesta
            payload = ACK+b'$'+mensaje[1].encode("utf-8")   # EAMA Concatena el payload indicando el ACK 
            self.publishData(topic,payload)                 # EAMA Publica el mensaje de respuesta
            logging.debug('Mensaje enviado')                # Indica que se envio el mensaje
            self.agregarusuario(mensaje[1])                 # Agrega el usuario a la lista
            #Se almacena el usuario recibido en el archivo 
            #logCommand = 'echo "(' + str(msg.topic) + ') -> ' + mensaje[1] + '" >> ' + LOG_FILENAME
            #os.system(logCommand)

    def agregarusuario(self,usuario):           # Funcion para agregar usuarios activos 
        if len(self.users)>0:                   # Si hay usuarios en la lista
            for i in range(len(self.users)):    # Evalua todas las posiciones de la lista
                if self.users[i][0]==usuario:   # Si el usuario existe aumenta su contador
                    self.users[i][1]+=1         # Aumenta el contador de pulsoss
                else:                           # Si el usuario no existe lo agrega a la lista
                    self.users.append([usuario,0])  # Agrega un usuario nuevo
        else:                                   # Si tenemos una lista vacia
            self.users.append([usuario,0])      # Agrega un usuario nuevo
        
                
    def active(self):
        if len(self.users)>0:                   # Si hay usuarios en la lista
            active =[]
            for i in range(len(self.users)):    # Evalua todas las posiciones de la lista
                if self.users[i][1]==0:         # Si no envio alive
                    del self.users[i]           # Elimina el usuario de la lista
            
            for i in range(len(self.users)):    # Evalua todas las posiciones de la lista
                self.users[i][1]=0              # Reinicia el contador de pulsoss                
                active.append(str(self.users[i][0]))    # Si envio pulso lo agrega a la lista
            return active                       # Regresa la lista con usuarios
        else:                                   # Si tenemos una lista vacia
            mensaje = "No hay usuario Activos" 
            return mensaje     

    def on_connect(self,client, userdata, rc):   #Callback que se ejecuta cuando nos conectamos al broker
        logging.info("Conectado al broker")

    def on_publish(self,client, userdata, mid):          # Handler si se publica satisfactoriamente
        publishText = "Publicacion satisfactoria."
        logging.debug(publishText)

    def TCPConfig(self, IP_ADDR, TCP_PORT):         #LFMV configuracion del socket
        TCP_server = socket.socket()
        TCP_server.bind(('',TCP_PORT))              #LFMV Se colocan los parametros del Socket
        TCP_server.listen(10)
        self.socket = socket
        self.TCP_server = TCP_server
        self.IP_ADDR = IP_ADDR
        self.TCP_PORT = TCP_PORT

        logging.debug('OBJETO TCP_SERVIDOR(SOCKET) CREADO')
    def recibir(self):                          #LFMV funcion de recibir
        conn, addr = TCP_server.accept()
        buff = conn.recv(BUFFER_SIZE)
        archivo = open('audio_ser.wav', 'wb')       #LFMV Aca se guarda el archivo entrante
        while buff:
            archivo.write(buff)
            buff = conn.recv(BUFFER_SIZE)           #LFMV Los bloques se van agregando al archivo
        archivo.close()                             #LFMV Se cierra el archivo
        logging.info("Recepcion de archivo finalizada")
    def enviar(self):                               #LFMV funcion para recibir
        conn, addr = TCP_server.accept()    
        with open('audio_ser.wav', 'rb') as f:       #LFMV Se abre el archivo a enviar en BINARIO
            conn.sendfile(f, 0)
            f.close()
        conn.close()
        logging.info("\n\nArchivo enviado a: ", addr)

###########################################################################################################



#print(type(usuarios()))
#print(usuarios())
#tupla=tuple(usuarios())
#print(tupla[0][1])
#print("\n\n")
#print(type(salas()))
#print(salas())
#print(len(salas()[0]))
#sala=usuarios()
#for i in range(len(sala)):
#    for j in range(len(sala[i])):
#        print(sala[i])

#############################################################################################


# logging.warning("Conectando con el broker MQTT...")     # Estableciendo conexion con MQTT
#qos = 2 # QoS de los topics
#for i in range(len(usuarios())):    # Suscripcion a topics
#    topic=str("comandos/10/"+str(usuarios()[i][0]))
#    client.subscribe((topic, qos))
#    logging.info("Suscripcion a: "+topic)

#Iniciamos el thread (implementado en paho-mqtt) para estar atentos a mensajes en los topics subscritos
#client.loop_start() # Crea un loop infinito tipo demonio, permite seguir trabajando
#client.loop_forever()  # Funcion bloqueante, no ejecuta el hilo principal
