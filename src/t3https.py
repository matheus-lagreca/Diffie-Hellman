###########
## HTTPS ##
###########
#hashlib para fazer o sha256
import os
import hashlib
import codecs
# AES 
# Kops me passou essa biblioteca
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# https://cryptography.io/en/latest/hazmat/primitives/padding/
from cryptography.hazmat.primitives import padding


### old dependencies
# pip install pycrypto pycryptodome
# from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad, unpad
# from Crypto.Random import get_random_bytes
# from base64 import b64decode, b64encode
# import json



p = "0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"
g = "0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5"

# gerar um 'a' menor do que p
a = "0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4340"
# mudei o final de 71 pra 40
# calcular 'A'
# g^a mod p
pInt = int(p, 0) 
aInt = int(a, 0)
gInt = int(g, 0)
 
A = pow(gInt, aInt, pInt)
#print("A", A)
# transforma A em Hexa
hexA = hex(A)
print("hexA", hexA)
#######################################

#######
# Receber B calcular V = B^a mod p
#
# calcular S = SHA256(V)
#

# TESTE local
# fake B

# b = "0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4320"
# B = pow(gInt, int(b,0), pInt)
# V = pow(B, aInt, pInt)
# hash = hashlib.sha256()
# hash.update(V.to_bytes(129, "big"))
# #hash.update(hex(V).encode('utf-8'))
# S = hash.digest()[:16].hex()
# S = S.encode()
# print("S", S)
# #
# key = S
# iv = os.urandom(16)
# cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
# encryptor = cipher.encryptor()
# padder = padding.PKCS7(block_size=128).padder()
# padded_data = padder.update(b"11111111111111112222222222")
# padded_data += padder.finalize()
# print("pd", padded_data)
# ct = encryptor.update(padded_data) + encryptor.finalize()
# print("iv", iv)
# print("ct", ct)

# unpadder = padding.PKCS7(block_size=128).unpadder()
# decryptor = cipher.decryptor()
# xxx = decryptor.update(ct) + decryptor.finalize()
# xxx = unpadder.update(xxx) + unpadder.finalize()
# print(xxx)

# #######################
# Avelino B
#B = "0x009A77FFA7E6F55530E203DAA030FA1E4F6586B65940794DF32183D89506AE9C0286D42090286D2F549987E33AF7C514AABA7AC5A98D1E65ACAF7AE6896ACA3C7C8A225E8823341B49CCEDBDF2BFE2160AA22CA914B13AF42D8B8FFB6C7C04E37B7EADB01046EFAF5561A84D008C306AA0204BA42EF61A1649EE2395C6B8475BA0"
# Kops B
B = "0x852637cd1afbda02989c9b0958ba1476cd44caa31b12d3fff5bec29b560c85185ffd8ed33408465fe853af68810861f8ae6cb74720d3f75dc3a2a9a5857941a52dd7f7b07732802c5e8eaf017e25db626ae27271cbb6ce79dd0e4c73d2a922a23d786a2fc9b10c432c97c88ee5e685cd69e11b95fd3b48bbbe3318fef0dee393"
BInt = int(B, 0)
V = pow(BInt, aInt, pInt)
hash = hashlib.sha256()
hash.update(V.to_bytes(129, "big"))
S = hash.digest()[:16].hex()
#S = S.encode()
S = bytes.fromhex(S)
print("128 bits de S", S)
# ########
# # Troca de mensagens
# # mensagem cifrada
# Avelino Msg
#msg = "E48CFC2DA61F029AB6A571EF92255D52E28D51784F890ECF1D13C8B10B3704A267887E4F51CA9B1D918C82B334A82CF49A0A509D89060639EABAF26637A7B8EEC54A96B5F52CC6CCEB4276A550345454CBF9430D00FE3C04009FA023C44A58A40A4DC8B6885F7F0DB3782307907B2AADA9725A11771A967EA5FF6F09EFDCA619"
# Kops msg
msg = "8c3acf5f0edbb7c9396aa9f4fc6e2f6c6e6ea35c67db5e12cc6d23dafb8bc5d2c436eae17853563eb2558b7f329b52cd"
bytesMsg = bytes.fromhex(msg)
# # AES CBC e padding
# # [128 bits com IV][msg] em hexa
# # decifrar a msg e enviar ela de volta invertida em hexa
# # https://stackoverflow.com/questions/57544299/valueerror-invalid-padding-bytes-when-decrypting-with-aes256
ivEnc = os.urandom(16)
ivDec, bytesMsg = bytesMsg[:16], bytesMsg[16:]
# # Setup
cipher = Cipher(algorithms.AES(S), modes.CBC(ivDec))
decryptor = cipher.decryptor()
# # unpadder
unpadder = padding.PKCS7(block_size=128).unpadder()
# unpadder = padding.ANSIX923(block_size=128).unpadder()
pMsg = decryptor.update(bytesMsg) + decryptor.finalize()
print("pMsg", pMsg)
pMsg = unpadder.update(pMsg) + unpadder.finalize()
print("unpaded", pMsg)
result = pMsg.hex()
print(result)

# gera
myMsg = "Schell & Gugu eram namoradinhos no Educa-Mais"
myMsg = myMsg.encode('utf-8')
print(myMsg)
encryptor = cipher.encryptor()
padder = padding.PKCS7(block_size=128).padder()
padded_data = padder.update(myMsg)
print("update", padded_data)
padded_data += padder.finalize()
print("finalize ", padded_data)
ct = encryptor.update(padded_data) + encryptor.finalize()
print("iv", ivEnc)
print("ct", ct)

result = ivEnc+ct
print("result", result)
print("hex result", result.hex())


print("decode------------------------")

c2 = Cipher(algorithms.AES(S), modes.CBC(ivEnc))
dcry = c2.decryptor()
unpd = padding.PKCS7(block_size=128).unpadder()
testMsg = dcry.update(result + dcry.finalize()
print(testMsg)
testMsg = unpd.update(testMsg) + unpd.finalize()
print(testMsg)



#binary_string = codecs.decode(pMsg, "hex")
#print(str(binary_string, 'utf-8'))
# ########################







## decryption
#iv = b64decode('iv')
#ct = b64decode(msg)
#cipher = AES.new(S, AES.MODE_CBC, iv)
#pt = unpad(cipher.decrypt(ct), AES.block_size)
#print("msg: ", pt)

#####################################
##### teste
##### troquei de chave com o kops

# BTest = "0x938d9ec609cbda896542654e2fec603c276934bc1aae9c4bfb72e2df80b00fe19835e6714b682d0825ed23fd0f3a041afa02f78c8bfb057f2e76857df47d9f62ea01574191b7b742876070f598551cdb41ef0800239d6b3270882f7deee59be8f8e3226cd0bfeb510c2afe24671a24d3771dc1259e2c1478cc841c2e14f525ea"
# BTestInt = int(BTest, 0)
#####
##### teste envia e recebe
# recebe = pow(BTestInt, aInt, pInt)
#print("envia", envia)
#print("recebe", recebe)

# VTestHex=hex(recebe).encode('utf-8')
# sTest = hashlib.sha256(VTestHex).digest()[:16].hex()

#hexSText = sTest.hex()
# print(sTest)


