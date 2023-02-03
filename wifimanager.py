import network
from time import sleep

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    SSID = 'xxx'
    pw = 'xxx'
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, pw)
        sleep(5)
        while not sta_if.isconnected():
            print('could not connect')
            break
    print('network config:', sta_if.ifconfig())

def close_connection():
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        print('Closing connection to network...')
        sta_if.active(False)
    print('Connection Closed')