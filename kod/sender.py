import checksum as ch
from control_chars import *
from loader import FileLoader
from packet import XPacketSender
import serial as ps
import serial.tools.list_ports as lp

file = FileLoader(input("Podaj ścieżkę do pliku do wysłania: "))

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

# otwarcie połączenia
print("Otwieram połączenie na " + choosen_port)
conn = ps.Serial(choosen_port, timeout=3, inter_byte_timeout=1) # inter_byte_timeout=1 <- odpowiada za poprawne działanie, nowe komputery są za szybkie
conn.flush()


print("Oczekuję na rozpoczęcie transmisji")
while True:
    method = conn.read(1)
    if method == b'': continue          # nic nieodebrano = czekaj dalej
    if method == NAK: method = ch.sum   # NAK = suma kontrolna to suma algebraiczna
    if method == C  : method = ch.crc   # c   = suma kontrolna to CRC
    break

print("Wykryto chęć odebrania pliku. Rozpoczynam transmisję")

packet = XPacketSender(method)

while not file.isEOF():
    conn.write(packet.sendPacket(file.readNext()))
    while True:
        tmp = conn.read(1)
        # Jeżeli ACK to przejdź do kroku dalej 
        if tmp == ACK: break
        if tmp == b'': continue
        # Jeżeli NAK to powtórz
        if tmp == NAK:
            conn.write(packet.sendPacket())
            continue

print("Wysłałem plik. Kończę transmisję")

while True:
    # Jak koniec to wyślij EOT
    conn.write(EOT)
    tmp = conn.read(1)
    # Jeżeli nie otrzymano ACK (potwierdzenie odebrania wiadomości o końcu) powtórz 
    if tmp == ACK: break

print("Transmisja zakończona")