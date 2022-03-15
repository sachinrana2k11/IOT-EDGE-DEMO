import time
from GENERIC_MQTT import Generic_Mqtt
mqtt = Generic_Mqtt()

def ping_mqtt():
    while 1:
        mqtt.send_azure_tables()
        #print("Pinging mqtt...")
        #time.sleep(0.2)
ping_mqtt()