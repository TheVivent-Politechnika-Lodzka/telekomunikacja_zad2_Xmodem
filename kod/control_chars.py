SOH = b'\x01'
'''Start of Header'''

EOT = b'\x04'
'''End of Transmission'''

ACK = b'\x06'
'''Acknowledge'''

NAK = b'\x15'
'''Not Acknowledge'''

ETB = b'\x17'
'''End of Transmission Block (Return to Amulet OS mode)'''

CAN = b'\x18'
'''Cancel (Force receiver to start sending C's)'''

C   = b'\x43'
'''ASCII C (CRC?)'''
