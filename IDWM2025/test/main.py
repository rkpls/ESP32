import json
from umqtt.simple import MQTTClient
import wifisetup

# Get network connection
wlan = wifisetup.getConnection()
broker_ip = wlan.ifconfig()[0]

# MQTT configuration
broker_port = 1883
topic = "binary/trigger"

def on_message(topic, msg):
    try:
        message = json.loads(msg)
        if 'trigger' in message and message['trigger'] == 1:
            print("Binary trigger received!")
        else:
            print("Message received but not recognized:", msg)
    except Exception as e:
        print("Error processing message:", e)

def main():
    print("Connecting to MQTT broker at", broker_ip)
    client = MQTTClient("esp32_client", broker_ip, port=broker_port)
    client.set_callback(on_message)
    
    try:
        client.connect()
        print("Connected to MQTT broker")
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    except Exception as e:
        print("Connection failed:", e)
        return

    while True:
        try:
            client.wait_msg()  # Wait for incoming messages
        except KeyboardInterrupt:
            print("Exiting...")
            client.disconnect()
            break
        except Exception as e:
            print("Error during wait_msg:", e)

if __name__ == "__main__":
    main()

