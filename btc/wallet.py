import solo

# P value for secp256k1
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663

CMD_PUBKEY = 0x63
CMD_RESET = 0x64


class Wallet(object):
    def __init__(self, key):
        assert (len(key) == 96)
        self.x = int.from_bytes(key[:32], byteorder='big')
        self.y = int.from_bytes(key[32:64], byteorder='big')
        self.chain = int.from_bytes(key[64:], byteorder='big')

        # Check that this is a valid keypair
        assert ((self.x ** 3 + 7 - self.y ** 2) % p == 0)


if __name__ == "__main__":
    # Find the Solo key
    client = solo.client.find()

    wallet = Wallet(client.ctap2.device.call(CMD_PUBKEY))

    client.ctap2.device.call(CMD_RESET)
