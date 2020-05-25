import time

def serial(spi):
    # Wait for GBA
    k = b'\x00\x00\x00\x00'
    while k != b'\xca\xfe\xfa\xce':
        buf = [0xAA, 0xBB, 0xCC, 0xDD]
        k = spi.exchange(buf, 4, start=False, stop=False, duplex=True)


def monitor(spi):
    # Serial console
    s = ""
    while True:
        buf = [0xFA, 0xCE, 0xCA, 0xFE]
        val = spi.exchange(buf, 4, start=False, stop=False, duplex=True)
        if val[1:3] != b'\xff\xff': 
            if val == b'\xca\xfe\xfa\xce':
                continue
            val[0] ^= 0x80
            if val != b'\x00\x00\x00\x00':
                s += chr(val[3])
            else:
                print(s, end='', flush=True)
                s = ""

        time.sleep(0.005)
