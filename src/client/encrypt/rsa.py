from Crypto.Util import number
import secrets
import gmpy2
from gmpy2 import mpz,mpq,mpfr,mpc

# 10-bit number
def get_n_bit_random(n=10):
    return number.getPrime(n)


def is_coprime(a, b):
    return gcd(a, b) == 1


# used to find  encryption key
def gcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a


# used to find the multiplicative inverse of two numbers
# source: https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
def mod_inverse(enc_key, phi):
    candidate = []
    # 10000000 ->number of multiples of enc_key
    num = secrets.randbelow(10000000)
    multiples_of_enc = [enc_key * i for i in range(num)]

    # select every phi_th elem
    for multiple in multiples_of_enc:
        if multiple % phi == 1:
            candidate.append(multiple / enc_key)

    idx = secrets.randbelow(len(candidate))
    return candidate[idx]


class RSA:
    def __init__(self):
        # pick two prime numbers
        self.prime1 = get_n_bit_random()
        self.prime2 = get_n_bit_random()

        # find num of co-prime numbers
        self.phi = (self.prime1 - 1) * (self.prime2 - 1)

        # public key
        self.pub_key = self.prime1 * self.prime2
        self.enc_key = self.__enc_key_generation()
        self.public_key = (self.enc_key, self.pub_key)
        # private decryption key
        self.private_key = self.__dec_key_generation()

    def __enc_key_generation(self):
        # choose e for encryption (1 < e < phi)
        # it must also be a co-prime with pub_key and phi
        e_co_primes = [i for i in range(1, self.phi)
                       if is_coprime(i, self.pub_key)
                       and is_coprime(i, self.phi)]

        idx = secrets.randbelow(len(e_co_primes))
        return e_co_primes[idx]

    def __dec_key_generation(self):
        # choose d for decryption
        # such that d*e mod phi = 1
        return mod_inverse(self.enc_key, self.phi)


def encrypt(message, public_key):
        # TODO: Finish @Amir

        # Encode string into an int
        # From https://stackoverflow.com/questions/55407713/how-to-encode-a-text-string-into-a-number-in-python
        message = list(message)
        encrypted_message = []
        for char in message:
            tmp = char.encode('utf-8')
            int_char = int.from_bytes(tmp, 'little')

            encrypted_char = int((mpz(int_char)**mpz(public_key[0]))%mpz(public_key[1]))
            encrypted_message.append(encrypted_char)

        return str(encrypted_message) # return list of encrypted characters as string

def decrypt(encrypted_message, decryption_key, public_key):
        # TODO: Finish @Amir
        #print(encrypted_message)
        #print(self.dec_key)
        decryption_key = int(decryption_key)
        #print(encrypted_message**self.dec_key)
        message = []
        for char in encrypted_message:
            decrypted_int = (mpz(char)**mpz(decryption_key))%mpz(public_key[1])
            decrypted_int = int(decrypted_int)

            decrypted_char = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'little')
            message.append(decrypted_char.decode('utf-8'))

        message = "".join(message)
        return message


if __name__ == "__main__":
    rsa = RSA()
    print(RSA)
    print('p1', rsa.prime1)
    print('p2', rsa.prime2)
    print('pub1', rsa.pub_key)
    print('phi(N)', rsa.phi)
    print('e', rsa.enc_key)
    print('d', rsa.private_key)
    print("--------------")
    message = input("Please type your message: ")
    print("Message: " + message)
    encrypted_message = encrypt(message, rsa.public_key)
    print("Encrypted Message: " + str(encrypted_message))
    decrypted_message = decrypt(encrypted_message, rsa.private_key, rsa.public_key)
    print("Decrypted Message: " + decrypted_message)
