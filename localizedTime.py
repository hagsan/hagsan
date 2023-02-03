import time
import machine
from machine import RTC
import pcf8563

i2c = machine.I2C(0, sda=machine.Pin(21), scl=machine.Pin(22), freq=400000)
pcf = pcf8563.PCF8563(i2c)

def getcet():
    year = time.localtime()[0]       #get current year
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    now=time.time()
    if now < HHMarch :               # we are before last sunday of march
        cet=time.localtime(now+3600) # CET:  UTC+1H
    elif now < HHOctober :           # we are before last sunday of october
        cet=time.localtime(now+7200) # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet=time.localtime(now+3600) # CET:  UTC+1H
    return(cet)

def getdatetime():
    time = pcf.datetime()
    return time

def gettimestring():
    timestamp = pcf.datetime()
    print(timestamp)
    print(getcet())
    timestring = "%02d:%02d" % (timestamp[3:5])
    return timestring

def setpcftime():
    datetime = getcet()
    year = datetime[0]
    month = datetime[1]-1
    day = datetime[2]-1
    hour = datetime[3]
    minute = datetime[4]
    second = datetime[5]
    weekday = datetime[6]
    setdatetime = (year, month, day, hour, minute, second, weekday)
    pcf.datetime(setdatetime)
    print(pcf.datetime())
    print('pcf time has been set')

def getdatestring():
    days = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    months = {0: "Jan", 1: "Feb", 2: "Mar", 3: "Apr", 4: "May", 5: "Jun", 6: "Jul", 7: "Aug", 8: "Sep", 9: "Oct", 10: "Nov", 11: "Dec"}
    timestamp = pcf.datetime()
    datestring = "%s, %02d %s '%02d" % (days[timestamp[6]],timestamp[2]+1,months[timestamp[1]],(timestamp[0]-2000))
    return datestring