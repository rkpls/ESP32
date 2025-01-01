from mqtt_simple import MQTTClient
import time
import json
from machine import Pin
from neopixel_custom import NeoPixel
import wifisetup

# MQTT Setup
CLIENT_ID = "ESP32_LED_Controller"
TOPIC = "esp/control"

# NeoPixel Setup
NUM_LEDS = 32
LED_PIN_1 = Pin(2)
LED_PIN_2 = Pin(4)

strip1 = NeoPixel(LED_PIN_1, NUM_LEDS)
strip2 = NeoPixel(LED_PIN_2, NUM_LEDS)

# Global state
current_animation = "off"
global_brightness = 1.0


def set_brightness(value):
    global global_brightness
    global_brightness = max(0.0, min(float(value), 1.0))  # Clamp between 0 and 1
    strip1.set_brightness(global_brightness)
    strip2.set_brightness(global_brightness)


def turn_off():
    strip1.fill((0, 0, 0))
    strip2.fill((0, 0, 0))
    strip1.write()
    strip2.write()


def animation_handler(animation):
    if animation == "off":
        turn_off()
    elif animation == "color_wipe":
        color_wipe(strip1, strip2, (0, 0, 255))
    elif animation == "rainbow_cycle":
        rainbow_cycle(strip1, strip2)
    elif animation == "fps_test":
        fps_test(strip1, strip2)
    else:
        print(f"Unknown animation: {animation}")


def message_callback(topic, msg):
    global current_animation

    try:
        # Parse JSON message
        data = json.loads(msg)
        if "brightness" in data:
            set_brightness(data["brightness"])
        if "animation" in data:
            current_animation = data["animation"]
    except Exception as e:
        print(f"Failed to parse message: {e}")


# Animations
def color_wipe(strip1, strip2, color=(0, 0, 255)):
    for i in range(strip1.n):
        strip1[i] = color
        strip2[i] = color
        strip1.write()
        strip2.write()
        time.sleep(0.05)


def rainbow_cycle(strip1, strip2, wait=20):
    for j in range(256):
        for i in range(strip1.n):
            color = wheel((i * 256 // strip1.n + j) & 255)
            strip1[i] = color
            strip2[i] = color
        strip1.write()
        strip2.write()
        time.sleep_ms(wait)


def fps_test(strip1, strip2):
    color1 = (255, 0, 0)
    color2 = (0, 255, 0)
    start_time = time.ticks_ms()
    frame_count = 0
    while frame_count < 100:
        strip1.fill(color1 if frame_count % 2 == 0 else color2)
        strip2.fill(color1 if frame_count % 2 == 0 else color2)
        strip1.write()
        strip2.write()
        frame_count += 1
    end_time = time.ticks_ms()
    fps = frame_count / ((time.ticks_diff(end_time, start_time)) / 1000)
    print(f"FPS: {fps:.2f}")


def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)


# Main MQTT Loop
def mqtt_loop(broker_ip):
    client = MQTTClient(CLIENT_ID, broker_ip)
    client.set_callback(message_callback)
    client.connect()
    client.subscribe(TOPIC)
    print(f"Connected to MQTT broker at {broker_ip}, subscribed to {TOPIC}")

    while True:
        client.check_msg()  # Check for new messages
        animation_handler(current_animation)  # Handle current animation


# Wi-Fi Connection
def main():
    wlan = wifisetup.getConnection()  # Use your existing Wi-Fi setup
    if wlan is None:
        print("[WifiMgr] Could not initialize the network connection.")
        while True:
            pass

    broker_ip = wlan.ifconfig()[0]
    print(f"[WifiMgr] Connected to Wi-Fi. IP Address: {broker_ip}")

    # Start MQTT loop
    try:
        mqtt_loop(broker_ip)
    except KeyboardInterrupt:
        print("Exiting...")


# Run the main function
if __name__ == "__main__":
    main()

