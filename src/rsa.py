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

    def encrypt(self):
        # TODO: Finish @Amir
        pass

    def decrypt(self):
        # TODO: Finish @Amir
        pass

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
