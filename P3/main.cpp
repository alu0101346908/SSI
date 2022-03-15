#include <stdint.h>
#include <stdio.h>
#include <string>
#include <bits/stdc++.h>
#include <vector>
#include <iomanip>
#include <bitset>


using namespace std;

#define ROUNDS 20

#define ROTL(a,b) (((a) << (b)) | ((a) >> (32 - (b))))

#define QR(a, b, c, d) (  \
  a += b, d ^= a, d = ROTL(d,16), c += d, b ^= c, b = ROTL(b,12), a += b, d ^= a, d = ROTL(d,8), c += d, b ^= c, b = ROTL(b,7))

void printBlock(vector<uint32_t>block){
  int counter2 = 0;
  std::stringstream stream;
  for(int i = 0; i < block.size(); ++i){
    stream << setw(8) << setfill('0') << std::hex << block[i];
    std::string result(stream.str());
    cout << result << " ";
    stream.str("");
    counter2++;
    if (counter2 == 4) {
      cout << endl;
      counter2 = 0;
    }
  }
  cout << endl;
}


vector<uint32_t> chacha_block(vector<uint32_t> input){
  int i = 0;
  vector<uint32_t> x;
  vector<uint32_t> out;
  x.resize(16);
  for (i = 0; i < 16; i++){
    x[i] = input[i];
  }
  for (i = 0; i < ROUNDS; i += 2) {
    QR(x[0], x[4], x[8], x[12]);
    QR(x[1], x[5], x[9], x[13]);
    QR(x[2], x[6], x[10], x[14]);
    QR(x[3], x[7], x[11], x[15]);

    QR(x[0], x[5], x[10], x[15]);
    QR(x[1], x[6], x[11], x[12]);
    QR(x[2], x[7], x[8], x[13]);
    QR(x[3], x[4], x[9], x[14]);
  }
  cout << "Estado final tras las 20 iteraciones=" << endl;
  printBlock(x);
  for (i = 0; i < 16; i++) {
    out.push_back(x[i] + input[i]);
  }
  return out;
}


vector<uint32_t> StringHexToUint(string input){
  input.erase(remove(input.begin(), input.end(), ':'), input.end());
  string dummy = input;
  int i = 0;
  vector<uint32_t> dummy2;
  bool flag = false;
  int counter = 0;
  int counter2 = 0;
  string dummy3 = "";
  string dummy4 = "";
  while (dummy.length() != 0){
    flag = false;
    if (dummy[0] != ' '){
      dummy3 =  dummy3 + dummy[0];
      dummy = dummy.substr(1,dummy.length()-1);
      counter++;
      counter2++;
      if (counter2 == 2){
        dummy4 = dummy3 + dummy4;
        dummy3 = "";
        counter2 = 0;
      }
      if (dummy.length() == 0 || counter == 8){
        flag = true;
      }
    }
    else {
      if (dummy[0] == ' '){
        dummy = dummy.substr(1,dummy.length()-1);
      }
    }
    if (flag){
      dummy2.push_back(stol(dummy4,nullptr,16));
      dummy4 = "";
      counter = 0;
    }

  }
  return dummy2;

}


const char* hex_char_to_bin(char c)
{
    switch(toupper(c))
    {
        case '0': return "0000";
        case '1': return "0001";
        case '2': return "0010";
        case '3': return "0011";
        case '4': return "0100";
        case '5': return "0101";
        case '6': return "0110";
        case '7': return "0111";
        case '8': return "1000";
        case '9': return "1001";
        case 'A': return "1010";
        case 'B': return "1011";
        case 'C': return "1100";
        case 'D': return "1101";
        case 'E': return "1110";
        case 'F': return "1111";
    }
}

std::string hex_str_to_bin_str(const std::string& hex)
{
    // TODO use a loop from <algorithm> or smth
    std::string bin;
    for(unsigned i = 0; i != hex.length(); ++i)
       bin += hex_char_to_bin(hex[i]);
    return bin;
}

vector<uint32_t> initialize(vector<uint32_t>&cons ,vector<uint32_t> &key, uint32_t &counter, vector<uint32_t> &nonce){
  vector<uint32_t> block;
  for(int i = 0; i < cons.size(); ++i){
    block.push_back(cons[i]);
  }
  for(int i = 0; i < key.size(); ++i){
    block.push_back(key[i]);
  }
  block.push_back(counter);
  for(int i = 0; i < nonce.size(); ++i){
    block.push_back(nonce[i]);
  }
  cout << "Estado inicial=" << endl;
  printBlock(block);
  return block;
}

string reverseHex(string input){
  string dummy = "";
  string result = "";
  int counter = 0;
  for (int i = input.length()-1; i >= 0; i--){
    dummy = input[i] + dummy;
    counter++;
    if(counter == 2){
      result = result + dummy;
      counter = 0;
      dummy = "";
    }
  }
  return result;
}

string encrypt(string text, vector<uint32_t> cypher) {
  std::stringstream stream;
  string key = "";
  string encripted = "";
  for (int i = 0; i < text.length(); ++i) {
    stream << setw(8) << setfill('0') << std::hex << cypher[i];
    std::string result(stream.str());
    key += result;
    stream.str("");
  }
  string byte = "";
  for (int i = 0; i < text.length(); ++i) {
    encripted += int(text[i])^stoi(key.substr(i*2,2),nullptr,16);

  }
  return encripted;
}

int main (void) {
  
  string input = "00:01:02:03: 04:05:06:07: 08:09:0a:0b: 0c:0d:0e:0f: 10:11:12:13: 14:15:16:17: 18:19:1a:1b: 1c:1d:1e:1f";

  vector<uint32_t> cons = {uint32_t(stol("61707865",nullptr,16)),uint32_t(stol("3320646e",nullptr,16)),uint32_t(stol("79622d32",nullptr,16)),uint32_t(stol("6b206574",nullptr,16))};
  vector<uint32_t> input_ =  StringHexToUint(input);
  uint32_t counter = stol(reverseHex("01000000"),nullptr,16);
  //vector<uint32_t> nonce = {uint32_t(rand() % 4294967296), uint32_t(rand() % 4294967296), uint32_t(rand() % 4294967296)};
  vector<uint32_t> nonce = {uint32_t(stol(reverseHex("00000009"),nullptr,16)), uint32_t(stol(reverseHex("0000004a"),nullptr,16)), uint32_t(stol(reverseHex("00000000"),nullptr,16))};
  vector<uint32_t> block = initialize(cons,input_,counter,nonce);
  vector<uint32_t> out;
  out = chacha_block(block);
  cout << "Estado de salida del generador=" << endl;
  printBlock(out);
  string message = "Hola";
  string encriptado = encrypt(message, block);
  cout << "Mensaje a encriptar: " << message << endl;
  cout << "Mensaje encriptado: " << encriptado << endl;
  cout << "Mensaje desencriptado: " << encrypt(encriptado, block) << endl;
}






