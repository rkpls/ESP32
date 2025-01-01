import network
import utime
import ubinascii
import json
from time import sleep_ms
from machine import Pin, SoftI2C
import machine
from umqtt.simple import MQTTClient
import gc
import ahtx0

i2c_sda = Pin(5)
i2c_scl = Pin(4)
i2c = SoftI2C(sda=i2c_sda, scl=i2c_scl)

sensor = ahtx0.AHT10(i2c)

ssid = 'Zenbook-14-Pals'
password = 'Micropython'
MQTT_SERVER = '192.168.178.1'
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_TOPIC = 'PLS'

temp = 0
humid = 0

def scan_i2c():
    print('Scan i2c')
    devices = i2c.scan()

    for device in devices:  
        print("Hex address: ",hex(device))
    if len(devices) == 0:
        print("No i2c device !")
    else:
        print('i2c devices found:',len(devices))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print(wlan.ifconfig())


def mqtt_send(server = MQTT_SERVER):
    global CLIENT_ID, MQTT_SERVER, MQTT_TOPIC, temp, humid
    client = MQTTClient(CLIENT_ID, MQTT_SERVER)
    client.connect()
    werte = {
        'Temp:': str(temp),
        'Humid': str(humid),
        'Hellig': str(bright)
        }
    dump = json.dumps(werte)
    client.publish(MQTT_TOPIC, dump)
    client.disconnect()

# ----------
        
scan_i2c()

gc.enable()

connect_wifi() 

while True:
    temp = int(sensor.temperature)
    humid = int(sensor.relative_humidity)
    mqtt_send()
    sleep_ms(2000)
    
c.disconnect()



