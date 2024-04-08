from OTA_Wrapper import OTA_Wrapper
from wifi_config import SSID, PASSWORD
from time import sleep
from Display import Display
from sr04t import Srt04t
from lora import LoRa
from umqtt.simple import MQTTClient
import network
import machine
import time


BROKER="18.185.170.141"
REPOSITORY = "https://github.com/ingcoty/pool_monitor.git"

level_sensor = Srt04t(triger_pin=25, echo_pin=4)
display = Display()
lora = LoRa()

display.text(f"Iniciando...", 0)


def process(msg):
    level_tank = int(msg)
    display.text(f"Tank Level: {msg}%", 0)
    pool_level = level_sensor.read_distance()
    display.text(f"Pool Level: {pool_level}%", 1)   
    if level_tank <= 75 and pool_level > 10:
        display.text(f"Bomba: ON", 2) 
    if level_tank >= 100 or pool_level < 10:
        display.text(f"Bomba: OFF", 2) 
        
  
def connect_wifi():
    """ Connect to Wi-Fi."""

    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    while not sta_if.isconnected():
        print('.', end="")
        sleep(0.25)
    display.text('Connected to WiFi', 0)
    display.text(f'IP:{sta_if.ifconfig()[0]}', 1)


def process_message(topic, msg):
    print("actualizando firmware")
    ota = OTA_Wrapper(github_url=REPOSITORY)

connect_wifi()

#process_message("","")

client_id = "ESP32_TankMonitor"
mqtt_client = MQTTClient(client_id, BROKER)
mqtt_client.set_callback(process_message)
mqtt_client.connect()
mqtt_client.subscribe("mqtt-github-action/pool_monitor")

lora.set_callback(process)
lora.wait_msg()

while True:
    mqtt_client.check_msg()   
    sleep(2)



