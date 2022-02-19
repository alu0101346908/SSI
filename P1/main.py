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


def random_key(message):
    print (pow(2,len(message)))
    result = bin(randrange(pow(2,len(message))))[2:]
    if (len(result) < len(message)):
        while len(result) < len(message):
            result = '0' + result
    return result
message = "Hola Mundo!"
result_transcoding = str_to_ascii_to_bin(message)
result_key = random_key(result_transcoding)
print(result_transcoding)
print("0100100001101111011011000110000100100000010011010111010101101110011001000110111100100001")
print(result_key)