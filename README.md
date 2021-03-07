# garden-temps

Service to publish tempeatures from DS18B20 sensors attached to a Raspberry Pi's one-wire interface to MQTT.

## Assumptions

- You've learned to enable one-wire on the Pi, and wired up 1 or more DS18B20s to the configured pin and no other one-wire devices (tip: `dtoverlay=w1-gpio`, and the default pin's GPIO 4. You also need 3v3 power and ground. https://pinout.xyz is helpful as a reminder where these are. You may want a 4.7K resistor between the signal and power, unless you've enabled built-in pull-up, which I never bother trying since I have the resistors.)
- You've learned how to identify each sensor's ID (tip: `ls /sys/bus/w1/devices/`)
- You've learned to run containers on your Pi (tip: you can go deep on this, but Balena Cloud makes everything else about this super easy - click-flash-click-deploy-easy. [Like this.](https://dashboard.balena-cloud.com/deploy) Don't forget about enabling w1-gpio if needed with the balenaOS version used.)

## Configuration

Required environment variables:

- MQTT_BROKER: hostname or IP of an MQTT broker
- DEVICE_PATH: typically `/sys/bus/w1/devices/`
- INTERVAL: number of seconds to sleep between sensor sweeps

Optional:

- None. (No, no support for username/password on MQTT.)

## Example usage

Let's say I'm running [mosquitto](https://mosquitto.org/) on 192.168.0.10 on default port 1883, no username/password.

When running the container, set environment variables

- MQTT_BROKER: `192.168.0.10`
- DEVICE_PATH: `/sys/bus/w1/devices/`
- INTERVAL: `60`

Now I `mosquitto_sub -t temperature/#` and every 60 seconds with 5 sensors connected I receive messages like:

    28-01204bcb1a00,2021-03-07T01:39:09,65.5
    28-01204c9fb29c,2021-03-07T01:39:09,65.4
    28-01204c5f8d3c,2021-03-07T01:39:09,65.2
    28-01204c68e858,2021-03-07T01:39:09,64.6
    28-01204cb9c15f,2021-03-07T01:39:09,64.5

These could be consumed as-is, or handled and sent to a database, Exceldabase, etc.