# garden-temps

Service to publish temperatures from DS18B20 sensors attached to a Raspberry Pi's one-wire interface to MQTT.

I used this to survey soil temperatures through the day in garden boxes, to satisfy curiousity about how much it varied, and how it compared to weather and the amount of sun each box gets.

> Wade: ... I'm going to build these different gardens, with boxes, and it'll all be drip-lined with a lot of sensors. You
> know, like ancient Egypt."
> 
> Someone: "You drew up plans for this?"
> 
> Wade: "No, no. It's all in my head."

## Expectations, and tips to get you there

- You've learned to enable one-wire on the Pi. You've wired up 1 or more DS18B20s to the configured pin, and no other one-wire devices (Tips: google `dtoverlay=w1-gpio`, and the default data pin's GPIO 4. <https://pinout.xyz> is helpful as a reminder where GPIO 4 is, 3v3 Power and Ground. You may want a 4.7K resistor between data and power, unless you've enabled built-in pull-up, which I've never tried since I have the resistors.)
- You've learned to run & manage containers on your Pi (Tip: you can go deep on this, but Balena Cloud makes this, and everything else about operating containers on headless single-board computers super easy - click-flash-click-deploy easy, [like this.](https://dashboard.balena-cloud.com/deploy) Don't forget about enabling w1-gpio if needed with the balenaOS version used.)
- You've learned to identify each sensor's ID (Tip: `ls /sys/bus/w1/devices/`)

## Configuration

Required environment variables:

- MQTT_BROKER: hostname or IP of an MQTT broker
- DEVICE_PATH: typically `/sys/bus/w1/devices/`
- INTERVAL: number of seconds to sleep between sensor sweeps

Optional:

- None. (No, no support for MQTT authentication yet.)

## Usage example

Let's say I'm running [mosquitto](https://mosquitto.org/) on 192.168.0.10 on default port 1883, no username/password.

When running the container on a Pi on this subnet, I set environment variables:

- MQTT_BROKER: `192.168.0.10`
- DEVICE_PATH: `/sys/bus/w1/devices/`
- INTERVAL: `60`

Now I `mosquitto_sub -t garden-temps/# -h 192.168.0.10` and every 60 seconds with 5 sensors connected I receive messages like:

    28-01204bcb1a00,2021-03-07T01:39:09,65.5
    28-01204c9fb29c,2021-03-07T01:39:09,65.4
    28-01204c5f8d3c,2021-03-07T01:39:09,65.2
    28-01204c68e858,2021-03-07T01:39:09,64.6
    28-01204cb9c15f,2021-03-07T01:39:09,64.5

This is sensor ID, timestamp, temperature in Fahrenheit.

These could be consumed as-is, or handled and sent to a database, Exceltabase, etc.

## Troubleshooting

If a sensor's not working quite right you'll get 185F (85C, the default value  DS18B20 resets to) or 32F (0C, not sure why that happens.)
