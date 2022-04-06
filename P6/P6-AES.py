# #Autor: Mario Hernandez Garcia
# #Email: alu0101346908@ull.edu.es
# #Práctica 6: AES


nb = 4  #columnas del estado
nr = 10  # numero de rondas del algoritmo
nk = 4  # longitud de la llave (32 bits)

sbox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

rcon = [[0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
]


def encrypt(input_bytes, key):
    input_symbols = []
    for i in range(0,len(input_bytes),2):
      dummy = input_bytes[i]+input_bytes[i+1]
      input_symbols.append(int(dummy,16))

    state = [[] for j in range(4)]
    for r in range(4):
        for c in range(nb):
            state[r].append(input_symbols[r + 4 * c])

    key_schedule = key_expansion(key)

    state = add_round_key(state, key_schedule,0)
    for rnd in range(1, nr):
        dummy = ''
        dummy2 = ''
        for i in range(0,16):
          dummy += f'{key_schedule[rnd-1][i]:#0{4}x}'[2::]
          dummy2 += f'{state[i%4][int(i/4)]:#0{4}x}'[2::]
        print (f'R'+str(rnd)+' (Subclave = ' + dummy + ') = ' +dummy2)
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key_schedule, rnd)

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, rnd + 1)
    dummy = ''
    dummy2 = ''
    for i in range(0,16):
      dummy += f'{key_schedule[len(key_schedule)-1][i]:#0{4}x}'[2::]
      dummy2 += f'{state[i%4][int(i/4)]:#0{4}x}'[2::]
    print (f'R'+str(10)+' (Subclave = ' + dummy + ') = ' +dummy2)
    return dummy2


def sub_bytes(state):

    box = sbox
    for i in range(len(state)):
        for j in range(len(state[i])):
            row = state[i][j] // 0x10
            col = state[i][j] % 0x10
            box_elem = box[16 * row + col]
            state[i][j] = box_elem

    return state


def shift_rows(state):

    count = 1

    for i in range(1, nb):
      state[i] = left_shift(state[i], count)
      count += 1
    return state


def mix_columns(state):

    for i in range(nb):

      s0 = mul_by_02(state[0][i]) ^ mul_by_03(state[1][i]) ^ state[2][i] ^ state[3][i]
      s1 = state[0][i] ^ mul_by_02(state[1][i]) ^ mul_by_03(state[2][i]) ^ state[3][i]
      s2 = state[0][i] ^ state[1][i] ^ mul_by_02(state[2][i]) ^ mul_by_03(state[3][i])
      s3 = mul_by_03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ mul_by_02(state[3][i])
      state[0][i] = s0
      state[1][i] = s1
      state[2][i] = s2
      state[3][i] = s3

    return state


def key_expansion(key):
    key_symbols = []
    for i in range(0,len(key),2):
      dummy = key[i]+key[i+1]
      key_symbols.append(int(dummy,16))

    if len(key_symbols) < 4 * nk:
        for i in range(4 * nk - len(key_symbols)):
            key_symbols.append(0x01)

    key_schedule = [[] for i in range(4)]
    for r in range(4):
        for c in range(nk):
            key_schedule[r].append(key_symbols[r + 4 * c])

    for col in range(nk, nb * (nr + 1)):  # col - column number
        if col % nk == 0:
            # Se cogen el 2, 3 y 4 valor de la ultima columna
            tmp = [key_schedule[row][col - 1] for row in range(1, 4)]
            #rotword de la primera que no se cogio
            tmp.append(key_schedule[0][col - 1])

            for j in range(len(tmp)):
                sbox_row = tmp[j] // 0x10
                sbox_col = tmp[j] % 0x10
                sbox_elem = sbox[16 * sbox_row + sbox_col]
                tmp[j] = sbox_elem

            # and finally make XOR of 3 columns
            for row in range(4):
                w = (key_schedule[row][col - 4]) ^ (tmp[row]) ^ (rcon[row][int(col / nk - 1)])
                key_schedule[row].append(w)

        else:
            # habiendo completado el primer bloque, se hacen xor simples para sacar las nuevas columnas y inicializar el segundo bloque
            for row in range(4):
                s = key_schedule[row][col - 4] ^ key_schedule[row][col - 1]
                key_schedule[row].append(s)

    dummy = [[] for i in range(11)]
    for r in range(11):
      for k in range(4):
        for c in range(4):
          dummy[r].append(key_schedule[c][k+(r*4)])
    return dummy


def add_round_key(state, key_schedule, round):
    key = key_schedule[round]
    for col in range(nk):
        s0 = state[0][col] ^ key[0+((col*4))]
        s1 = state[1][col] ^ key[1+((col*4))]
        s2 = state[2][col] ^ key[2+((col*4))]
        s3 = state[3][col] ^ key[3+((col*4))]

        state[0][col] = s0
        state[1][col] = s1
        state[2][col] = s2
        state[3][col] = s3

    return state



def left_shift(array, count):
    res = array
    for i in range(count):
        temp = res[1:]
        temp.append(res[0])
        res = temp

    return res


def mul_by_02(num):

    if num < 0x80:
        res = (num << 1)
    else:
        res = (num << 1) ^ 0x1b

    return res % 0x100


def mul_by_03(num):
    return (mul_by_02(num) ^ num)


print('Introduzca la clave (128bits en hex)')
key = input()
print('Introduzca el mensaje (128bits en hex)')
message = input()
print('\n')
print (f'\nBloque de Texto Cifrado: '+ encrypt(message,key))