from azure.data.tables import TableServiceClient
import logging,sys
from termcolor import colored
import uuid
class savedata:
    def __init__(self):
        self.conn_str = "DefaultEndpointsProtocol=https;AccountName=storageaccountnewte97ef;AccountKey=PVbM+xvgMTpCMA0jipqBo7iKZunv1uPs5utcRohnDCqPGkbcLlwbwHjv9CBdJHEmjVYLi/A+KTkVveQc2dZecA==;EndpointSuffix=core.windows.net"
        self.table_service_client = TableServiceClient.from_connection_string(conn_str=self.conn_str)
        self.appid = u"AzurePoc"
        self.productname = u"HomeAutomation"
        # self.logger = logging.getLogger('azure')
        # self.logger.setLevel(logging.DEBUG)
        # self.handler = logging.StreamHandler(stream=sys.stdout)
        # self.logger.addHandler(self.handler)


    def save_into_table(self, data):
        final_data = self.make_data(data)
        self.send_data_azure_table(final_data)
        #print(final_data)

    def send_data_azure_table(self,data_to_send):
        try:
            self.table_client = self.table_service_client.get_table_client(table_name=data_to_send[1])
            entity = self.table_client.create_entity(entity=data_to_send[0])
            print(colored("DATA SAVED INTO AZURE TABLES:- " + str(entity),"green"))
        except:
            e = sys.exc_info()[0]
            print(colored("EXCEPTION GOT WHILE SAVING TO AZURE TABLES-:" + str(e),"red"))
            pass


    def make_data(self,data):
        test = {
            u'PartitionKey': self.appid,
            u'RowKey': str(uuid.uuid4()),
            'EdgeId': data["EdgeID"],
            'DeviceId': data["DeviceID"],
            'temperature': data["Data"]["Temperature"],
            'humidity': data["Data"]["Humidity"],
            'timestamp': data["timestamp"]
        }
        if data["EdgeID"] == "1891832b-cbca-43ba-9c6b-192660b316a6":
            return [test,"EDGE1"]
        if data["EdgeID"] == "9c2f0f03-5778-4d6b-a6e9-42fa473752e4":
            return [test,"EDGE2"]


