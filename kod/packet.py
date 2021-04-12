from control_chars import *

class XPacket:

    start                   = SOH
    packet_number           = 0
    packet_number_reversed  = 255
    data                    = b''
    checksum                = b''

    def newPacket(self, buffer):
        # pierwszy Bajt - nagłówek SOH
        self.start                  = buffer[0].to_bytes(1, "big")
        if len(buffer) == 1: return
        # drugi Bajt - numer pakietu
        self.packet_number          = buffer[1]
        # trzeci Bajt - 255 odjąć numer pakietu
        self.packet_number_reversed = buffer[2]
        # wyczyszczenie starych danych
        self.data                   = b'' 
        # bajty 4-131 - dane
        for i in range(3, 131):
            self.data += buffer[i].to_bytes(1, "big")
        # bajty 132-133 - suma kontrolna
        self.checksum = buffer[131].to_bytes(1, "big")
        # jeżeli jest to CRC to dodajemy jeszcze jeden Bajt
        if len(buffer) == 133:
            self.checksum += buffer[132].to_bytes(1, "big")

    def getStart(self):
        return self.start
    
    def getPacketNumber(self):
        return self.packet_number

    def getPacketNumberReversed(self):
        return self.packet_number_reversed

    def getData(self):
        return self.data

    def getChecksum(self):
        return self.checksum
    
    def checkChecksum(self, method):
        # przeliczenie sumy kontrolnej danych i porównanie
        # z sumą otrzymaną w pakiecie
        # metodą podaną przez użytkownika (suma algb lub crc)
        sum_length = 1
        if len(self.checksum) == 2: sum_length = 2
        return method(self.data).to_bytes(sum_length, "big") == self.checksum