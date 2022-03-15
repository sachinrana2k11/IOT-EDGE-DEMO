import sys
import json
import time

import paho.mqtt.client as mqtt
from termcolor import colored
from SaveData import savedata
from queue import Queue
class Generic_Mqtt():
    def __init__(self):
        with open("CONFIG/config.json", "r") as jsonfile:
            self.data = json.load(jsonfile)
            print("Config Read successfully MQTT")
        self.MQTT_client = mqtt.Client()
        self.q = Queue()
        self.savedata = savedata()
        self.MQTT_Connect()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(self.data["TOPIC_SUB"])
        print("Subscribe topic mqtt")


    def on_message(self, client, userdata, msg):
        in_data = json.loads(msg.payload.decode("utf-8"))
        print(colored("GOT DATA" + str(in_data), "blue"))
        self.q.put(in_data)



    def MQTT_Connect(self):
        try:
            temp = self.data["USR"]
            print(temp)
            self.MQTT_client.username_pw_set(self.data["USR"], self.data["PWD"])
            self.MQTT_client.on_connect = self.on_connect
            self.MQTT_client.on_message = self.on_message
            self.MQTT_client.connect(self.data["URL"], self.data["PORT"])
            self.MQTT_client.loop_start()
            print(colored("SUCCESSFULLY CONNECTED TO MQTT BROKER", "green"))
        except:
            e = sys.exc_info()[0]
            print(colored("FAILED TO CONNECT MQTT SERVER CHECK CONNECTION - " + str(e), "red"))
            pass

    def MQTT_Send_Data(self, payload):
        try:
            self.MQTT_client.publish(topic=self.data["TOPIC_PUB"], payload=payload, qos=self.data["QOS"])
            print(colored("PUBLISHING  DATA TO MQTT-:" + str(payload), "green"))
            return True
        except:
            e = sys.exc_info()[0]
            print(colored("EXCEPTION IN SENDING DATA BY GENERIC MQTT - " + str(e), "red"))
            pass

    def send_azure_tables(self):
        #print(self.q.empty())
        if self.q.empty():
            print(colored("WAITING FOR DATA FROM EDGE GATEWAYS-: ", "blue"))
            time.sleep(2)
        if not self.q.empty():
            incomming_data = self.q.get()
            self.savedata.save_into_table(incomming_data)
