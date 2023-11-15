from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = 'secret data'.encode('UTF-8')

key = 'Password123aaa'
if 10 < len(key) < 33:
    while len(key) < 32:
        key += 'a'
else:
    exit(1)

bkey = key.encode('UTF-8')
print(bkey)
# Encryption
cipher = AES.new(bkey, AES.MODE_EAX)

ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce
print(ciphertext, nonce)

# decryption
cipher = AES.new(bkey, AES.MODE_EAX, nonce)
data = cipher.decrypt_and_verify(ciphertext, tag)
print(nonce, tag)

print(data.decode('UTF-8'))




# original_string = 'secret data'
# target_length = 31

# while len(original_string) < target_length:
#     original_string += original_string

# result_string = original_string[:target_length]
# print(result_string)
