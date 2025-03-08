import random
import string
import math
import wordninja
import nltk
from nltk.corpus import words

# nltk wordlist
nltk.download('words')
word_list = set(words.words())
capitalized_words = [word.upper() for word in word_list]

## this wordlist from nltk has many non-words as a part of the list which interferes with accuracy checking
words_to_remove = {"B","C","CA","D","E","EN","EM","ED","F","G","GI","H","J","K","L","M","MU","N","O","OG","OS","P","Q","R","RE","S","T","TD","U","V","W","X","Y","YN","Z"}

# Given string is in all caps so we capitalize the words from the wordlist
capitalized_words = [word for word in capitalized_words if word not in words_to_remove]

quadgram_scores = { }


def load_quadgrams():
    with open("quadgrams.txt") as f:
        ## http://practicalcryptography.com/media/cryptanalysis/files/english_quadgrams.txt.zip
        total = 0
        for line in f:
            quadgram, count = line.split()
            quadgram_scores[quadgram] = int(count)
            total += int(count)
        for quadgram in quadgram_scores:
            quadgram_scores[quadgram] = math.log10(quadgram_scores[quadgram] / total)

# Calculate fitness score based on quadgram frequency
def fitness(text):
    score = 0
    for i in range(len(text) - 3):
        quadgram = text[i:i + 4]
        if quadgram in quadgram_scores:
            score += quadgram_scores[quadgram]
        else:
            score += -10  # Penalize unknown quadgrams
    return score


# Generate a random key
def random_key():
    alphabet = list(string.ascii_uppercase)
    shuffled = alphabet[:]
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))


# Decrypt text using a given key
def decrypt(text, key):
    reverse_key = {v: k for k, v in key.items()}
    return "".join(reverse_key.get(c, c) for c in text)


# Swap two letters in the key to generate a neighbor
def mutate_key(key):
    new_key = key.copy() # Copy of the current key to avoid modifying the original
    a, b = random.sample(string.ascii_uppercase, 2)
    new_key[a], new_key[b] = new_key[b], new_key[a]  # Select two distinct random letters and swap their positions
    return new_key


# Hill climbing algorithm
def hill_climb(ciphertext, iterations=10000):
    best_key = random_key() # Start with random key
    best_decryption = decrypt(ciphertext, best_key) # Attempt decryption with the new key
    best_score = fitness(best_decryption)  # check decryption quality

    # Perform the hill climbing search
    for _ in range(iterations):
        new_key = mutate_key(best_key)  # Generate a neighboring key by swapping two letters
        new_decryption = decrypt(ciphertext, new_key) # Attempt decryption with the new key
        new_score = fitness(new_decryption) # check new decryption quality

        # If the new key produces a better decryption, update the best known key and score
        if new_score > best_score:
            best_key, best_decryption, best_score = new_key, new_decryption, new_score

    # Return the best decryption found and its key
    return best_decryption, best_key


