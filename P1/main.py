from random import randrange

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

def random_key(message):
    #print (pow(2,len(message)))
    result = bin(randrange(pow(2,len(message))))[2:]
    if (len(result) < len(message)):
        while len(result) < len(message):
            result = '0' + result
    return result

message = "Hola Mundo!"
print ("Mensaje: " + message + "\n")
result_transcoding = str_to_ascii_to_bin(message)
print ("Mensaje en ASCII a binario: " + result_transcoding + "\n")
result_key = random_key(result_transcoding)
print("Llave generada: " + result_key + "\n")
encripted_message = xor_strings(result_transcoding,result_key)
print("Mensaje encriptado en binario: " + encripted_message + "\n")

print("Mensaje encriptado en ASCII: " + bin_to_ascii_to_str(encripted_message) + "\n")

message_decoded_bin = xor_strings(encripted_message,result_key)
print("Mensaje desencriptado en binario: " + message_decoded_bin + "\n")

message_decoded_ascii = bin_to_ascii_to_str(message_decoded_bin)
print("Mensaje desencriptado en ASCII: " + message_decoded_ascii + "\n")

if (message_decoded_bin == result_transcoding and message_decoded_ascii == message):
    print ("\n\033[2;32;40m ¡CORRECTO! \033[0;0m")
else:
    print ("\033[2;31;40m ¡INCORRECTO! \033[0;0m")