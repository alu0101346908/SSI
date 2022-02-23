from random import randrange

RED = "\033[2;31;40m"
CYAN = "\033[2;36;40m"
GREEN = "\033[2;32;40m"
CLEAR_COLOR = "\033[0;0m"

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

def xor_strings(s,t):
    return "".join(str(int(a,2) ^ int(b,2)) for a,b in zip(s,t))

def bin_to_ascii_to_str(input_string):
    return "".join([chr(int(input_string[i:i+8],2)) for i in range(0,len(input_string),8)])

def random_key(bin_message):
    #print (pow(2,len(message)))
    result = bin(randrange(pow(2,len(bin_message))))[2:]
    if (len(result) < len(bin_message)):
        while len(result) < len(bin_message):
            result = '0' + result
    return result

message = input("¿Que mensaje quieres encriptar?\n")
key = input(f"Introduzca la clave o presione enter para usar una pseudoaleatoria (longitud mensaje {len(message)})\n")
while (not all(char in '01' for char in key)):
    key = input("Error. Clave no binaria. Vuelve a introducirlo\n")

print (CYAN+"\nMensaje: " + CLEAR_COLOR  + message + "\n")
result_transcoding = str_to_ascii_to_bin(message)
print (GREEN + "Mensaje en ASCII a binario: " + CLEAR_COLOR  + result_transcoding + "\n")
if (len(key) == 0):
    key = random_key(result_transcoding)
    print(RED + "Llave generada: " + CLEAR_COLOR  + key + "\n")
else:
    if (len(key) < len(result_transcoding)):
        while len(key) < len(result_transcoding):
            key = '1' + key
    print(RED + "Llave: " + CLEAR_COLOR  + key + "\n")

encripted_message = xor_strings(result_transcoding,key)
print(GREEN + "Mensaje encriptado en binario: " + CLEAR_COLOR  + encripted_message + "\n")

print(CYAN+"Mensaje encriptado en ASCII: " + CLEAR_COLOR  + bin_to_ascii_to_str(encripted_message) + "\n")

message_decoded_bin = xor_strings(encripted_message,key)
print(GREEN + "Mensaje desencriptado en binario: " + CLEAR_COLOR  + message_decoded_bin + "\n")

message_decoded_ascii = bin_to_ascii_to_str(message_decoded_bin)
print(CYAN+"Mensaje desencriptado en ASCII: " + CLEAR_COLOR  + message_decoded_ascii + "\n")

if (message_decoded_bin == result_transcoding and message_decoded_ascii == message):
    print ("\n\033[2;32;40m ¡CORRECTO! " + CLEAR_COLOR )
else:
    print (RED + " ¡INCORRECTO! " + CLEAR_COLOR )