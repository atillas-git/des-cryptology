import random
import string

def generateKey(language = "english"):
    alphabet = []
    if(language == "english"):
        alphabet = list(string.ascii_lowercase)
        random.shuffle(alphabet)
        return dict(zip(string.ascii_lowercase, alphabet))
    elif language == "turkish":
        alphabet = list("abcçdefgğhıijklmnoöprsştuüvyz")
        random.shuffle(alphabet)
        return dict(zip("abcçdefgğhıijklmnoöprsştuüvyz", alphabet))

def encrypt(message, key):
    encryptedMessage = ""
    for char in message.lower():
        if char in key:
            encryptedMessage += key[char]
        else:
            encryptedMessage += char
    return encryptedMessage

def decrypt(encryptedMessage, key):
    decryptedMessage = ""
    for char in encryptedMessage.lower():
        if char in key.values():
            for k, v in key.items():
                if v == char:
                    decryptedMessage += k
        else:
            decryptedMessage += char
    return decryptedMessage

def hack(encryptedMessage):
    freq = {}
    for char in string.ascii_lowercase:
        freq[char] = encryptedMessage.count(char)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    key = {}
    for i in range(26):
        key[sortedFreq[i][0]] = string.ascii_lowercase[i]
    decrypted_message = decrypt(encryptedMessage, key)
    return decrypted_message

def hackTurkish(encryptedMessage):
    freq = {}
    for char in "abcçdefgğhıijklmnoöprsştuüvyz":
        freq[char] = encryptedMessage.count(char)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    
    key = {}
    for i in range(29):
        key[sortedFreq[i][0]] = "abcçdefgğhıijklmnoöprsştuüvyz"[i]
    
    decryptedMessage = decrypt(encryptedMessage, key)
    return decryptedMessage

def test(language = "english"):
    message  = ""
    if language == "english":
        message = "I remember as a child, and as a young budding naturalist, spending all my time observing and testing the world around me moving pieces, altering the flow of things, and documenting ways the world responded to me. Now, as an adult and a professional naturalist, I’ve approached language in the same way, not from an academic point of view but as a curious child still building little mud dams in creeks and chasing after frogs. So this book is an odd thing: it is a naturalist’s walk through the language-making landscape of the English language, and following in the naturalist’s tradition it combines observation, experimentation, speculation, and documentation activities we don’t normally associate with language. This book is about testing, experimenting, and playing with language. It is a handbook of tools and techniques for taking words apart and putting them back together again in ways that I hope are meaningful and legitimate (or even illegitimate). This book is about peeling back layers in search of the language-making energy of the human spirit. It is about the gaps in meaning that we urgently need to notice and name the places where our dreams and ideals are no longer fulfilled by a society that has become fast-paced and hyper-commercialized. Language is meant to be a playful, ever-shifting creation but we have been taught, and most of us continue to believe, that language must obediently follow precisely prescribed rules that govern clear sentence structures, specific word orders, correct spellings, and proper pronunciations. If you make a mistake or step out of bounds there are countless, self-appointed language experts who will promptly push you back into safe terrain and scold you for your errors. And in case you need reminding, there are hundreds of dictionaries and grammar books to ensure that you remember the “right” way to use English."
    else:
        message = "Çocukluğumda ve yetişmekte olan genç bir doğa bilimci olarak, tüm zamanımı etrafımdaki dünyayı hareket halinde gözlemleyerek ve test ederek geçirdim parçalar, olayların akışını değiştiriyor ve dünyanın yollarını belgeliyor bana cevap verdi. Artık bir yetişkin ve profesyonel bir doğa bilimci olarak, Dile akademik açıdan değil aynı şekilde yaklaştım ama meraklı bir çocuk olarak hala derelerde küçük çamur barajları inşa ediyorum ve kurbağaların peşinde koşuyorum. Yani bu kitap tuhaf bir şey: doğa bilimcinin dil yaratan manzarada yürüyüşü İngilizce dili ve doğa bilimci geleneğini takip ederek gözlem, deney, spekülasyon ve normalde dille ilişkilendirmediğimiz belgeleme faaliyetleri. Bu kitap test etmek, denemek ve oynamakla ilgilidir. dil. Kelime almaya yönelik araç ve tekniklerin yer aldığı bir el kitabıdır. birbirinden ayırıp onları umduğum şekillerde tekrar bir araya getiriyorum anlamlı ve meşru (hatta gayri meşru). Bu kitap hakkında Dilin yapıcı enerjisini bulmak için katmanları soyarak insan ruhu. Bu, acilen gidermemiz gereken anlam boşluklarıyla ilgilidir. hayallerimizin ve ideallerimizin olmadığı yerleri fark edin ve adlandırın artık hızlı tempolu ve aşırı ticarileşmiş bir toplum tarafından yerine getiriliyor. Dilin eğlenceli, sürekli değişen bir yaratım olması gerekiyor ama biz öğretildi ve çoğumuz dilin gerekli olduğuna inanmaya devam ediyoruz. açık bir şekilde yönetilen kesin olarak belirlenmiş kurallara itaatkar bir şekilde uyun cümle yapıları, belirli kelime sıraları, doğru yazımlar ve doğru telaffuzlar. Bir hata yaparsanız veya sınırların dışına çıkarsanız kendi kendini atamış sayısız dil uzmanı var sizi derhal güvenli bölgeye geri iter ve yaptığınız hatalardan dolayı sizi azarlar. hatalar. Ve eğer hatırlatmaya ihtiyaç duyarsanız, yüzlerce var. hatırlamanızı sağlamak için sözlükler ve gramer kitapları İngilizceyi kullanmanın 'doğru' yolu."
        
    key = generateKey(language)
    encryptedMessage = encrypt(message, key)
    print("Alice's encrypted message (sent to Bob):")
    print(encryptedMessage)
    print()

    print("Bobs decrypted message (Bob's view):")
    decryptedMessage = decrypt(encryptedMessage, key)
    print(decryptedMessage)
    print()

    print("Hacking Attempt (Oscar's view):")
    if(language == "english"):
        hackedMessage = hack(encryptedMessage)
        print(hackedMessage)
    elif language == "turkish":
        hackedMessage = hackTurkish(encryptedMessage)
        print(hackedMessage)


print("--------English Version----------")
print()
test(language="english")
print("--------Turkish Version----------")
print()
test(language="turkish")
