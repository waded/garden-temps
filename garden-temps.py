import os
import time
import paho.mqtt.client as mqtt

def read_temp(device_path):
    file = open(device_path, 'r')
    data = file.readlines()
    file.close()
    return float(data[1].split("t=")[1]) / 1000.0 * 9/5 + 32

def main():
    MQTT_USER = os.environ('MQTT_USER')
    MQTT_PWD = os.environ('MQTT_PWD')
    MQTT_BROKER = os.environ('MQTT_BROKER') # server name
    DEVICE_PATH = os.environ('DEVICE_PATH') # e.g. /sys/bus/w1/devices/
    INTERVAL_S = os.environ('INTERVAL_S') # seconds

    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, MQTT_PWD)
    client.connect(MQTT_BROKER)
    client.loop_start()
    while True:
        for file in os.listdir(DEVICE_PATH):
            device_path = os.path.join(DEVICE_PATH, file)
            device_path = os.path.join(device_path, 'w1_slave')
            temp = read_temp(device_path)
            event_name = file
            client.publish(event_name, temp)
                        
        time.sleep(int(INTERVAL_S))

main()