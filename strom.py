from machine import Pin, ADC
import time

adc_1 = ADC(Pin(25))
adc_2 = ADC(Pin(26))
adc_3 = ADC(Pin(27))
adc_4 = ADC(Pin(36))
adc_5 = ADC(Pin(39))
adc_6 = ADC(Pin(34))
adc_7 = ADC(Pin(35))

adc_1.atten(ADC.ATTN_11DB)
adc_2.atten(ADC.ATTN_11DB)
adc_3.atten(ADC.ATTN_11DB)
adc_4.atten(ADC.ATTN_11DB)
adc_5.atten(ADC.ATTN_11DB)
adc_6.atten(ADC.ATTN_11DB)
adc_7.atten(ADC.ATTN_11DB)

data_1 = []
data_2 = []
data_3 = []
data_4 = []
data_5 = []
data_6 = []
data_7 = []

def extend(data_reading, data_set):
    data_set.append(data_reading)

def return_volts(data_set):
    if data_set:
        avg_value = sum(data_set) / len(data_set)
        volts = avg_value
        #print(volts)
    else:
        print("Data set is empty")
        
def return_amps(data_set):
    if data_set:
        avg_value = sum(data_set) / len(data_set)
        amps = avg_value
        print(amps)
    else:
        print("Data set is empty")

while True:
    loop_start = time.ticks_ms()
    
    while time.ticks_diff(time.ticks_ms(), loop_start) < 1000:
        read_1 = adc_1.read()
        read_2 = adc_2.read()
        read_3 = adc_3.read()
        read_4 = adc_4.read()
        read_5 = adc_5.read()
        read_6 = adc_6.read()
        read_7 = adc_7.read()

        extend(read_1, data_1)
        extend(read_2, data_2)
        extend(read_3, data_3)
        extend(read_4, data_4)
        extend(read_5, data_5)
        extend(read_6, data_6)
        extend(read_7, data_7)
    
    return_volts(data_1)
    return_volts(data_2)
    return_volts(data_3)
    return_amps(data_4)
    return_amps(data_5)
    return_amps(data_6)
    return_amps(data_7)
    print("------")

    data_1.clear()
    data_2.clear()
    data_3.clear()
    data_4.clear()
    data_5.clear()
    data_6.clear()
    data_7.clear()