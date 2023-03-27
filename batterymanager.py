from machine import Pin, ADC
BATT_MIN_VOL = 28
BATT_MAX_VOL = 38

adc_pin=Pin(34, mode = Pin.IN)

def get_battery_percentage():
    adc = ADC(adc_pin)
    adc.atten(ADC.ATTN_11DB)
    val_u16 = adc.read_u16()
    voltage = val_u16 / 1000
    print("u16: " + (str(val_u16)))
    print("voltage: " + (str(voltage)))
    batt_percentage = round((voltage - BATT_MIN_VOL) / (BATT_MAX_VOL - BATT_MIN_VOL) * 100)
    print("Battery percentage: " + str(batt_percentage) + "%")
    return batt_percentage