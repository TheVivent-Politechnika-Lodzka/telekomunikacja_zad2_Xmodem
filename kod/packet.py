from control_chars import *

class XPacketSender:

    method                  = None
    start                   = SOH
    packet_number           = 0
    packet_number_reversed  = 255
    data                    = b''
    checksum                = b''

    def __init__(self, method):
        # zapisanie metody obliczania sumy kontrolnej
        self.method = method

    def sendPacket(self, data=None):
        # jeżeli podano dane, to zaaktualizuj klasę
        # jeżeli nie, to wyślij to samo co wcześniej
        if data != None:
            self.__iteratePacketNumber()
            self.data = data
            self.checksum = self.method(self.data)

        # połącz dane i wyślij
        return self.start\
            + self.packet_number.to_bytes(1, "big")\
            + self.packet_number_reversed.to_bytes(1, "big")\
            + self.data\
            + self.checksum

    def __iteratePacketNumber(self):
        # ziteruj numer pakietu
        self.packet_number          += 1
        self.packet_number_reversed -= 1
        # jeżeli przekracza zakres, to napraw
        if self.packet_number > 255:
            self.packet_number = 0
        if self.packet_number_reversed < 0:
            self.packet_number_reversed = 255

class XPacketReceiver:

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
        return method(self.data) == self.checksum