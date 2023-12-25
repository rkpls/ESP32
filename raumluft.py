import utime
from machine import Pin, SoftI2C, SoftSPI

from bme280_float import *
import CCS811
from mq135 import MQ135
import sh1106

pin_bme_sda = 27
pin_bme_scl = 14
pin_ccs_sda = 12
pin_ccs_scl = 13

pin_MQ_AO = Pin(21)
pin_MQ_DO = Pin(19)

pin_sck = 23
pin_sda = 22
pin_res = 21
pin_dc = 19
pin_cs = 18
pin_miso = 15

pin_dc = 1
pin_res = 3

pin_air = Pin(25)
pin_rpm = Pin(26, Pin.IN)

i2c_bme = SoftI2C(scl=Pin(pin_bme_scl), sda=Pin(pin_bme_sda), freq=100000)
i2c_ccs = SoftI2C(scl=Pin(pin_ccs_scl), sda=Pin(pin_ccs_sda), freq=100000)

pin_air.value(1)
pin_air.on()

bme280 = BME280(i2c=i2c_bme)
s = CCS811.CCS811(i2c=i2c_ccs)

spi = SoftSPI(sck=Pin(23), mosi=Pin(22), miso=Pin(15), baudrate=400000)
oled = sh1106.SH1106_SPI(128, 64, spi, Pin(18), Pin(15), Pin(19))

