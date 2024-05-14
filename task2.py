import random
import string
import itertools
import time

def generateKey(messageLength, keyLength):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(keyLength))

def extendKeyword(keyword, length):
    extendedKeyword = keyword
    while len(extendedKeyword) < length:
        extendedKeyword += keyword
    return extendedKeyword[:length]

def encrypt(message, keyword):
    encryptedMessage = ""
    keyword = extendKeyword(keyword, len(message))
    for i in range(len(message)):
        char = message[i].lower()
        if char in string.ascii_lowercase:
            shift = ord(keyword[i]) - ord('a')
            encrypted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            encryptedMessage += encrypted_char
        else:
            encryptedMessage += char
    return encryptedMessage

def decrypt(encryptedMessage, keyword):
    decryptedMessage = ""
    keyword = extendKeyword(keyword, len(encryptedMessage))
    for char, key_char in zip(encryptedMessage.lower(), keyword.lower()):
        if char.isalpha():
            shift = ord(key_char) - ord('a')
            decrypted_char = chr(((ord(char) - ord('a') - shift) % 26) + ord('a'))
            decryptedMessage += decrypted_char
        else:
            decryptedMessage += char
    return decryptedMessage

def hack(encryptedMessage):
    decryptedMessages = []
    max_length = 5
    for length in range(2, max_length+1):
        for keyword in itertools.product(string.ascii_lowercase, repeat=length):
            keyword = ''.join(keyword)
            decryptedMessage = decrypt(encryptedMessage, keyword)
            decryptedMessages.append((decryptedMessage, keyword))
    return decryptedMessages

message = "I remember as a child, and as a young budding naturalist, spending all my time observing and testing the world around me moving pieces, altering the flow of things, and documenting ways the world responded to me. Now, as an adult and a professional naturalist, I’ve approached language in the same way, not from an academic point of view but as a curious child still building little mud dams in creeks and chasing after frogs. So this book is an odd thing: it is a naturalist’s walk through the language-making landscape of the English language, and following in the naturalist’s tradition it combines observation, experimentation, speculation, and documentation activities we don’t normally associate with language."


key_length = random.randint(5, 10)
keyword = generateKey(len(message), key_length)

encrypted_message = encrypt(message, keyword)

print("Alice's encrypted message (sent to Bob):")
print(encrypted_message)
print()

print("Bob's decrypted message (Bob's view):")
decrypted_message = decrypt(encrypted_message, keyword)
print(decrypted_message)
print()

start_time = time.time()
decrypted_messages = hack(encrypted_message)
end_time = time.time()

print("Hacking Attempt (Oscar's view):")
for decrypted_message, keyword in decrypted_messages:
    print(f"Keyword: {keyword}, Decrypted Message: {decrypted_message}")

print(f"\nHacking took {end_time - start_time:.2f} seconds.")