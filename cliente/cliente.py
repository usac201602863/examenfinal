# ssh pr10@167.71.243.238  conectarse al servidor
from BrockerConf import*
#
#
#       CAMBIAR NIVEL DEL LOGGIN A INFO
#
"""
def sendALIVE(recibido=False, retain = False):              # EAMA Funcion para publicar ALIVE
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
            send = False
    sys.exit()  # Matamos el hilo
            
    #sys.exit()    # EAMA Al utilizarlo el main principal sigue en ejecucion
"""
broker=Cliente(False)    # Creamos la instancia brocker del tipo cliente


try:
    broker.Suscribe()
    AliveTh = threading.Thread(name = 'ALIVE',
                        target = broker.sendALIVE,
                        args = (),
                        daemon = False
                        )
    AliveTh.start()
    logging.debug("Iniciando Hilo de Alive")

    #print(usuario().encode("utf-8"))
    #publishData("test","Mensaje Inicial pr80")
    #logging.info("Los datos han sido enviados al broker")            
    #time.sleep(DEFAULT_DELAY)   # Retardo hasta la proxima publicacion de info
    while(State):
        if(AliveTh.is_alive()==False):
            sys.exit()
            State=False

        print("\n\nEnviar texto")
        print("\t 1 - Enviar a usuario")
        print("\t 2 - Enviar a sala")
        print("Enviar mensaje de voz: ") 
        print("\t 3 - Enviar a usuario")
        print("\t 4 - Enviar a sala")
        print("5 - Limpiar pantalla")
        print("6 - Salir")
        opcion=input('Ingrese su opcion: ') # Crear validaciones, si ingresa letra, valor diferente u otras

        if(opcion.isnumeric()):
            opcion=int(opcion)
            if(opcion==1):  # Enviar texto a usuario
                user = str(input('Ingrese usuario: '))          # Realizar excepciones para usuario
                mensaje=str(input('Ingrese mensaje a enviar: '))
                topic='usuarios/'+user
                broker.publishData(topic,mensaje)
                print('\n')
                logging.info("Los datos han sido enviados al usuario") 
            elif(opcion==2):    # Enviar texto a sala
                sala = str(input('Ingrese sala: '))             # Realizar excepciones para sala
                mensaje=str(input('Ingrese mensaje a enviar: '))
                sala=sala.split("s")
                topic='salas/'+sala[0]+'/s'+sala[1]
                broker.publishData(topic,mensaje)
                print('\n')
                logging.info("Los datos han sido enviados a la sala") 
            elif(opcion==3):    # Enviar voz a usuario
                # Selecciona usuario a publicar
                # Ingresa duracion del audio
                # Graba del audio
                # Envia el audio al servidor 

                # Manejo de excepciones +++++++++++++++++++++++++++++++++++++++++++++++
                d = input("Ingrese duracion en segundos: ") # Duracion del mensaje en segundos   
                if(d.isnumeric()):
                    d=int(d)
                    if (d<=30):
                        audio = str(datetime.datetime.now().ctime())    # Nombre de audio con timestamp
                        audio=audio.replace(" ","_")  # Eliminando espacios del nombre
                        grabar(audio,d)
                        reproducir(audio,d)
                    else:
                        logging.error('El mensaje no debe ser mayor a 30 segundos')
                else:
                    logging.error('Debe ingresar un numero.')
            elif(opcion==4):    # Enviar voz a sala
                pass
            elif(opcion==5):    # Salir
                os.system('clear')
            elif(opcion==6):    # Salir
                # Matar todos los hilos
                print('\n')
                logging.warning("Terminando hilos...")
                #if AliveTh.is_alive():
                #    AliveTh.stop()
                State=False
            else:
                print('\n')
                logging.warning('La instruccion ingresada no es valida')
        else:
            print("\n [ERROR]Debe ingresar un numero para seleccionar una opcion.")
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")
    sys.exit()
finally:
    broker.Disconect()


