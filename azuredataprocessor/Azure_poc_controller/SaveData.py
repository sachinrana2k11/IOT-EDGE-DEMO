from azure.data.tables import TableServiceClient
import logging,sys
import uuid
from queue import Queue
class savedata:
    def __init__(self):
        self.q = Queue()
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
        #print(final_data)
        self.q.put(final_data)



    def send_data_azure_table(self):
        #print("getting data from q:- ")
        print(self.q.empty())
        if not self.q.empty():
            #print(self.q.get())
            data_to_send = self.q.get()
            self.table_client = self.table_service_client.get_table_client(table_name=data_to_send[1])
            entity = self.table_client.create_entity(entity=data_to_send[0])
            print("data saved to table azure:- " + str(entity))


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


# my_entity = {
#     u'PartitionKey': APPLICATIONID,
#     u'RowKey': PRODUCT_NAME,
#     u'Stock': 15,
#     u'Price': 9.99,
#     u'Comments': u"great product",
#     u'OnSale': True,
#     u'ReducedPrice': 7.99,
#     u'PurchaseDate': datetime(1973, 10, 4),
#     u'BinaryRepresentation': b'product_name'
# }
