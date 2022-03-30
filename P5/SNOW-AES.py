#Autor: Mario Hernandez Garcia
#Email: alu0101346908@ull.edu.es
#Práctica 5: MULTIPLICACIÓN EN SNOW 3G y AES

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

#Recibe el segundo byte para descomponerlo en nuevos "bytes" que representan la descomposicion de la multiplicacion segun las posiciones de los 1
def separate_polinomy(secondbyte):
  dummy_vector = []
  for i in range(len(secondbyte)):
    dummy_polinomy = ''
    if(secondbyte[i] == '1'):
      for k in range(8):
        if (k == i):
          dummy_polinomy += '1'
        else:
          dummy_polinomy += '0'
      dummy_vector.append(dummy_polinomy)
  return dummy_vector


#Recibe el primer byte y el segundo byte asi como el polinomio ya en bits del algoritmo seleccionado. Separa el segundo byte en nuevos "bytes" que contienen un unico 1 para obtener luego los desplazamientos
#Luego el algoritmo va a ir desplazando el primer byte a la izquierda añadiendo un 0 al final tantas veces como sea la posicion de ese nuevo byte con un uno, en caso de que al realizar el desplazamiento
#Tenemos un 1 en la primera posicion del primer byte tenemos que hacer el xor con los bits del algoritmo seleccionado. Se repite todo esto por tantos nuevos "bytes" y por ultimo se hace la suma de todos esos segmentos
#obteniendo luego el resultado
def multAesSnow(firstbyte, secondbyte, algorimth_polinomy):
  dummy_string = firstbyte
  dummy_result = []
  separated_polinomy_array = separate_polinomy(secondbyte)
  separated_polinomy_array.reverse()
  next_iter = False
  for i in range(len(separated_polinomy_array)):
    dummy_string = firstbyte
    next_iter = False
    print(f'{dummy_string} x {(separated_polinomy_array[i])}')
    print(f'Step 0: {dummy_string}')
    for k in range(((separated_polinomy_array[i])[::-1]).find('1')):
      if(next_iter):
        dummy_string = dummy_string[1:len(dummy_string)] + '0'
        print(f'Step {k+1}: {dummy_string} + {algorimth_polinomy}')
        dummy_string = xor_strings(dummy_string, algorimth_polinomy)
        print(f'= {dummy_string}')
        next_iter = False
      else:
        dummy_string = dummy_string[1:len(dummy_string)] + '0'
        print(f'Step {k+1}: {dummy_string}')
      if(dummy_string[0] == '1'):
        next_iter = True
    dummy_result.append(dummy_string)
    dummy_result.reverse()
  result = dummy_result[0]
  for i in range(1,len(dummy_result)):
    print(f'Suma de la descomposicion {result} + {dummy_result[i]}')
    result = xor_strings(result, dummy_result[i])
  return result;

print("Introduzca el primer byte:")
byte1 = input()
print("Introduzca el segundo byte:")
byte2 = input()
result_byte1 = ""
result_byte2 = ""
for i in range(len(byte1)):
  byte1_string = bin(int(byte1[i],16))[2:]
  while len(byte1_string) < 4 :
    byte1_string = '0' + byte1_string
  result_byte1 += byte1_string
for i in range(len(byte2)):
  byte2_string = bin(int(byte2[i],16))[2:]
  while len(byte2_string) < 4 :
    byte2_string = '0' + byte2_string
  result_byte2 += byte2_string
print("0. AES")
print("1. SNOW3G:")

selection_number = input()
print(f'Primer byte en binario: {result_byte1}')
print(f'Segundo byte en binario: {result_byte2}')
selection = ''
dummy = ''
if(int(selection_number) == 0):
  selection = 'AES'
if(int(selection_number) == 1):
  selection = 'SNOW'
if (selection == 'AES'):
  dummy = multAesSnow(result_byte1, result_byte2, '00011011')
if (selection == 'SNOW'):
  dummy = multAesSnow(result_byte1, result_byte2, '10101001')

print(f'Resultado Mult: {dummy}')
# print(f"Mensaje en binario: \n {str_to_ascii_to_bin(message)} ")
# print(f"Secuencia C/A PRN1 de longitud {str(cypher_length)} : {dummy}")
# encrypted_message_bin = xor_strings(dummy,str_to_ascii_to_bin(message))
# encrypted_message_ascii = bin_to_ascii_to_str(encrypted_message_bin)
# print(f"Mensaje encriptado binario: \n {encrypted_message_bin} ")
# print(f"Mensaje encriptado ascii: \n {encrypted_message_ascii} ")

# dummy = gpsCA(result_vector_1, result_vector_2, polinomy_out_1, polinomy_out_2, polinomy_re_1, polinomy_re_2)

# print(f"Secuencia descifrante C/A PRN1 de longitud {str(cypher_length)} : {dummy}")
# decrypted_message_bin = xor_strings(encrypted_message_bin,dummy)
# decrypted_message_ascii = bin_to_ascii_to_str(decrypted_message_bin)
# print(f"Mensaje desencriptado binario: \n {decrypted_message_bin} ")
# print(f"Mensaje desencriptado ascii: \n {decrypted_message_ascii} ")