
str1 = "SOL"
result = ""
for i in range(len(str1)):
    bin_result = bin(ord(str1[i]))[2:]
    if (len(bin_result) == 8):
        result += bin_result
    else:
        while len(bin_result) < 8 :
            bin_result = '0' + bin_result
        result += bin_result
print(result)
print("010100110100111101001100")