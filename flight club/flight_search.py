import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_API_KEY = "yourtoken"



class FlightSearch:
    def get_code(self, city):
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city, "location_types": "city"}
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        r = requests.get(url=location_endpoint, headers=headers, params=query)
        results = r.json()["locations"]
        code = results[0]["code"]
        return code

    def search(self, from_iata, to_iata, from_time, to_time):
        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {"apikey": TEQUILA_API_KEY}
        search_params = {
            "fly_from": from_iata,
            "fly_to": to_iata,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": "7",
            "nights_in_dst_to": "28",
            "flight_type": "round",
            "one_for_city": "1",
            "max_stopovers": 0,
            "curr": "GBP"
        }

        r = requests.get(
            url=search_endpoint,
            headers=headers,
            params=search_params
        )

        try:
            data = r.json()["data"][0]
        except IndexError:
            try:
                search_params["max_stopovers"] = 1
                r = requests.get(
                    url=search_endpoint,
                    headers=headers,
                    params=search_params
                )
                data = r.json()["data"][0]
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
            except IndexError:
                print(f"No flights found for {to_iata}.")
                return None
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]['cityFrom'],
                origin_airport=data["route"][0]['flyFrom'],
                destination_city=data["route"][0]['cityTo'],
                destination_airport=data["route"][0]['flyTo'],
                out_date=data["route"][0]['local_departure'].split("T")[0],
                return_date=data["route"][1]['local_departure'].split("T")[0],
            )
            return flight_data