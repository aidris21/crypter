from Crypto.Util import number
import secrets


def get_n_bit_random(n=1024):
    return number.getPrime(n)


def is_coprime(a, b):
    return gcd(a, b) == 1


# used to find  encryption key
def gcd(a, b):
    while b != 0:
        a, b = b, a % b

    return a


class RSA:
    phi: int

    def __init__(self, name, age):
        # pick two prime numbers
        self.prime1 = get_n_bit_random()
        self.prime2 = get_n_bit_random()
        # find public key
        self.pub_key = self.prime1 * self.prime2
        # find num of co-prime numbers
        self.phi = (self.prime1 - 1)(self.prime2 - 1)
        # private encryption key
        self.enc_key = 0
        # private decryption key
        self.dec_key = 0

    def key_generation(self):
        # choose e for encryption (1 < e < phi)
        # it must also be a co-prime with pub_key and phi
        e_co_primes = [i for i in range(1, self.phi)
                       if is_coprime(i, self.pub_key)
                       and is_coprime(i, self.phi)]

        idx = secrets.randbelow(len(e_co_primes))
        self.enc_key = e_co_primes[idx]

        # choose d for decryption
        # d*e mod phi = 1
        # TODO: find decryption key
        pass

    def encrypt(self):
        pass

    def decrypt(self):
        pass
