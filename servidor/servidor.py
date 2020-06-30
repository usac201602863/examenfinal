from ServerBroker import*
#
#
#       CAMBIAR NIVEL DEL LOGGIN A INFO
#
broker=Servidor()

logCommand = 'touch '+LOG_FILENAME
os.system(logCommand)
try:
    broker.Suscribe()
    print('\n')
    while True:
        logging.info("Los usuarios activos son: ")
        print(str(broker.active()))
        # Verifica si su contador es mayor a cero, de lo contrario lo elimina de la lista
        print('\n')
        time.sleep(6)
        # Reinicia el contador de alives de los cientes

except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")

