import os
import time
from datetime import datetime

import paho.mqtt.client as mqtt


def read_temp(device_file):
    with open(device_file, 'r') as f:
        data = f.readlines()

    temp_c = float(data[1].split("t=")[1]) / 1000.0
    temp_f = temp_c * 9.0/5.0 + 32
    return round(temp_f, 1)

def main():     
    MQTT_BROKER = os.getenv('MQTT_BROKER') # e.g. hostname or IP    
    MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
    MQTT_USERNAME = os.getenv('MQTT_USERNAME')
    MQTT_PASSWORD = os.getenv('MQTT_PASSWORD')
    MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'garden-temps')
    DEVICE_PATH = os.getenv('DEVICE_PATH', '/sys/bus/w1/devices/')
    INTERVAL = int(os.getenv('INTERVAL', '60'))

    print(f'connecting to {MQTT_BROKER}:{MQTT_PORT}')

    client = mqtt.Client()
    if MQTT_USERNAME is not None:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, port=MQTT_PORT)
    client.loop_start()

    print(f'sending to -h {MQTT_BROKER}:{MQTT_PORT} -t {MQTT_TOPIC}')

    while True:
        now = datetime.now().isoformat(timespec='seconds')

        print(f'tick: {now}')

        for f in os.listdir(DEVICE_PATH):
            device_file = os.path.join(DEVICE_PATH, f, 'w1_slave')
            if (os.path.isfile(device_file)):
                temp = read_temp(device_file)
                topic = f'{MQTT_TOPIC}'
                message = f'{f},{now},{temp}'
                client.publish(topic, message)

        time.sleep(INTERVAL)

main()
