import serial as ps  # załaduj pyserial
from loader import FileLoader

SOH = 0x01  # Start of Header
EOT = 0x04  # End of Transmission
ACK = 0x06  # Acknowledge
NAK = 0x15  # Not Acknowledge
ETB = 0x17  # End of Transmission Block (Return to Amulet OS mode)
CAN = 0x18  # Cancel (Force receiver to start sending C's)
C   = 0x43  # ASCII "C" (CRC?)
