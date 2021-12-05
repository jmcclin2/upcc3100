from micropython import const
from machine import Pin
import time

class CC3100:
    """Micropython CC3100 Class - currently WIP"""
    def __init__(self, nRst, nHib, intr):
        
        print("CC3100 Init...")
        
        # Setup nReset, nHibernate and interrupt
        nRst.init(nRst.OUT, value=0)
        nHib.init(nHib.OUT, value=1)
        intr.init(intr.IN)
        self.nRst = nRst
        self.nHib = nHib
        self.intr = intr
                       
        print("CC3100 Reset...")
        self.reset()
        print("CC3100 Out of Reset...")
        time.sleep_ms(1400)
        
    def reset(self):
        self.nRst.value(False)
        time.sleep_ms(3)
        self.nRst.value(True)
        time.sleep_ms(25)
        
    def _disable(self):
        self.nHib.value(False)
        time.sleep_ms(10)
        
    def _enable(self):
        self._disable()
        self.nHib.value(True)
        time.sleep_ms(50)
        
    def _msgRead(self):
        time.sleep(1);
        
    def _msgWrite(self):
        time.sleep(1);
        
    def _interrupt_handler(self, pin):
        self.intr.irq(trigger=0)
        print("_interrupt_handler")
        self.intr.irq(self._interrupt_handler, Pin.IRQ_RISING)
        
    def dataReadOp(self):
        time.sleep(1)
        
    def dataWriteOp(self):
        time.sleep(1)
        
    def start(self):
        self._disable()
        self.intr.irq(self._interrupt_handler, Pin.IRQ_RISING)
        self._enable()
        
class CC3100_I2C(CC3100):
    def __init__(self, i2c, nRst, nHib, intr, addr=0x3c):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        super().__init__(nRst, nHib, intr)

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
    def __init__(self, spi, cs, nRst, nHib, intr):
        self.rate = 10000000
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.cs = cs
        super().__init__(nRst, nHib, intr)
        
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
        
    def read_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs.value(True)
        self.cs.value(False)
        self.spi.recv(buf)
        self.cs.value(True)
