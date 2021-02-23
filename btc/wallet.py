import solo
import hashlib
import base58
import sys

# P value for secp256k1
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663

CMD_PUBKEY = 0x63
CMD_RESET = 0x64


class Wallet(object):
    def __init__(self, key):
        assert (len(key) == 96)
        x = int.from_bytes(key[:32], byteorder='big')
        y = int.from_bytes(key[32:64], byteorder='big')

        self.key = Key(x, y, key[64:])


class Key(object):
    def __init__(self, x, y, chain):
        self.x = x
        self.y = y
        self.chain = chain

        # Check that this is a valid key
        assert ((self.x ** 3 + 7 - self.y ** 2) % p == 0)

    def get_compressed(self):
        prefix = b'03'
        if self.y % 2 == 0:
            prefix = b'02'
        return prefix + self.x.to_bytes(length=32, byteorder='big')

    def get_hash(self):
        return hash160(self.get_compressed())

    def get_address(self, prefix: bytes) -> str:
        # Prefix should be a byte sequence
        key_hash = self.get_hash()
        check = checksum(prefix + key_hash)
        unencoded_addr = prefix + key_hash + check
        return base58.b58encode(unencoded_addr).decode("ascii")


def hash160(val):
    s = hashlib.sha256()
    s.update(val)
    r = hashlib.new('ripemd160')
    r.update(s.digest())
    return r.digest()


def checksum(val):
    s = hashlib.sha256()
    s.update(val)
    one = s.digest()
    s = hashlib.sha256()
    s.update(one)

    return s.digest()[:4]


if __name__ == "__main__":
    # Find the Solo key
    client = solo.client.find()

    if len(sys.argv) > 1:
        if sys.argv[1] == "reset":
            print("Resetting device. Press the button to reset")
            client.ctap2.device.call(CMD_RESET)

    wallet = Wallet(client.ctap2.device.call(CMD_PUBKEY))
    address = wallet.key.get_address(b'\x00')
    print(f"Address is {str(address)}")
