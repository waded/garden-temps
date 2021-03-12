# garden-temps

Service to publish temperatures from DS18B20 sensors attached to a Raspberry Pi's one-wire interface to MQTT.

I used this to survey soil temperatures in garden boxes, to satisfy curiousity about how much those varied, compared to weather, water, and the sun each box gets.

> Wade: ... I'm going to build these different gardens, with boxes, and it'll all be drip-lined with a lot of sensors. You
> know, like ancient Egypt."
> 
> Someone: "You drew up plans for this?"
> 
> Wade: "No, no. It's all in my head."

## Expectations, and tips to get you there

- You've learned to enable one-wire on the Pi. You've wired up 1 or more DS18B20s to the configured pin, and no other one-wire devices (Tips: google `dtoverlay=w1-gpio`, and the default data pin's GPIO 4. <https://pinout.xyz> is helpful as a reminder where GPIO 4 is, 3v3 Power and Ground. You may want a 4.7K resistor between data and power, unless you've enabled built-in pull-up, which I've never tried since I have the resistors.)
- You've learned to run & manage containers on your Pi (Tip: you can go deep on this, but Balena Cloud makes this, and everything else about operating containers on headless single-board computers super easy - click-flash-click-deploy easy, [like this.](https://dashboard.balena-cloud.com/deploy) If you use Balena Cloud/OS, don't forget about enabling w1-gpio using *Define DT overlays* under a device's *Device Configuration*)
- You've learned to identify each sensor's ID (Tip: `ls /sys/bus/w1/devices/`)

## Configuration

Required environment variables:

- MQTT_BROKER: hostname or IP of an MQTT broker

Optional:

- MQTT_USERNAME
- MQTT_PASSWORD
- MQTT_USETLS: set `True` if TLS is required
- MQTT_CLIENTID: client ID to use if a random ID isn't desired
- MQTT_PORT: port number, e.g. secured port `8883`, if `1883` isn't desired
- MQTT_TOPIC: root path to use for topics, if `garden-temps` isn't desired
- INTERVAL: number of seconds to wait between sensor sweeps, if `60` isn't desired. Note that sweeps aren't instantaneous - it depends on number of sensors, quality of signal - so total time for each measurement is INTERVAL + each sweep.
- DEVICE_PATH: if typical `/sys/bus/w1/devices/` isn't desired

## Usage example

Let's say I'm running [mosquitto](https://mosquitto.org/) on 192.168.0.10 on default port 1883, no username/password.

When running the container on a Pi on this subnet, I set environment variables:

- MQTT_BROKER: `192.168.0.10`

Now I `mosquitto_sub -t garden-temps/# -h 192.168.0.10` and every 60 seconds with 5 sensors connected I receive messages like:

    {"sensor": "28-01204bcb1a00", "time": "2021-03-07T01:39:09", "temp_F": 33.9, "temp_C": 1.1}
    {"sensor": "28-01204c9fb29c", "time": "2021-03-07T01:39:09", "temp_F": 35.8, "temp_C": 2.1}
    {"sensor": "28-01204c5f8d3c", "time": "2021-03-07T01:39:09", "temp_F": 32.6, "temp_C": 0.3}
    {"sensor": "28-01204c68e858", "time": "2021-03-07T01:39:09", "temp_F": 32.7, "temp_C": 0.4}
    {"sensor": "28-01204cb9c15f", "time": "2021-03-07T01:39:09", "temp_F": 32.6, "temp_C": 0.3}

Each message includes the sensor's ID, device timestamp at start of the sweep, temperatures in Fahrenheit and Celsius.

These could be consumed as-is, or handled and sent to a database, Exceltabase, etc.

## Troubleshooting

If a sensor's not working quite right you'll get 185F/85C (the default value DS18B20 resets to) or 32F/0C (not sure why that happens.)
