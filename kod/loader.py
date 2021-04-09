class FileLoader:
    
    current = b''
    EOF = False

    def __init__(self, path):
        # otorzenie pliku do odczytu(r) binarnego(b)
        self.file = open(path, "rb")


    def readNext(self, amount=128):
        # dzielenie na bloki o rozmiarze 128B 
        self.current = self.file.read(amount)
        # uzupełnienie do 128
        while len(self.current) < 128:
            # uzupełnianie pustym znakiem null
            self.current += b'\x00' * 8 
            # ustawienie flagi końca pliku
            self.EOF = True
        return self.current

    def repeat(self):
        # powtarzanie ostatniego przesłanego bloku
        return self.current

    def isEOF(self):
        return self.EOF