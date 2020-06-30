from cryptography.fernet import Fernet              #WAIG Importamos de la libreria cryptography Fernet

class endescrip(object):                            #WAIG Definimos la clase para enciptar y desencriptar
    def __init__(self, llave):                      #WAIG Constructor
        self.llave = llave
    
    def encriptar_mensaje(self, mensaje):           #WAIG Metodo para encriptar el mensaje
        cipher = Fernet(self.llave)                 #WAIG Se convierte cipher en clase Fernet
        encriptar_texto = cipher.encrypt(mensaje)   #WAIG encriptamos el mensaje utilizando la llave
        return encriptar_texto                      

    def desencriptar_mensaje(self, mensaje_encriptado):     #WAIG Metodo para desencriptar el mensaje         
        cipher = Fernet(self.llave)                         #WAIG Se convierte cipher en clase Fernet
        desencriptar_texto = cipher.decrypt(mensaje_encriptado) #WAIG desencriptamos el mensaje utilizando la llave
        return desencriptar_texto

    def encriptar_archivo(self,archivo):            #WAIG Metodo para encriptar el archivo (audio)
        cipher = Fernet(self.llave)                 #WAIG Se convierte cipher en clase Fernet
        
        with open(archivo,'rb') as f:               #WAIG Se abre el archivo y lo definimos con una variable
            archivo_leido = f.read()                #WAIG Leemos el contenido del archivo y lo guardamos en una variable
        archivo_encriptado = cipher.encrypt(archivo_leido)  #WAIG El contenido del archivo lo encriptamos y lo guardamos en otra variable  
        with open(archivo, 'wb') as f:              #WAIG Se abre el archivo y lo definimos con una variable
            f.write(archivo_encriptado)             #WAIG Sobrescribimos los datos del archivo con la encriptacion
    
    def desencriptar_archivo(self, archivo_cifrado):#WAIG Metodo para encriptar el archivo (audio)
        cipher = Fernet(self.llave)                 #WAIG Se convierte cipher en clase Fernet
        
        with open(archivo_cifrado,'rb') as f:       #WAIG Se abre el archivo encriptado y lo definimos con una variable
            archivo_leido = f.read()                #WAIG Leemos el contenido del archivo encriptado y lo guardamos en una variable
        archivo_encriptado = cipher.decrypt(archivo_leido)  #WAIG El contenido del archivo encriptado lo desencriptamos y lo guardamos en otra variable
        with open(archivo_cifrado, 'wb') as f:      #WAIG Se abre el archivo encriptado y lo definimos con una variable
            f.write(archivo_encriptado)             #WAIG Sobrescribimos los datos del archivo encriptado con la desencriptacion     
                                                    #WAIG Asi el archivo vuelve a la normalidad