def caesar_cipher_decrypt(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shift_amount = shift % 26
            new_char = chr(((ord(char.lower()) - 97 - shift_amount) % 26) + 97)
            decrypted_text += new_char.upper() if char.isupper() else new_char
        else:
            decrypted_text += char
    return decrypted_text

#Brute force caesar cipher, since there's only 26 possible ciphers, it can be bruteforced instantly
def brute_force_caesar(ciphertext):
    for shift in range(26):
        split_and_check(caesar_cipher_decrypt(ciphertext, shift))

# split_and_check's purpose is to find how many words in the inputted string are real words
# I use the word ninja module to split the string into multiple words, and check the split words against the nltk wordlist
# to get a grasp of its readability
def split_and_check(text, threshold=0.7):
    words = wordninja.split(text)
    valid_words = [word for word in words if word in capitalized_words]


    # Calculate the percentage of valid words
    valid_ratio = len(valid_words) / len(words)

    # Return the phrase if it meets the threshold, else return None
    if valid_ratio >= threshold:
        print(valid_words)
        print(valid_ratio)
        print(" ".join(words))
        print(text)
        return True
    else:
        return None


# Accuracy check for substitution cipher
def split_and_check2(text, threshold=0.9):
    words = wordninja.split(text)
    valid_words = [word for word in words if word in capitalized_words]
    print(valid_words)

    # Calculate the percentage of valid words
    valid_ratio = len(valid_words) / len(words)
    print(valid_ratio)

    if valid_ratio <= threshold:
        print(" ".join(words))
        return True
    else:
        return None

load_quadgrams()
print("Program should be able to solve in under 2 minutes, if wrong result is return please run again")
while True:

    choice = int(input("Decrypt:\n1.FNCNJLQNABJANAJCQNAPXXMJCVJPRLHXDTWXF\n"
                   "2.NUCDMAHJVGJDHHUIEAJFJPNBEAKRJQMHHRJQCHRUFJBIUPHTOEKTHEAKOUPMAXEONUCPJQPMFJMAXDUCPMKJUCBMAXAJFJPLCEHNUCDMADUSJUCHMIEAAJPYCBHREZJSJ\n"
                   "3.HTEBGRMAJHTMBUPPMHTJPTMXMGPUQRJSITEDTIMBHTEBSUBHUOHTJGJUGRJREFEAKUAEHIJPJCATMGGNOUPGPJHHNSCDTUOHTJHESJSMANBURCHEUABIJPJBCKKJBHJXOUPHTEBGPUQRJSQCHSUBHUOHTJBJIJPJRMPKJRNDUADJPAJXIEHTHTJSUFJSJAHUOBSMRRKPJJAGEJDJBUOGMGJPITEDTIMBUXXQJDMCBJUAHTJITURJEHIMBAHHTJBSMRRKPJJAGEJDJBUOGMGJPHTMHIJPJCATMGGN\n"
                   "4.EAHTEBTUCPEXUAUHQJREJFJHTMHMANXMPZAJBBIERRJAXCPJ\n"
                   "5.Quit\n"))
    if choice == 1:
        encrypted_text = "FNCNJLQNABJANAJCQNAPXXMJCVJPRLHXDTWXF"
        print("Decrypting:", encrypted_text)
        brute_force_caesar(encrypted_text)

    if choice == 2:
        ciphertext = "NUCDMAHJVGJDHHUIEAJFJPNBEAKRJQMHHRJQCHRUFJBIUPHTOEKTHEAKOUPMAXEONUCPJQPMFJMAXDUCPMKJUCBMAXAJFJPLCEHNUCDMADUSJUCHMIEAAJPYCBHREZJSJ"
        finished = False

        while not finished:
            plaintext, key = hill_climb(ciphertext)
            if split_and_check2(plaintext):
                print("Decrypted Text:", plaintext, "\n")
            else:
                print("Successful Decrypted Text:", plaintext)
                finished = True

    if choice == 3:
        ciphertext = "HTEBGRMAJHTMBUPPMHTJPTMXMGPUQRJSITEDTIMBHTEBSUBHUOHTJGJUGRJREFEAKUAEHIJPJCATMGGNOUPGPJHHNSCDTUOHTJHESJSMANBURCHEUABIJPJBCKKJBHJXOUPHTEBGPUQRJSQCHSUBHUOHTJBJIJPJRMPKJRNDUADJPAJXIEHTHTJSUFJSJAHUOBSMRRKPJJAGEJDJBUOGMGJPITEDTIMBUXXQJDMCBJUAHTJITURJEHIMBAHHTJBSMRRKPJJAGEJDJBUOGMGJPHTMHIJPJCATMGGN"
        finished = False

        while not finished:
            plaintext, key = hill_climb(ciphertext)
            if split_and_check2(plaintext):
                print("Decrypted Text:", plaintext, "\n")
            else:
                print("Successful Decrypted Text:", plaintext)
                finished = True

    if choice == 4:
        ciphertext = "EAHTEBTUCPEXUAUHQJREJFJHTMHMANXMPZAJBBIERRJAXCPJ"
        finished = False

        while not finished:
            plaintext, key = hill_climb(ciphertext)
            if split_and_check2(plaintext):
                print("Decrypted Text:", plaintext, "\n")
            else:
                print("Successful Decrypted Text:", plaintext)
                finished = True

    if choice == 5:
        break
    else:
        pass