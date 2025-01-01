import network
import socket
import time
from machine import Pin
from NeoPixel import NeoPixel  # Use your custom NeoPixel class

# Wi-Fi Setup
SSID = "YourHotspotSSID"
PASSWORD = "YourHotspotPassword"

# NeoPixel Setup
NUM_LEDS = 32 #led count currently testing
LED_PIN_1 = Pin(2)
LED_PIN_2 = Pin(4)

strip1 = NeoPixel(LED_PIN_1, NUM_LEDS)
strip2 = NeoPixel(LED_PIN_2, NUM_LEDS)

# Access Point (Fallback)
def create_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid="ESP-LED-Control", authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
    print("Access Point Created: ESP-LED-Control")
    return ap.ifconfig()[0]

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
            run_animation(strip1, strip2, color_wipe)
        elif "/animation2" in request:
            run_animation(strip1, strip2, rainbow_cycle)
        elif "/animation3" in request:
            run_animation(strip1, strip2, pulse)

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
        body { font-family: Arial; text-align: center; margin-top: 50px; }
        button { font-size: 20px; padding: 10px; margin: 10px; }
    </style>
</head>
<body>
    <h1>ESP LED Control</h1>
    <button onclick="location.href='/animation1'">Animation 1</button>
    <button onclick="location.href='/animation2'">Animation 2</button>
    <button onclick="location.href='/animation3'">Animation 3</button>
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

ip = create_access_point()
start_server(ip)
