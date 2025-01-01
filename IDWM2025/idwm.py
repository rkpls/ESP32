import socket
import time
from machine import Pin
from neopixel_custom import NeoPixel
import wifisetup

# NeoPixel Setup
NUM_LEDS = 32  # LED count currently testing
LED_PIN_1 = Pin(2)
LED_PIN_2 = Pin(4)

strip1 = NeoPixel(LED_PIN_1, NUM_LEDS)
strip2 = NeoPixel(LED_PIN_2, NUM_LEDS)

# Web Server
def start_server(ip):
    addr = socket.getaddrinfo(ip, 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Listening on", addr)

    while True:
        cl, addr = s.accept()
        print("Client connected from", addr)
        request = cl.recv(1024).decode("utf-8")
        print("Request:", request)

        # Parse request
        if "/animation1" in request:
            color_wipe(strip1, strip2, (0, 0, 255))  # Blue
        elif "/animation2" in request:
            rainbow_cycle(strip1, strip2)
        elif "/animation3" in request:
            pulse(strip1, strip2, (0, 255, 0))  # Green

        response = generate_html()
        cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
        cl.send(response)
        cl.close()

# Generate HTML for Web Interface
def generate_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP LED Control</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; margin: 0; padding: 20px; }
        h1 { font-size: 2.5em; margin-bottom: 20px; }
        button { font-size: 1.5em; padding: 15px; margin: 10px; width: 200px; background-color: #1f1f1f; color: #ffffff; border: 2px solid #ffffff; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #333333; }
    </style>
</head>
<body>
    <h1>ESP LED Control</h1>
    <button onclick="location.href='/animation1'">Animation 1</button><br>
    <button onclick="location.href='/animation2'">Animation 2</button><br>
    <button onclick="location.href='/animation3'">Animation 3</button><br>
</body>
</html>
"""
    return html

# LED Animations
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

def pulse(strip1, strip2, color=(0, 255, 0), steps=50):
    for i in range(steps):
        brightness = i / steps
        strip1.set_brightness(brightness)
        strip2.set_brightness(brightness)
        strip1.fill(color)
        strip2.fill(color)
        strip1.write()
        strip2.write()
        time.sleep(0.05)
    for i in range(steps, 0, -1):
        brightness = i / steps
        strip1.set_brightness(brightness)
        strip2.set_brightness(brightness)
        strip1.fill(color)
        strip2.fill(color)
        strip1.write()
        strip2.write()
        time.sleep(0.05)

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Main

wlan = wifisetup.getConnection()

if wlan is None:
    print("[WifiMgr] Could not initialize the network connection.")
    while True:
        pass
ip = wlan.ifconfig()[0]
print(f"[WifiMgr] Network initialized. IP Address: {ip}")
start_server(ip)

