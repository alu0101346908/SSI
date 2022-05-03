# #Autor: Mario Hernandez Garcia
# #Email: alu0101346908@ull.edu.es
# #Práctica 9: RSA


import random

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def fastExp(a, b, m):
  x = 1
  y = a % m
  while ((b > 0) and (y > 1)):
    if ((b % 2) == 1):
      x = (x * y) % m
      b = b - 1
    else :
      y = (y * y) % m
      b = b // 2
  return x

def extendedEuclides(a, b, mode):
  if (a > b):
    x0 = a
    x1 = b
    z = 0
    z_1 = 1
    z_2 = 0
    while (x0 % x1 != 0):
      z = ((-(x0 // x1) * z_1) + z_2) % a
      z_2 = z_1
      z_1 = z
      dummy = x1
      x1 = x0 % x1
      x0 = dummy
    if(mode == 1):
      if (x1 == 1):
        return True
      else: return False
    if(mode == 0):
      return z
  else: return -1


def lehmanPeralta(p, t):
  firstPrimes = [2, 3, 5, 7, 11, 13]

  if (p in firstPrimes):
    return True

  for prime in firstPrimes:
    if p % prime == 0:
      return False

  a = []
  for i in range(t):
    a.append(random.randint(2, p-1))

  ai = []
  possiblePrime = False

  for i in range(t):
    ai.append(fastExp(a[i], (p-1) // 2, p))
    if (ai[i] != 1):
      possiblePrime = True
  
  if (not possiblePrime):
    return False
  
  for i in range(t):
    if ((ai[i] != p-1) and (ai[i] != 1)):
      maybePrime = false

  return possiblePrime


def messageToBlock(message, n):
  alphabetLength = len(ALPHABET)
  message = message.replace(' ','')
  j = 0
  while (pow(alphabetLength,j) < n):
    j += 1
  j += -1
  print(f'Como n={n} el texto se divide en bloques de {j} caracteres')
  messageBlock = []
  for i in range((len(message)//j)):
    splits = ''
    for x in range(j):
      splits += message[x+i*j]
    messageBlock.append(splits)
  if((len(message)%j) != 0):
    splits = ''
    for i in range((len(message)%j)):
      splits += 'X'
    messageBlock.append(splits)
  return messageBlockToDecimalBlock(messageBlock,j)


def messageBlockToDecimalBlock(messageBlock, j):
  decimalBlock = []
  for i in range(len(messageBlock)):
    value = 0
    exp = len(messageBlock[i]) - 1
    for j in range(len(messageBlock[i])):
      value += ALPHABET.find(messageBlock[i][j]) * pow(len(ALPHABET), exp)
      exp -= 1
    decimalBlock.append(value)
  return decimalBlock

def cipherDecimalBlock(decimalBlock, e, n):
  encriptedDecimalBlock = []
  for i in range(len(decimalBlock)):
    encriptedDecimalBlock.append(fastExp(decimalBlock[i], e, n))
  return encriptedDecimalBlock


def main():
  prime = False

  while (not prime):
    print('Introduzca el numero primo (p)')
    p = int(input())
    prime = lehmanPeralta(p, 10)
    if (not prime):
      print('Numero p no es un posible primo, vuelve a intentarlo')
  prime = False

  while (not prime):
    print('Introduzca el numero primo (q)')
    q = int(input())
    prime = lehmanPeralta(q, 10)
    if (not prime):
      print('Numero q no es un posible primo, vuelve a intentarlo')

  print('p y q son posibles primos')
  n = p*q
  phiN = (p-1)*(q-1)
  print(f'\nphiN: {phiN}')

  bothPrime = False


  while (not bothPrime):
    print('\nIntroduzca el entero primo (d)')
    d = int(input())
    if (d > phiN):
      bothPrime = extendedEuclides(d, phiN, 1)
    else: 
      bothPrime = extendedEuclides(phiN, d, 1)
    if (not bothPrime):
      print('Numero d no es primo con phi (n), vuelve a intentarlo')

  print('d es primo con phiN')

  print('\nIntroduzca el mensaje')
  message = input()

  if (d > phiN):
    e = extendedEuclides(d, phiN, 0)
  else: 
    e = extendedEuclides(phiN, d, 0)

  print(f'e:= {e}')


  decimalBlock = messageToBlock(message,n)
  print(f'Mensaje a bloque decimal: \n{decimalBlock}')
  encriptedDecimalBlock = cipherDecimalBlock(decimalBlock, e, n)
  print(f'Bloque decimal a encriptado: \n{encriptedDecimalBlock}')
  decriptedDecimalBlock = cipherDecimalBlock(encriptedDecimalBlock, d, n)
  print(f'Bloque encriptado a decimal: \n{decriptedDecimalBlock}')





main()