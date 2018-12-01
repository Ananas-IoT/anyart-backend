import json
from pprint import pprint
import requests

url = 'https://opendata.city-adm.lviv.ua/api/3/action/datastore_search'


class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


def getListRecords():
    parameters = {"resource_id": "d8dfe789-167d-4074-be39-d661c666e08d",
                  "fields": {'_id', 'adress_street', 'adress_building', 'adress_notes'}, \
                  #"filters": '{"adress_building": "1.0"}',
                  "limit": 5,  # set amount of result records
                  'records_format': 'lists'  # can be objects, lists, csv and tsv
                  }
    headers = {'Content-Type': 'application/json'}

    response = requests.get(url, params=parameters, headers=headers)
    print(response.status_code)
    if response.status_code != 200:

        raise APIError(response.status_code)
    else:
        data = json.loads(response.text)
        # json_data = json.JSONEncoder(indent=None,
        #                              separators=(',', ': ')).encode(data)
        # pprint(json_data)
        # print(type(data))
        result = data['result']['records']
        for i in range(0, len(data['result']['records'])):
            print(data['result']['records'][i])

        # print(json.dumps(result, indent=4))
        # print(json.dumps(data, indent=5))

    # print(response.content)

    return result

def check_in_API():
    
if __name__ == '__main__':
    getListRecords()
