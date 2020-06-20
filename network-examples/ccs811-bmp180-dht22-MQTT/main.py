import i2c_read
import json
import time
import read_dht
import pycom
import _thread
from mqtt import MQTTClient

with open('config.json') as f:
    config = json.load(f)

def sub_cb(topic, msg):
    print((topic, msg))

def interval_send(t_):
    while True:
        send_value()
        time.sleep(t_)

def blink_led():
    for n in range(1):
        pycom.rgbled(0xfcfc03)
        time.sleep(0.5)
        pycom.rgbled(0x000000)
        time.sleep(0.2)

def send_value():
    try:
        co2, voc, bmp_P, bmp_T = i2c_read.value()
        dht_T, dht_RH = read_dht.value()
        print('co2: ', co2) # two bytes
        print('voc: ', voc) # two bytes
        print('bmp P: ', bmp_P) # range of BMP180 300 as min and 1100 as max 800 range, 0,02hPa acc. Atm pressure.
        print('bmp temp: ', bmp_T) # -40  +85 range. 125 total range. one byte
        print('dht temp: ', dht_T) # one byte
        print('dht RH: ', dht_RH) # one byte
        c.publish(topic_pub,'{"co2":' + str(co2) +
                          ',"voc":'+ str(voc) +
                          ',"bmp P":' + str(bmp_P) +
                          ',"bmp temp":' + str(bmp_T) +
                          ',"dht temp":' + str(dht_T) +
                          ',"dht RH":' + str(dht_RH) +
                          '}')
        blink_led()

    except (NameError, ValueError, TypeError):
        pass


# topic = 'testtopic7891/1'
# broker_url = 'broker.hivemq.com' # HiveMQ can be used for testing, open broker
topic_pub = 'devices/office-sens/'
topic_sub = 'devices/office-sens/control'
broker_url = 'sjolab.lnu.se'
client_name = 'office-sensor-1'

c = MQTTClient(client_name,broker_url,user=config['user_mqtt'],password=config['pass_mqtt'])
c.set_callback(sub_cb)
c.connect()
c.subscribe(topic_sub)

def listen_command():
    while True:
        if True:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(3)

#_thread.start_new_thread(interval_send,[10])