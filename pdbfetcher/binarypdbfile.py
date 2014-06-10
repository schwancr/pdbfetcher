

class BinaryPDBFile(object):
    def __init__(self):
        self.binary_text=''


    def __iter__(self):
        for line in self.readlines():
            yield line


    def write(self, text):
        self.binary_text += text


    def decompress(self):
        self.text = zlib.decompress(self.binary_text, 16 + zlib.MAX_WBITS)


    def read(self):
        if self.text is None:
            self.decompress()

        return self.text

    def readlines(self):
        if self.text is None:
            self.decompress()
        
        return self.text.split('\n')


    def load_traj(self):
        # argggggggh
