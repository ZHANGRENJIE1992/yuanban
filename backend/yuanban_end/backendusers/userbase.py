import hashlib
import base64
from django.utils.encoding import force_bytes
from django.utils.crypto import constant_time_compare
from .common import Common


class BaseUser(Common):
    algorithm = "pbkdf2_sha256"
    iterations = 30000
    digest = hashlib.sha256
    library = None

    def pbkdf2(self, password, salt, iterations, dklen=0, digest=None):
        if hasattr(hashlib, "pbkdf2_hmac"):
            if digest is None:
                digest = self.digest
            if not dklen:
                dklen = None
            password = force_bytes(password)
            salt = force_bytes(salt)
            return hashlib.pbkdf2_hmac(digest().name, password, salt,
                                       iterations, dklen)
        else:
            assert iterations > 0
            if not digest:
                digest = self.digest
            password = force_bytes(password)
            salt = force_bytes(salt)
            hlen = digest().digest_size
            if not dklen:
                dklen = hlen
            if dklen > (2**32 - 1) * hlen:
                raise OverflowError('dklen too big')
            l = -(-dklen // hlen)
            r = dklen - (l - 1) * hlen

            hex_format_string = "%%0%ix" % (hlen * 2)

            inner, outer = digest(), digest()
            if len(password) > inner.block_size:
                password = digest(password).digest()
            password += b'\x00' * (inner.block_size - len(password))
            inner.update(password.translate(hmac.trans_36))
            outer.update(password.translate(hmac.trans_5C))

            def F(i):
                u = salt + struct.pack(b'>I', i)
                result = 0
                for j in range(int(iterations)):
                    dig1, dig2 = inner.copy(), outer.copy()
                    dig1.update(u)
                    dig2.update(dig1.digest())
                    u = dig2.digest()
                    result ^= _bin_to_long(u)
                return _long_to_bin(result, hex_format_string)

            T = [F(x) for x in range(1, l)]
            return b''.join(T) + F(l)[:r]

    def encode(self, password, salt, iterations=None):
        assert password is not None
        assert salt and '$' not in salt
        if not iterations:
            iterations = self.iterations
        hash = self.pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def verify(self, password, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, salt, int(iterations))
        return constant_time_compare(encoded, encoded_2)
