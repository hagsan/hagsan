import epaper1in54
import machine
import esp32
import localizedTime
import wifimanager
import watchface
import batterymanager
from machine import Pin, SPI, RTC
from time import sleep, sleep_ms
from ntptime import settime

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woken up from deep sleep')

up_button = Pin(35, mode = Pin.IN)
down_button = Pin(4, mode = Pin.IN)
menu_button = Pin(26, mode = Pin.IN)
back_button = Pin(25, mode = Pin.IN)
esp32.wake_on_ext1(pins = (up_button, down_button, menu_button, back_button), level=esp32.WAKEUP_ANY_HIGH)

# SPI2 on ESP32
sck  = Pin(18)
miso = Pin(32)
mosi = Pin(23)
cs   = Pin(5, Pin.OUT)
dc   = Pin(10, Pin.OUT)
rst  = Pin(9, Pin.OUT)
busy = Pin(19, Pin.OUT)

spi  = SPI(2, baudrate=20000000, polarity=0, phase=0)

e = epaper1in54.EPD(spi, cs, dc, rst, busy)

w = 200
h = 200
x = 0
y = 0

def partial_update():
    e.clear_frame_memory(0xFF)
    buf = watchface.drawwatchface()
    e.init(e.PART_UPDATE)
    e.clear_frame_memory(0xFF)
    e.set_frame_memory(buf, x, y, w, h)
    e.display_frame_part()
    e.sleep()

def full_update():
    e.clear_frame_memory(0xFF)
    e.init((e.FULL_UPDATE))
    e.clear_frame_memory(0xFF)
    buf = watchface.drawwatchface()
    e.set_frame_memory(buf, x, y, w, h)
    e.display_frame()
    e.sleep()

if(up_button.value() == 1):
    print("pushed up button")
    try:
        wifimanager.do_connect()
        settime()
        localizedTime.setpcftime()
        wifimanager.close_connection()
    except:
        print("not able to reset time")
    full_update()
    sleep(5)
elif(menu_button.value() == 1):
    print("sw update mode")
    import webrepl
    webrepl.start()
    import network
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    print(ap_if.ifconfig())
    sleep(60)
    print("closing sw update mode")
elif(back_button.value() == 1):
    print("battery mode")
    batterymanager.get_battery_percentage()
    full_update()
    sleep(5)
elif(down_button.value() == 1):
    print("full update")
    full_update()
    sleep(5)
elif(localizedTime.getdatetime()[4] in {0,15,30,45}):
    full_update()
else:
    partial_update()

print("going to sleep")
machine.deepsleep(55000)