from machine import Pin,UART
import time
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17))
uart.init(bits=8, parity=None, stop=1)
