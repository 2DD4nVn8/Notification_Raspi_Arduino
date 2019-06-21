from xbee import ZigBee
import paho.mqtt.client as mqtt
import struct
import ast
import serial
import json
from ast import literal_eval

#MQTT_BROKER_ADDR = '172.29.156.89'
#MQTT_BROKER_PORT = 1883
#BEAT_MAC = 0x0013A200415411D3
MQTT_FILE = "/home/pi/Desktop/mqtt/mqtt.txt"
mqtt_broker = open(MQTT_FILE).read()
mqtt_dict = literal_eval(mqtt_broker)
MQTT_BROKER_ADDR = mqtt_dict['MQTT_BROKER_ADDR']
MQTT_BROKER_PORT = mqtt_dict['MQTT_BROKER_PORT']

SUB_TOPIC = "inouelab/sensing_part/electric_pot"
PUB_TOPIC = "Beep/famima"

def onConnect(publisher, user_data, flags, response_code):
    print("response code: {0}".format(response_code))
    publisher.subscribe(SUB_TOPIC, 0)



def onMessage(publisher, user_data, msg):
    print("topic: " + msg.topic)
    print("subtopic " + msg.topic.split("/")[1])
    print("payload: " + str(msg.payload.decode('utf-8')))
    print(msg.payload)
    payload_DICT = ast.literal_eval(msg.payload.decode('utf-8'))
    
    if payload_DICT["electric_pot"] == "off":
        print("沸いた")
        pub_Message = '{"beep":"on"}'
        mqtt_publisher.publish(PUB_TOPIC,pub_Message,qos=0)
        print("send")
        print()


if __name__ == '__main__':    
    mqtt_subscriber = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_subscriber.on_connect = onConnect
    mqtt_subscriber.on_message = onMessage
    mqtt_subscriber.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)

    mqtt_publisher = mqtt.Client(protocol=mqtt.MQTTv31)
    mqtt_publisher.connect(host=MQTT_BROKER_ADDR, port=MQTT_BROKER_PORT, keepalive=0)


try:
    mqtt_subscriber.loop_forever()

except KeyboardInterrupt:
    None
