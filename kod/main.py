import serial as ps  # załaduj pyserial
from loader import FileLoader

SOH = 0x01  # Start of Header
EOT = 0x04  # End of Transmission
ACK = 0x06  # Acknowledge
NAK = 0x15  # Not Acknowledge
ETB = 0x17  # End of Transmission Block (Return to Amulet OS mode)
CAN = 0x18  # Cancel (Force receiver to start sending C's)
C   = 0x43  # ASCII "C" (CRC?)

# ser = ps.Serial()
# ser.baudrate = 19200
# ser.port = 'COM1'
# print(ser)
# #Serial<id=0xa81c10, open=False>(port='COM1', baudrate=19200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)
# ser.open()
# print(ser.is_open)

testFile = open("out.txt", "wb")

fl = FileLoader("test")
for i in range(11):
    print(len(fl.readNext()))