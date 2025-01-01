from machine import Pin, ADC, unique_id, reset
import machine
import gc
from utime import ticks_ms, ticks_diff, sleep_ms
import network
from ubinascii import hexlify
from umqtt.simple import MQTTClient
import json

# ---------- PINS ----------

adc_1 = ADC(Pin(33))
adc_2 = ADC(Pin(32))
adc_3 = ADC(Pin(35))
adc_4 = ADC(Pin(34))
adc_5 = ADC(Pin(36))
adc_6 = ADC(Pin(39))

adc_1.atten(ADC.ATTN_11DB)
adc_2.atten(ADC.ATTN_11DB)
adc_3.atten(ADC.ATTN_11DB)
adc_4.atten(ADC.ATTN_11DB)
adc_5.atten(ADC.ATTN_11DB)
adc_6.atten(ADC.ATTN_11DB)

# ---------- DATA ----------
U1 = []
U2 = []
U3 = []
I1 = []
I2 = []
I3 = []

# ---------- CONNECT ----------
ssid = 'zzz'
password = 'fck_afd'
wlan = network.WLAN(network.STA_IF)
MQTT_SERVER = '192.168.2.45'
CLIENT_ID = hexlify(unique_id())
MQTT_TOPIC = '/home/energy/*'

# ---------- DEFS----------
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print(wlan.ifconfig())
    return wlan

def average(values):
    if len(values) > 0:
        if len(values) > 8:
            values.pop(0)
        return sum(values) / len(values)
    else:
        return 0


def read_data():
    global U1, U2, U3, I1, I2, I3
    U1.append(adc_1.read())
    U2.append(adc_2.read())
    U3.append(adc_3.read())
    I1.append(adc_4.read())
    I2.append(adc_5.read())
    I3.append(adc_6.read())

def mqtt_send():
    global CLIENT_ID, MQTT_SERVER, MQTT_TOPIC, U1, U2, U3, I1, I2, I3
    client = MQTTClient(CLIENT_ID, MQTT_SERVER)
    client.connect()
    data = {
        "U1": int(average(U1)),
        "U2": int(average(U2)),
        "U3": int(average(U3)),
        "I1": int(average(I1)),
        "I2": int(average(I2)),
        "I3": int(average(I3))
        }
    dump = json.dumps(data)
    print(str(dump))
    client.publish(MQTT_TOPIC, dump)
    client.disconnect()
        
    U1.clear()
    U2.clear()
    U3.clear()
    I1.clear()
    I2.clear()
    I3.clear()

# ---------- START ----------

gc.enable()
connect_wifi()

# ---------- LOOP ----------

try:
    passed = 0
    while True:
        read_data()
        sleep_ms(10)
        time = ticks_ms()
        if (ticks_diff(time, passed) >= 1000):
            mqtt_send()
            passed = time
            
except Exception as e:
    print("MQTT Error:", e)
    sleep_ms(10000)
    reset()

