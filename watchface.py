import framebuf
import orbitron_medium_40, orbitron_regular_20
import localizedTime
import batterymanager
from writer import Writer

class epaperDisplay(framebuf.FrameBuffer):
    def __init__(self, width, height, buffer):
        self.width = width
        self.height = height
        self.buffer = buffer
        self.mode = framebuf.MONO_HLSB
        super().__init__(self.buffer, self.width, self.height, self.mode)

    def show(self):
        ...

w = 200
h = 200
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
black = 0
white = 1
my_display = epaperDisplay(w, h, buf)

def drawwatchface():
    time = localizedTime.gettimestring()
    date = localizedTime.getdatestring()
    batt_percentage = batterymanager.get_battery_percentage()
    batt_percentage_str = str(batt_percentage) + "%"
    fb.fill(white)
    font = orbitron_medium_40
    wri = Writer(my_display, font)
    Writer.set_textpos(my_display, 0, 0)
    wri.printstring(time, invert=True)
    font = orbitron_regular_20
    wri = Writer(my_display, font)
    Writer.set_textpos(my_display, 50, 0)
    wri.printstring(date, invert=True)
    wri = Writer(my_display, font)
    Writer.set_textpos(my_display, 80, 0)
    wri.printstring(batt_percentage_str, invert=True)
    return buf