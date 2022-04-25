# #Autor: Mario Hernandez Garcia
# #Email: alu0101346908@ull.edu.es
# #Práctica 8: gamalDH

def extendedEuclides(a, b):
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
    return z
  else: return -1


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

print('Introduzca el numero primo (py)')
py = int(input())
print('Introduzca el numero entero (a)')
a = int(input())
print('Introduzca el secreto (xA)')
xA = int(input())
print('Introduzca el secreto (xB)')
xB = int(input())
print('Introduzca el mensaje (m)')
message = int(input())

yA = fastExp(a, xA, py)
print(f'yA = {yA}')

yB = fastExp(a, xB, py)
print(f'yB = {yB}')

kA = fastExp(yB, xA, py)

kB = fastExp(yA, xB, py)

if (kA == kB):
  k = kA
else:
  k = -1

print(f'k = {k}')

encripted_message = (kB * message) % py
print(f'c = {encripted_message}')

invertedK = extendedEuclides(py, k)
print(f'k^-1 = {invertedK}')

decrypted_message = (encripted_message * invertedK) % py;
print(f'm = {decrypted_message}')
