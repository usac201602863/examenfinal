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
        time.sleep(6)


except KeyboardInterrupt:
    logging.warning("Desconectando del broker...")

finally:
    client.loop_stop() #Se mata el hilo que verifica los topics en el fondo
    client.disconnect() #Se desconecta del broker
    logging.info("Desconectado del broker. Saliendo...")

