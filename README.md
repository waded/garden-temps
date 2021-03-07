# garden-temps

Service to publish data from DS18B20 sensors attached to a Raspberry Pi's one-wire interface to MQTT.

# Assumptions

- You've learned to enable one-wire on the Pi, and wired up 1 or more DS18B20s to the configured pin and no other one-wire devices (tip: `dtoverlay=w1-gpio`, and the default one-wire pin's GPIO 4. You also need 3v3 power and ground. [https://pinout.xyz/])
- You've learned how to identify each sensor's ID (tip: `ls /sys/bus/w1/devices/`)
- You've learned to run containers on your Pi (tip: use what Balena Cloud provides, it's click-flash-click-deploy from GitHub easy.)

# Configuration

By environment variables,

    MQTT_BROKER: the hostname or IP of an MQTT broker
    DEVICE_PATH: typically /sys/bus/w1/devices/    
    INTERVAL_S: the number of seconds to sleep between checks. Note sometimes the 
