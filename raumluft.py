from time import sleep_ms
from machine import Pin, SoftI2C, SoftSPI

from bme280_float import BME280
import CCS811
import mq135
import sh1106

#   - D7 - GPIO 13  - Din / MOSI fixed
#   - D5 - GPIO 14  - Clk / Sck fixed
#   - D8 - GPIO 4   - CS (optional, if the only connected device)
#   - D2 - GPIO 5   - D/C
#   - D1 - GPIO 2   - Res

i2c_ccs = SoftI2C(sda=Pin(12), scl=Pin(13))
s = CCS811.CCS811(i2c_ccs, addr=0x5a)

lufter = Pin(25,Pin.OUT)

pin_bme_sda = 27
pin_bme_scl = 14

pin_ccs_sda = 12
pin_ccs_scl = 13

sda_pin = 22
scl_pin = 23

spi = SoftSPI(sda = sda_pin, scl = scl_pin, baudrate=100000)
dc = Pin(19)
res = Pin(21)
cs = Pin(18)

oled = sh1106.SH1106_SPI(128, 64, spi, Pin(21), Pin(18), Pin(19))

lufter.on()
i2c_bme = SoftI2C(scl=Pin(pin_bme_scl), sda=Pin(pin_bme_sda), freq=100000)
bme280 = BME280(i2c=i2c_bme)
while True:
    print(bme280.values)
    if s.data_ready():
        print('eCO2: %d ppm, TVOC: %d ppb' % (s.eCO2, s.tVOC))
        sleep_ms(1000)
    oled.fill(0)
    oled.show()
    oled.text("Hello, MicroPython!", 0, 0)
    oled.show()
