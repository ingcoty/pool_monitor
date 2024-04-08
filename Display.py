import re
from ssd1306 import SSD1306_I2C
from machine import SoftI2C
from machine import Pin

class Display:
    
    def __init__(self):
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
        self.display = SSD1306_I2C(128, 32, i2c)
        self.msgs = ['','','']

    def text(self, msj:str, line):
        
        self.msgs[line] = msj
        
        self.display.fill(0)
        line = 0
        for msg in self.msgs:
            self.display.text(msg, 0, line, 1)
            line = line + 10
        
        self.display.show()
        