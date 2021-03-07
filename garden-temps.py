from datetime import datetime
import os
import time
import paho.mqtt.client as mqtt

def read_temp(device_file):
    with open(device_file, 'r') as f:
        data = f.readlines()

    temp_c = float(data[1].split("t=")[1]) / 1000.0
    temp_f = temp_c * 9.0/5.0 + 32
    return round(temp_f, 1)

def main():     
    MQTT_BROKER = os.getenv('MQTT_BROKER') # e.g. hostname or IP
    DEVICE_PATH = os.getenv('DEVICE_PATH') # typ. /sys/bus/w1/devices/
    INTERVAL = os.getenv('INTERVAL') # in seconds

    print(f'connecting to {MQTT_BROKER}')

    client = mqtt.Client()
    client.connect(MQTT_BROKER)
    client.loop_start()

    print(f'sending data to {MQTT_BROKER}')

    while True:
        now = datetime.now().isoformat(timespec='seconds')

        print(f'tick:{now}')

        for f in os.listdir(DEVICE_PATH):
            device_file = os.path.join(DEVICE_PATH, f, 'w1_slave')
            if (os.path.isfile(device_file)):
                temp = read_temp(device_file)
                event_name = f'temperature/{f}'
                message = f'{f},{now},{temp}'
                client.publish(event_name, message)

        time.sleep(int(INTERVAL))

main()