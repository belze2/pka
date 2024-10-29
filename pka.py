### picturekeys advanced python3 hiding ###
'''
   
    '''
class Materials:
    def __init__(self, pictureFileName='materials/hubble.png'):
        # setup keys with a pictue file 
        self.KEYDATA = []
        self.keysize = 1024
        self.keypartbuffer = ''
        self.blockcounts = -7   # avoiding PNG Header
        self.cap = 99
        self.part = None
        self.pictureFileName = pictureFileName
        self.trail = [self.cap]
        self.block = ''
        self.memory = None
        
        if pictureFileName:
            self.keyObj = open(pictureFileName, 'rb')
            # fill KEYDATA with 1024 byte-blocks
            # use block of reading to set self.part(the active key)
            while self._reading():
                self.blockcounts += 1
                if self.blockcounts >= 0 and len(self.keypartbuffer) == self.keysize:
                    self.KEYDATA.append(self.keypartbuffer)
                
                    if len(self.keypartbuffer) == self.keysize:
                        if self.blockcounts == self.cap:
                            self.part = self.keypartbuffer
                            break
                elif len(self.keypartbuffer) < self.keysize:
                    break
                
            self.keyObj.close()
        
    def _reading(self):
        # returns 0 when the reading reaches the end
        self.keypartbuffer = ''
        self.keypartbuffer = self.keyObj.read(self.keysize)
        if self.keypartbuffer != '': return 1
        else: return 0
        
    def _ciph(self, ordl):
        # cycle too high or low bytevalues
        if ordl > 255: return ordl - 256
        elif ordl < 0: return ordl + 256
        else: return ordl
        
    def changekey(self, index):
        # indexes between 0 and default 99 changes the used keypart
        if 0 < index < self.trail[0]:
            self.part = self.KEYDATA[index]
            print('*active key has been changed...')
        
    def decrypt(self, chipertext):
        # decrypt a chipertext via Picturebytes
        message = ''
        for k, item in enumerate(chipertext):
            message += chr(self._ciph(ord(item) - self.part[k])) # _ciph avoid under 0
        return message
    
    def encrypt(self, plaintext):
        # encrypt a plain textline
        feed = list(plaintext)
        r = ''
        for k, item in enumerate(feed):
            r += chr(self._ciph(ord(item) + self.part[k])) # _ciph avoid over 256
        return r
        
