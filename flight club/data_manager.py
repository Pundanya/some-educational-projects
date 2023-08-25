import requests
from flight_search import FlightSearch

SHEETY_PRICES_ENDPOINT = "https://api.sheety.co/74fb0a658b282c2eb356888c03db8bb7/flightDeals/prices"
sheet_header = {
    "Authorization": "Bearer asdasd1d1d12d2dasrw4atb4a3ayb435g$#@!%QV#%#!@VR#@bf"
}

class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.flight_search = FlightSearch()

    def get_destination_data(self):
        r = requests.get(url=SHEETY_PRICES_ENDPOINT, headers=sheet_header)
        self.destination_data = r.json()["prices"]

    def update_destination_codes(self):
        for price in self.destination_data:
            if price["iataCode"] == "":
                new_data = {
                    "price": {
                        "iataCode": self.flight_search.get_code(price["city"])
                    }
                }
                r = requests.put(
                    url=f"{SHEETY_PRICES_ENDPOINT}/{price['id']}",
                    headers=sheet_header,
                    json=new_data
                )
