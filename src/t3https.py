###########
## HTTPS ##
###########

# Nomes: Matheus Lagreca da Silva, João Pedro Laureano
# Engenharia de Software - Segurança de Sistemas
# Trabalho 3 - Simular parte do HTTPS

#hashlib para fazer o sha256
import os
import hashlib
# AES 
# https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# https://cryptography.io/en/latest/hazmat/primitives/padding/
from cryptography.hazmat.primitives import padding

# Variaveis
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
# transforma A em Hexa
hexA = hex(A)
print("a em Hexadecimal: ", a, "\n")
print("A em Hexadecimal: ", hexA, "\n")
#######################################

#######
# Receber B 
# calcular V = B^a mod p
#
# calcular S = SHA256(V)
# #######################
# Avelino B
B = "0x009A77FFA7E6F55530E203DAA030FA1E4F6586B65940794DF32183D89506AE9C0286D42090286D2F549987E33AF7C514AABA7AC5A98D1E65ACAF7AE6896ACA3C7C8A225E8823341B49CCEDBDF2BFE2160AA22CA914B13AF42D8B8FFB6C7C04E37B7EADB01046EFAF5561A84D008C306AA0204BA42EF61A1649EE2395C6B8475BA0"
BInt = int(B, 0)

print("B em Hexadecimal: ", B, "\n")

# Calcular V
V = pow(BInt, aInt, pInt)
hash = hashlib.sha256()
hash.update(V.to_bytes(128, "big"))

# Calcular S
S = hash.digest()[:16].hex()
S = bytes.fromhex(S)
print("128 bits de S: ", S, "\n")
# ########

# # Troca de mensagens
# # mensagem cifrada
# Avelino Msg
msg = "E48CFC2DA61F029AB6A571EF92255D52E28D51784F890ECF1D13C8B10B3704A267887E4F51CA9B1D918C82B334A82CF49A0A509D89060639EABAF26637A7B8EEC54A96B5F52CC6CCEB4276A550345454CBF9430D00FE3C04009FA023C44A58A40A4DC8B6885F7F0DB3782307907B2AADA9725A11771A967EA5FF6F09EFDCA619"
bytesMsg = bytes.fromhex(msg)

# # AES CBC e padding
# # [128 bits com IV][msg] em hexa
# # decifrar a msg e enviar ela de volta invertida em hexa
# # https://stackoverflow.com/questions/57544299/valueerror-invalid-padding-bytes-when-decrypting-with-aes256
# Usamos este post do stackoverflow para resolver um erro de padding
ivDec, bytesMsg = bytesMsg[:16], bytesMsg[16:]
cipher = Cipher(algorithms.AES(S), modes.CBC(ivDec))
decryptor = cipher.decryptor()

# # unpadder
unpadder = padding.PKCS7(block_size=128).unpadder()
# outro unppader que testamos
# unpadder = padding.ANSIX923(block_size=128).unpadder()
pMsg = decryptor.update(bytesMsg) + decryptor.finalize()
pMsg = unpadder.update(pMsg) + unpadder.finalize()
print("Mensagem em texto claro: ", pMsg.decode(), "\n")

print("--------------------------------------------- Invert Msg-------------------------------------------------------\n")

invertedMsg = pMsg.decode()[::-1]
print("Mensagem Invertida: ", invertedMsg, "\n")

# gera
print("---------------------------------------------- Encode ------------------------------------------------------\n")
ivEnc = os.urandom(16)
myMsg = invertedMsg
myMsg = myMsg.encode('utf-8')
# Cipher novo para criptografar
cEnc = Cipher(algorithms.AES(S), modes.CBC(ivEnc))
encry = cEnc.encryptor()
# Adicionando padding
padder = padding.PKCS7(block_size=128).padder()
padded_data = padder.update(myMsg)
padded_data += padder.finalize()
ct = encry.update(padded_data) + encry.finalize()

# printando mensagem invertida com IV
msgInvertCryp =ivEnc+ct
print("hex result: ", msgInvertCryp.hex(), "\n") 

print("-------------------------------------------- Decode ---------------------------------------------------------")
# Ultima mensagem recebida
finalMsg = "62019C19EE03973A5427766CA0392A62307100CB8D2947B4144FBBCBC9E9A128AE007F396BC1C651E5FA1865B29DCBF1235B9F9B6C102D423150FF30C3D91455C3E36BEBDB3FF842D499714F3E317D78B650CA41FF7DFEA0F05A6B843AB660980CA0282BA716434EE6D9D820486E9521894C0F5345CC237DBC498F0810D8F25E5116A02CAFDC79AC6671D5488EFB473CBD9F4B071488CF51D215456FCAE0DA6DF4104744A1E5E7D150C57DB8BBBDA91DBCE992AEFE69E3F37EEFEEA7C3440864"
bytesR = bytes.fromhex(finalMsg)
# separando IV da mensagem
ivDec2, bytesR = bytesR[:16], bytesR[16:]
# novo cipher
c2 = Cipher(algorithms.AES(S), modes.CBC(ivDec2))
dcry = c2.decryptor()
# tirando o padding
unpd = padding.PKCS7(block_size=128).unpadder()
testMsg = dcry.update(bytesR) + dcry.finalize()
testMsg = unpd.update(testMsg) + unpd.finalize()
print("Final Msg: ", testMsg.decode(), "\n")

