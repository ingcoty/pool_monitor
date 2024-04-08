from machine import Pin
import machine
import utime

class Srt04t:

    def __init__(self, triger_pin:int, echo_pin:int):
        self.triger = Pin(triger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)


    def read_distance(self) -> int:
        sum = 0
        for i in range(10):
            self.triger.value(0)
            utime.sleep_us(20000)
            self.triger.value(1)
            utime.sleep_us(15)
            self.triger.value(0)
            pulse = machine.time_pulse_us(self.echo, 1)
            distance = pulse*0.034/2
            sum = sum + distance

        mean = int(sum/10)
        return(mean)