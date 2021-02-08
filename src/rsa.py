from Crypto.Util import number
import secrets


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

        # find public key
        self.pub_key = self.prime1 * self.prime2
        # find num of co-prime numbers
        self.phi = (self.prime1 - 1) * (self.prime2 - 1)
        # private encryption key
        self.enc_key = self.__enc_key_generation()
        # private decryption key
        self.dec_key = self.__dec_key_generation()

    def encrypt(self, message):
        # TODO: Finish @Amir

        # Encode string into an int
        # From https://stackoverflow.com/questions/55407713/how-to-encode-a-text-string-into-a-number-in-python
        message = list(message)
        encrypted_message = []
        for char in message:
            tmp = char.encode('utf-8')
            int_char = int.from_bytes(tmp, 'little')

            encrypted_message.append((int_char**self.enc_key)%self.pub_key)

        return encrypted_message

    def decrypt(self, encrypted_message):
        # TODO: Finish @Amir
        #print(encrypted_message)
        #print(self.dec_key)
        self.dec_key = int(self.dec_key)
        #print(encrypted_message**self.dec_key)
        message = []
        for char in encrypted_message:
            decrypted_int = (char**self.dec_key)%self.pub_key

            decrypted_char = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'little')
            message.append(decrypted_char.decode('utf-8'))
            
        message = "".join(message)
        return message

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


if __name__ == "__main__":
    rsa = RSA()
    print(RSA)
    print('p1', rsa.prime1)
    print('p2', rsa.prime2)
    print('pub1', rsa.pub_key)
    print('phi(N)', rsa.phi)
    print('e', rsa.enc_key)
    print('d', rsa.dec_key)
    print("--------------")
    message = "Hello Planet"
    print("Message: " + message)
    encrypted_message = rsa.encrypt(message)
    print("Encrypted Message: " + str(encrypted_message))
    decrypted_message = rsa.decrypt(encrypted_message)
    print("Decrypted Message: " + decrypted_message)
