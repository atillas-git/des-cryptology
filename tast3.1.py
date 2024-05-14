import binascii
import itertools
from des import Des,CBC_VALUE,PAD_PKCS5_VALUE

def crypt(data, secret):
    cipher = Des(secret, CBC_VALUE, secret, pad=None, padmode=PAD_PKCS5_VALUE)
    data_bytes = data.encode('utf-8')
    encoded_data = cipher.encrypt(data_bytes)
    return binascii.hexlify(encoded_data).decode('utf-8')
 
def decrypt(encodedData, secret):
    cipher = Des(secret, CBC_VALUE, secret, pad=None, padmode=PAD_PKCS5_VALUE)
    encodedDataBytes = binascii.unhexlify(encodedData)
    decoded = cipher.decrypt(encodedDataBytes)
    return decoded.decode('utf-8').rstrip()
 
def hack(encodedData):
    p_keys = [''.join(secret) for secret in itertools.product('01', repeat=64)] 
    for secret in p_keys:
        secretBytes = binascii.unhexlify(hex(int(secret, 2))[2:].zfill(16))  
        try:
            decryptedData = decrypt(encodedData, secretBytes)
            if all(char < 128 for char in decryptedData.encode('utf-8')):
                return decryptedData, secretBytes
        except Exception as e:
            pass

message = "I remember as a child, and as a young budding naturalist, spending all my time observing and testing the world around me moving pieces, altering the flow of things, and documenting ways the world responded to me. Now, as an adult and a professional naturalist, I’ve approached language in the same way, not from an academic point of view but as a curious child still building little mud dams in creeks and chasing after frogs. So this book is an odd thing: it is a naturalist’s walk through the language-making landscape of the English language, and following in the naturalist’s tradition it combines observation, experimentation, speculation, and documentation activities we don’t normally associate with language."

key = b'abcdefgh'
aliceMsg = crypt(message, key)

print("Alice's encyrpted message:")
print(aliceMsg)
print()
print("----------------------------------------------")

print("Bob's decyrpted message:")
bobsMsg = decrypt(aliceMsg, key)
print(bobsMsg)
print()
print("----------------------------------------------")

print("Oscars Hacking Attempt:")
hackedMessage, hackedKey = hack(aliceMsg)
print("Decrypted Message:", hackedMessage)
print("Decryption Key:", binascii.hexlify(hackedKey).decode('utf-8'))