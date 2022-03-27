import datetime, uuid, json, os
from worker.sensor import sensor
from pytz import timezone 
from worker.GENERIC_MQTT import Generic_Mqtt
#from azure.iot.device import IoTHubModuleClient,Message
import time
# deviceID = "87898ce2-3cce-4758-a645-f37d495615af" #E1 edge
# deviceID = "cc978ac6-f78f-404c-82da-dac01393f59c" #E2 edge
# id = os.getenv("IOTEDGE_DEVICEID")
mqtt = Generic_Mqtt()
sensor_data = sensor()
#module_client = IoTHubModuleClient.create_from_edge_environment()
#module_client.connect()
while True:
    t_data = sensor_data.get_data()
    #print(t_data)
    if t_data[0] == "null":
        print("Resetting the counter")
    else:
        #msg = Message(json.dumps(t_data[0]))                           
        #msg.message_id = uuid.uuid4()                   # Add a custom message property               
        #module_client.send_message_to_output(msg,t_data[1])           # Send the message.
        mqtt.MQTT_Send_Data(t_data[0])
        print("Message sent: {}".format(t_data[0]))
        time.sleep(5)
    