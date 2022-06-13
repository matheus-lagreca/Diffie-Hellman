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
print("bytesMsg", bytesMsg)
# # AES CBC e padding
# # [128 bits com IV][msg] em hexa
# # decifrar a msg e enviar ela de volta invertida em hexa
# # https://stackoverflow.com/questions/57544299/valueerror-invalid-padding-bytes-when-decrypting-with-aes256
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
print("---------------------------------------------- Encode ------------------------------------------------------")
ivEnc = os.urandom(16)
myMsg = "Schell & Gugu eram namoradinhos no Educa-Mais"
myMsg = myMsg.encode('utf-8')
print("MSG", myMsg)
encryptor = cipher.encryptor()
padder = padding.PKCS7(block_size=128).padder()
padded_data = padder.update(myMsg)
padded_data += padder.finalize()
print("finalize ", padded_data)
ct = encryptor.update(padded_data) + encryptor.finalize()
print("iv", ivEnc)
print("ct", ct)

print("--------------------------------------------- results -------------------------------------------------------")
result =ivEnc+ct
print("ivEnc", ivEnc.hex())
print("ct", ct.hex())
print("result", result)

bytesR = bytes.fromhex(result.hex())
print("hex result", bytesR) 


print("-------------------------------------------- decode ---------------------------------------------------------")
ivDec2, bytesR = bytesR[:16], bytesR[16:] 
print("ivDec2", ivDec2)
print("bytesMsg2", bytesR)
c2 = Cipher(algorithms.AES(S), modes.CBC(ivDec2))
dcry = c2.decryptor()
unpd = padding.PKCS7(block_size=128).unpadder()
testMsg = dcry.update(bytesR) + dcry.finalize()
print("tMsg", testMsg)
testMsg = unpd.update(testMsg) + unpd.finalize()
print("msg", testMsg)



#binary_string = codecs.decode(pMsg, "hex")
#print(str(binary_string, 'utf-8'))
# ########################





