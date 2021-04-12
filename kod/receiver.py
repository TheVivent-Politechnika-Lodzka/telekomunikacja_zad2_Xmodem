import CRC
from control_chars import *
import serial as ps

# gdzie zapisać plik
outFile = open(input("Podaj jak zapisać odbierany plik: "), 'wb')

# wybranie rodzaju sumy kontrolnej
control_sum = None
bytes_to_read = 132 # default jako suma kontrolna
print("1. Suma kontrolna")
print("2. CRC")
print("Cokolwiek. Wyjscie z programu")
choice = input("Wybierz sposób potwierdzenia transmisji: ")
if choice == "1":
    control_sum = CRC.calc_crc
    C = NAK
elif choice == "2":
    control_sum = CRC.calc_crc
    bytes_to_read += 1 # CRC potrzebuje dodatkowego bajtu
else: exit()

print("Otwieram połączenie na COM1")
conn = ps.Serial("COM1", timeout=3)

# zainicjuj połączenie
buffer = b''
while len(buffer) == 0:
    conn.write(C)
    buffer = conn.read(bytes_to_read)


# print(buffer[bytes_to_read-2].to_bytes(1, "big"))
# print(buffer[bytes_to_read-1].to_bytes(1, "big"))
# print(int.from_bytes(buffer[bytes_to_read-2].to_bytes(1, "big") + buffer[bytes_to_read-1].to_bytes(1, "big"), "big"))

print("coś odbieram")
print(buffer)