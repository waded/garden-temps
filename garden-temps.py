from datetime import datetime
import os
import time
import paho.mqtt.client as mqtt

def read_temp(device_path):
    file = open(device_path, 'r')
    data = file.readlines()
    file.close()
    return round(float(data[1].split("t=")[1]) / 1000.0 * 9.0/5.0 + 32, 1)

def main():
    MQTT_BROKER = os.getenv('MQTT_BROKER') # e.g. hostname/IP
    DEVICE_PATH = os.getenv('DEVICE_PATH') # e.g. /sys/bus/w1/devices/
    INTERVAL_S = os.getenv('INTERVAL_S') # seconds

    print(f'garden-temps sending temp data to {MQTT_BROKER}')

    client = mqtt.Client()
    client.connect(MQTT_BROKER)
    client.loop_start()
    while True:
        print('tick')
        now = datetime.now().isoformat(timespec='seconds')

        for file in os.listdir(DEVICE_PATH):
            device_path = os.path.join(DEVICE_PATH, file)
            device_path = os.path.join(device_path, 'w1_slave')
            if (os.path.isfile(device_path)):
                temp = read_temp(device_path)
                event_name = file            
                client.publish('temperature', f'{now},{file},{temp}')

        time.sleep(int(INTERVAL_S))

main()