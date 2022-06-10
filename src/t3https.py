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
 
#print("p", pint) 
#print("a", aint) 
#print("g", gint) 

A = pow(gInt, aInt, pInt)
#print("A", A)
# transforma A em Hexa
hexA = hex(A)
#print("hexA", hexA)

#######################################

########
# Receber B calcular V = B^a mod p
##
# calcular S = SHA256(V)
##

#####
B = "0x009A77FFA7E6F55530E203DAA030FA1E4F6586B65940794DF32183D89506AE9C0286D42090286D2F549987E33AF7C514AABA7AC5A98D1E65ACAF7AE6896ACA3C7C8A225E8823341B49CCEDBDF2BFE2160AA22CA914B13AF42D8B8FFB6C7C04E37B7EADB01046EFAF5561A84D008C306AA0204BA42EF61A1649EE2395C6B8475BA0"
BInt = int(B, 0)

V = pow(BInt, aInt, pInt)
# transformando o V de int para Hexa
hexV = hex(V).encode('utf-8')
# sha256 do V 
# pegando os primeiros 128 bites em bytes
S = hashlib.sha256(hexV).digest()[:16]
# print(S)

########
# Troca de mensagens
########
# mensagem cifrada
msg = "E48CFC2DA61F029AB6A571EF92255D52E28D51784F890ECF1D13C8B10B3704A267887E4F51CA9B1D918C82B334A82CF49A0A509D89060639EABAF26637A7B8EEC54A96B5F52CC6CCEB4276A550345454CBF9430D00FE3C04009FA023C44A58A40A4DC8B6885F7F0DB3782307907B2AADA9725A11771A967EA5FF6F09EFDCA619"
bytesMsg = bytearray.fromhex(msg)

# AES CBC e padding
# [128 bits com IV][msg] em hexa
# decifrar a msg e enviar ela de volta invertida em hexa

iv = os.urandom(16)
cipher = Cipher(algorithms.AES(S), modes.CBC(iv))
unpadder = padding.PKCS7(block_size=128).unpadder()
decryptor = cipher.decryptor()

dMsg = decryptor.update(bytesMsg) + decryptor.finalize()
udMsg = unpadder.update(dMsg) + unpadder.finalize()
#hexMsg = udMsg.hex()
#print(udMsg.hex())

#print(bytes.fromhex(udMsg.hex()).decode('utf-8'))
#binary_string = codecs.decode(hexMsg, "hex")
#print(str(binary_string, 'utf-8'))


result = udMsg

print(result)








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


