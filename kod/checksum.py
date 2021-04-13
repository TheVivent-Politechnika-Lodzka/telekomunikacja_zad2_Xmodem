def crc(data : bytes):
    # funkcja generująca nagłówek CRC
    # zmiana na tablicę bajtową
    data = bytearray(data)
    crc = 0
    for byte in data:
        crc ^= byte << 8
        for i in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return (crc & 0xFFFF).to_bytes(2, "big")

def sum(data : bytes):
    # funkcja generująca sumę algebraiczną
    data = bytearray(data)
    result = 0
    for byte in data:
        result += byte
        result %= 256
    return result.to_bytes(1, "big")