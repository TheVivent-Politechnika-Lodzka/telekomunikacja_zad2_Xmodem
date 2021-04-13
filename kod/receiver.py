import checksum as ch
from control_chars import *
from packet import XPacketReceiver
import serial as ps
import serial.tools.list_ports as lp

# gdzie zapisać plik
outFile = open(input("Podaj jak zapisać odbierany plik: "), 'wb')

# wybranie rodzaju sumy kontrolnej
control_sum = None
bytes_to_read = 132 # default jako suma kontrolna
print("1. Suma algebraiczna")
print("2. CRC")
print("Cokolwiek. Wyjscie z programu")
choice = input("Wybierz sposób potwierdzenia transmisji: ")
if choice == "1":
    control_sum = ch.sum
    C = NAK
elif choice == "2":
    control_sum = ch.crc
    bytes_to_read += 1 # CRC potrzebuje dodatkowego bajtu
else: exit()

# wylistowanie dostępnych portów
ports = sorted(lp.comports())
res_ports = []
print("Dostępne porty:")
i=0
for port, desc, hwid in ports:
    res_ports.append(port)
    print(str(i) + ". " + port)
    i += 1
if len(res_ports) == 0: exit("Brak dostępnych portów")
choosen_port = res_ports[int(input("Wybierz: "))]

print("Otwieram połączenie na " + choosen_port)
conn = ps.Serial(choosen_port, timeout=3, inter_byte_timeout=1) # inter_byte_timeout=1 <- odpowiada za poprawne działanie, nowe komputery są za szybkie
conn.flush()

# zainicjuj połączenie
buffer = XPacketReceiver()
while len(buffer.getData()) == 0:
    # wysłanie C <- zainicjiowanie odbioru z sumą kontrolną CRC
    conn.write(C)
    tmp = conn.read(bytes_to_read)
    if len(tmp) > 0: buffer.newPacket(tmp)

print("Połączenie ustanowione. Odbieram dane")

while buffer.getStart() != EOT:
    if not buffer.checkChecksum(control_sum):
        # wysłanie znaku sterującego NAK, proźba ponownego wysłania
        conn.write(NAK)
        # ponowne odczytanie pakietu
        tmp = conn.read(bytes_to_read)
        # jeżeli odebrany pakiet ma właściwą długość jest przekazywany dalej
        if len(tmp) == bytes_to_read: buffer.newPacket(tmp)
        continue
    # zapis widomości do pliku
    outFile.write(buffer.getData())
    # czyszczenie buforu
    conn.flush()
    # Wysłanie ACK <- potwierdzenie poprawnego odebrania pakietu
    conn.write(ACK)

    i = 0
    for i in range(20):
        # zapis otrzymanego pakietu
        tmp = conn.read(bytes_to_read)
        if len(tmp) > 0:
            # jeżeli długość jest większa od 0 to przekazuje otrzymany pakiet dalej
            buffer.newPacket(tmp)
            break
    # jeżeli przez minutę nie uda się otrzymać wiadomości, to zwróć błąd
    if i == 19: 
        conn.write(CAN)
        exit("Timeout")
    
# zakończenie połączenia (otrzymano EOT)
conn.write(ACK)

print("Połączenie zakończone. Plik odebrany")