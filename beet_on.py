import paho.mqtt.client as mqtt
from random import uniform
from time import sleep


mqtt_broker_addr = '172.29.156.83'
mqtt_broker_port = 1883
MAIN_TOPIC = "Beep/famima"

mqtt_publisher = mqtt.Client(protocol=mqtt.MQTTv31)
mqtt_publisher.connect(host=mqtt_broker_addr, port=mqtt_broker_port, keepalive=0)



try:
	mqtt_publisher.publish(MAIN_TOPIC, "ON", qos=0)
	mqtt_publisher.disconnect()

except KeyboardInterrupt:
	None
