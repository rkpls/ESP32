from machine import Pin, ADC
from time import sleep_ms, ticks_ms, ticks_diff

adc_1 = ADC(Pin(25))
adc_2 = ADC(Pin(26))
adc_3 = ADC(Pin(27))
adc_4 = ADC(Pin(34))
adc_5 = ADC(Pin(35))
adc_6 = ADC(Pin(32))
adc_7 = ADC(Pin(33))

adc_1.atten(ADC.ATTN_11DB)
adc_2.atten(ADC.ATTN_11DB)
adc_3.atten(ADC.ATTN_11DB)
adc_4.atten(ADC.ATTN_11DB)
adc_5.atten(ADC.ATTN_11DB)
adc_6.atten(ADC.ATTN_11DB)
adc_6.atten(ADC.ATTN_11DB)

while True:
    read_1 = adc_1.read()
    read_2 = adc_2.read()
    read_3 = adc_3.read()
    read_4 = adc_4.read()
    read_5 = adc_5.read()
    read_6 = adc_6.read()
    read_7 = adc_7.read()

    print("L1:", read_1)
    print("L2:", read_2)
    print("L3:", read_3)
    print("C1:", read_4)
    print("C2:", read_5)
    print("C3:", read_6)
    print("C4:", read_7)

    sleep_ms(5000)