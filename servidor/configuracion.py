import binascii
QoS = 0		                    # EAMA Calidad de envio del mensaje
qos = 2                         # EAMA Calidad de suscripcion a topic  
State = True                    # EAMA Control de main principal
Grupo= 10                       # EAMA Numero de grupo
LOG_FILENAME = 'activos'        # EAMA Archivo con usuarios activos

FRR = binascii.unhexlify("02")	    # EAMA Constante para transferencia de archivos servidor a cliente
FTR = binascii.unhexlify("03")	    # EAMA Constante para transferencia de archivos cliente a servidor
ALIVE = binascii.unhexlify("04")	# EAMA Constante para indicar que esta activo
ACK = binascii.unhexlify("05")	    # EAMA Constante para indicar que esta activo
OK = binascii.unhexlify("06")	    # EAMA Constante para indicar que esta activo
NO = binascii.unhexlify("07")	    # EAMA Constante para indicar que esta activo

ALIVE_PERIOD = 2            # EAMA El alive se envia cada 2 segundos

SALAS = 'salas'             # EAMA Archivo que contiene las salas validas
USUARIOS = 'usuarios'       # EAMA Archivo que contiene los usuarios validos
