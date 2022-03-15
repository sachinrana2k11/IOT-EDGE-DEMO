import json, time,sys
from azure.eventhub import EventHubConsumerClient
from SaveData import savedata
import threading
CONNECTION_STR = "Endpoint=sb://ihsuprodpnres008dednamespace.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=qd8yo8ga8p6xIPX67Y6CxprBWiJ8URtt5Q28qPvebm8=;EntityPath=iothub-ehub-ideaxa-iot-16068338-c9744dbf0e"#os.environ["EVENT_HUB_CONN_STR"]
EVENTHUB_NAME = "iothub-ehub-ideaxa-iot-16068338-c9744dbf0e"
savedata = savedata()

def on_event(partition_context, event):
    print("Received the data from iothub: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'),partition_context.partition_id))
    #print(json.loads(event.body_as_str(encoding='UTF-8')))
    savedata.save_into_table(json.loads(event.body_as_str(encoding='UTF-8')))

def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))

def get_data(num):
    consumer_client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group='$Default',
        eventhub_name=EVENTHUB_NAME,
    )

    try:
        with consumer_client:
            consumer_client.receive(
                on_event=on_event,
                on_partition_initialize=on_partition_initialize,
                on_partition_close=on_partition_close,
                on_error=on_error,
                starting_position="@latest",  # "-1" is from the beginning of the partition.
            )
    except KeyboardInterrupt:
        print('Stopped receiving.')


def save_azure(num):
    while 1:
        try:
            savedata.send_data_azure_table()
            #print("data sender thred open")
            time.sleep(1)
        except:
            e = sys.exc_info()[0]
            print("exception got..-:" + str(e))
            continue

if __name__ == '__main__':
    t1 = threading.Thread(target=get_data, args=(10,))
    t2 = threading.Thread(target=save_azure, args=(10,))
    t1.start()
    t2.start()
