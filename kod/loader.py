class FileLoader:
    
    NULL = 0x00
    
    def __init__(self, path):
        #otorzenie pliku do odczytu(r) binarnego(b)
        self.file = open(path, "rb")


    def readNext(self, amount=128):
        #dzielenie na bloki o rozmiarze 128B 
        data = self.file.read(amount)
        while len(data) < 128:
            data += self.NULL
        return data