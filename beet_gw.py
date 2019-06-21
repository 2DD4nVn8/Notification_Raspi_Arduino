from xbee import ZigBee
import paho.mqtt.client as mqtt
import struct
import ast
import serial
import json
from ast import literal_eval


PORT = '/dev/ttyUSB0'
BAND_RATE = 9600
SERIAL_PORT = serial.Serial(PORT,BAND_RATE)
#MQTT_BROKER_ADDR = '172.29.156.83'
#MQTT_BROKER_PORT = 1883
MQTT_FILE = "/home/pi/Desktop/mqtt/mqtt.txt"
BEAT_MAC = 0x0013A200415411D3
SUB_MAIN_TOPIC = "Beep/#"

mqtt_broker = open(MQTT_FILE).read()
mqtt_dict = literal_eval(mqtt_broker)
print(mqtt_dict)
MQTT_BROKER_ADDR = mqtt_dict['MQTT_BROKER_ADDR']
MQTT_BROKER_PORT = mqtt_dict['MQTT_BROKER_PORT']

def onConnect(publisher, user_data, flags, response_code):
    print("response code: {0}".format(response_code))
    publisher.subscribe(SUB_MAIN_TOPIC, 0)

def is_json_format(line):
    try:
        json.loads(line)
        return True
    except json.JSONDecodeError:
        return False

def onMessage(publisher, user_data, msg):
    print("topic: " + msg.topic)
    print("subtopic " + msg.topic.split("/")[1])
    print("payload: " + str(msg.payload.decode('utf-8')))
    print(msg.payload)
    if is_json_format(msg.payload.decode('utf-8')) == True:
        payload_DICT = ast.literal_eval(msg.payload.decode('utf-8'))
        print(payload_DICT)
    
        if msg.topic.split("/")[1] == "famima":
            if payload_DICT["beep"] == "on":
                print("beep")
        
                xbee.send('tx',dest_addr_long=struct.pack('>q',BEAT_MAC),options=b'\x01',data=b"famima\0")
                print("send")
                print()


if __name__ == '__main__':
    xbee = ZigBee(SERIAL_PORT, escaped=True)
    
    mqtt_subscriber = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_subscriber.on_connect = onConnect
    mqtt_subscriber.on_message = onMessage
    mqtt_subscriber.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)

    #xbee.send('tx',dest_addr_long=struct.pack('>q',BEAT_MAC),options=b'\x01',data=b"famima\0")

try:
    mqtt_subscriber.loop_forever()
except KeyboardInterrupt:
    None
