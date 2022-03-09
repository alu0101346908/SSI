#Autor: Mario Hernandez Garcia
#Email: alu0101346908@ull.edu.es
#Práctica 2: Entrega RC4

#Modulo de la libreria random para generar numeros aleatorios
import random 
from random import randrange


#Funcion que recibe la llave solicitada por pantalla con la que se generara el vector K clave, se inicializara ademas el vector S de 0 a 256 con
# que posteriormente se intercambiara los valores con el vector K clave
def initialize(key_vector):
    S = []
    K = []
    for i in range(0,256):
        S.append(i)
        K.append(int(key_vector[i%len(key_vector)]))
    j = 0
    for i in range(256):
            j = (j+S[i]+K[i]) % 256
            if (i > 250 or i < 5):
                print (f"Swap i:{i} y j:{j}")
            S[i] , S[j] = S[j], S[i]
    return S


#Funcion que recibe el vector S inicializado y el mensaje del que se usara su tamaño binario para calcular el numero de bytes cifrantes necesarios
# se procedera al algoritmo de prga guardando en sequence todos los bytes cifrantes que se uniran posteriormente para realizar la operacion xor

def prga(initializedArray, message_bin):
    j = 0
    k = 0
    i = 0
    t = 0
    sequence = []
    for k in range(round(len(message_bin)/8)):
        i = (i + 1) % 256
        j = (j + initializedArray[i]) % 256
        t = (initializedArray[i] + initializedArray[j]) % 256
        #print(initializedArray[j])
        initializedArray[i], initializedArray[j] = initializedArray[j] , initializedArray[i]
        sequence.append(initializedArray[t])
    sequence_result = ''
    k = 0
    for value in sequence:
        bin_result = bin(value)[2:]
        result = ''
        if (len(bin_result) == 8):
            result += bin_result
        else:
            while len(bin_result) < 8 :
                bin_result = '0' + bin_result
            result += bin_result
        sequence_result += result
        k +=1
        print(f'Byte de secuencia cifrante {k} = {result}')
    print("\n")
    return sequence_result

# Funcion que simplemente invoca a la funcion xor_strings, para generalizar
def encrypt(key,message):
    return xor_strings(message,key)




#Costantes de colores para la salida por pantalla
RED = "\033[2;31;40m"
CYAN = "\033[2;36;40m"
GREEN = "\033[2;32;40m"
CLEAR_COLOR = "\033[0;0m"

#Funcion que recibe la string de entrada por consola y la transforma a una string binaria, en caso de que la funcion de 
# conversion no cubra los 8bits que definen un valor en la tabla ascii rellenamos con ceros ya que estos se omiten en la conversion
def str_to_ascii_to_bin(input_string):
    result = ""
    for i in range(len(input_string)):
        bin_result = bin(ord(input_string[i]))[2:]
        if (len(bin_result) == 8):
            result += bin_result
        else:
            while len(bin_result) < 8 :
                bin_result = '0' + bin_result
            result += bin_result
    return result

#Funcion que realiza la operacion xor entre dos strings binarias, para ello se recorre la string binaria valor a valor, 
# se transforma en entero, se realiza la operacion xor y este se vuelve a transformar en string que se añadira a una vacia que retornaremos
def xor_strings(s,t):
    return "".join(str(int(a,2) ^ int(b,2)) for a,b in zip(s,t))

#Funcion que recibe una string binaria y la pasa a ASCII, para ello se recorre la string binaria de 8 en 8 posiciones, 
# se pasa a entero y se utiliza char sobre ese entero para realizar la conversion, esto se añade en cada iteracion a una string nueva
def bin_to_ascii_to_str(input_string):
    return "".join([chr(int(input_string[i:i+8],2)) for i in range(0,len(input_string),8)])

#Funcion generadora de llaves la cual recibe el mensaje en binario para sacar su longitud y asi poder hacer que la clave tenga la misma longitud. 
# La funcion random utiliza la longitud del mensaje como valor tope a generar aleatoriamente. El resultado normalmente tiene menor longitud por lo que lo rellenamos con 0 a la izquierda
#def random_key(bin_message):
    #result = bin(randrange(pow(2,len(bin_message))))[2:]
    #if (len(result) < len(bin_message)):
        #while len(result) < len(bin_message):
            #result = '0' + result
    #return result

message = input("¿Que mensaje quieres encriptar?\n")
key_message = input("Introduzca la clave separandolo por comas (42, 1, 456)\n")
if " " in key_message:
    key_vector = key_message.split(", ")
else:
    key_vector = key_message.split(",")

print(f'Vector de Clave: {key_vector}')
print(GREEN + "Encriptacion" +CLEAR_COLOR+"\n")
encryption = prga(initialize(key_vector),str_to_ascii_to_bin(message))
encrypted_message = encrypt(encryption,str_to_ascii_to_bin(message))
encrypted_message_string = bin_to_ascii_to_str(encrypted_message)
#print (encrypted_message)
#print (encrypted_message_string)
print(GREEN + "Desencriptado" +CLEAR_COLOR+"\n")
encryption2 = prga(initialize(key_vector),encrypted_message)
decrypted_message = encrypt(encryption2,encrypted_message)
decrypted_message_string = bin_to_ascii_to_str(decrypted_message)
#print (decrypted_message)
#print (decrypted_message_string)
# key = input(f"Introduzca la clave o presione enter para usar una pseudoaleatoria (longitud mensaje {len(message)*8})\n")
# while (not all(char in '01' for char in key)):
    # key = input("Error. Clave no binaria. Vuelve a introducirlo\n")

print ("\n"+ CYAN+ "Mensaje: " + CLEAR_COLOR  + message + "\n") 
result_transcoding = str_to_ascii_to_bin(message)
print (GREEN + "Mensaje en ASCII a binario: " + CLEAR_COLOR  + result_transcoding + "\n")
# if (len(key) == 0):
    #key = random_key(result_transcoding)
    #print(RED + "Llave generada: " + CLEAR_COLOR  + key + "\n")
#else:
    #if (len(key) < len(result_transcoding)):
        #while len(key) < len(result_transcoding):
            #key = '1' + key
    #print(RED + "Llave: " + CLEAR_COLOR  + key + "\n")

#encripted_message = xor_strings(result_transcoding,key)
print(CYAN + "Claves cifrantes :"+CLEAR_COLOR + encryption + "\n")

print(GREEN + "Mensaje encriptado en binario: " + CLEAR_COLOR  + encrypted_message + "\n")

print(CYAN+"Mensaje encriptado en ASCII: " + CLEAR_COLOR  + bin_to_ascii_to_str(encrypted_message) + "\n")

print(CYAN + "Claves descifrantes :"+CLEAR_COLOR + encryption2 + "\n")

print(GREEN + "Mensaje desencriptado en binario: " + CLEAR_COLOR  + decrypted_message + "\n")

print(CYAN+"Mensaje desencriptado en ASCII: " + CLEAR_COLOR  + decrypted_message_string + "\n")

if (decrypted_message == result_transcoding and decrypted_message_string == message):
    print ("\n\033[2;32;40m ¡CORRECTO! " + CLEAR_COLOR )
else:
    print (RED + " ¡INCORRECTO! " + CLEAR_COLOR )