from micropython import const

class CC3100:
    """Micropython CC3100 Class - currently WIP"""
    def __init__(self):
        
class CC3100_I2C(CC3100):
    def __init__(self, i2c, addr=0x3c):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__()

    def write_cmd(self, cmd):
        self.temp[0] = 0
        self.temp[1] = 0
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.temp[0] = self.addr << 1
        self.temp[1] = 0
        self.i2c.start()
        self.i2c.write(self.temp)
        self.i2c.write(buf)
        self.i2c.stop()
        
class CC3100_SPI(CC3100):
    def __init__(self, spi, cs):
        self.rate = 10000000
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.cs = cs
        super().__init__()

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.value(True)
        self.cs.value(False)
        self.spi.write(bytearray([cmd]))
        self.cs.value(True)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.value(True)
        self.cs.value(False)
        self.spi.write(buf)
        self.cs.value(True)
