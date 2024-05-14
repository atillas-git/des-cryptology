from PIL import Image
import io
from des import Des,CBC_VALUE,PAD_PKCS5_VALUE

def encrypt(data, secretKey):
    s = Des(secretKey, CBC_VALUE, secretKey, pad=None, padmode=PAD_PKCS5_VALUE)
    encrypted = s.encrypt(data)
    return encrypted
 
def decrypt(data, secretKey):
    s = Des(secretKey, CBC_VALUE, secretKey, pad=None, padmode=PAD_PKCS5_VALUE)
    decrypted = s.decrypt(data)
    return decrypted
 
def hack(encryptedData):
    for i in range(256):
        key = bytes([i]) * 8 
        decryptedData = decrypt(encryptedData, key)
        if decryptedData.startswith(b'BM'):
            return decryptedData, key  
 
path = "sample-image.bmp"
image = Image.open(path)
 
image.show()
 
with io.BytesIO() as buffer:
    image.save(buffer, format="BMP")
    imageBytes = buffer.getvalue()
 
secretKey = "abcdefgh"

encryptedBytes = encrypt(imageBytes, secretKey)
 
encryptedImagePath = "encrypted-image.bmp"
 
with open(encryptedImagePath, "wb") as encryptedFile:
    encryptedFile.write(encryptedBytes)
 
decryptedImageBytes = decrypt(encryptedBytes, secretKey)
 
decryptedImg = Image.open(io.BytesIO(decryptedImageBytes))
 
decryptedImg.show()

hackedImgBytes, key = hack(encryptedBytes)
if hackedImgBytes is not None:
    with io.BytesIO(hackedImgBytes) as buffer:
        decryptedImg = Image.open(buffer)
    decryptedImg.show()
    print("Key:", key.decode())
else:
    print("Hack unsuccessful.")