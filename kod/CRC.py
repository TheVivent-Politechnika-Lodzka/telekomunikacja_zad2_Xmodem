def calc_crc(data : bytes):
    # funkcja generująca nagłówek CRC
    # zmiana na tablicę bajtową
    data = bytearray(data)
    crc = 0x0000
    for i in range(0, len(data)):
        # instrukcja xor i przesunięcie 8 bitów
        crc ^= data[i] << 8
        for j in range(0, 8):
            # koniunkcja
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF