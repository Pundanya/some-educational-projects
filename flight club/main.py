from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from notification_manager import NotificationManager
import requests

SHEETY_USERS_ENDPOINT = "https://api.sheety.co/74fb0a658b282c2eb356888c03db8bb7/flightDeals/users"
sheet_header = {
    "Authorization": "Bearer yourtoken"
}

ORIGIN_CITY_IATA = "LON"

data_manager = DataManager()
data_manager.get_destination_data()
data_manager.update_destination_codes()
sheet_data = data_manager.destination_data

flight_search = FlightSearch()

notification_manager = NotificationManager()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

r = requests.get(url=SHEETY_USERS_ENDPOINT, headers=sheet_header)
users = r.json()["users"]

for dst in sheet_data:
    flight = flight_search.search(
        ORIGIN_CITY_IATA,
        dst["iataCode"],
        tomorrow,
        six_month_from_today
    )

    if flight is None:
        continue

    if flight.price <= dst["lowestPrice"]:
        for user in users:
            msg = f"Subject: {user['firstName']} {user['lastName']}, дешёвый авиабилет!\n\n Рейс всего за £{flight.price}: ИЗ {flight.origin_city}–{flight.origin_airport} В {flight.destination_city}–{flight.destination_airport}. С {flight.out_date} по {flight.return_date}.".encode(
                            "utf8")
            if flight.stop_overs > 0:
                msg += f"\nПолет имеет {flight.stop_overs} пересадку, через {flight.via_city}."

            notification_manager.send_mail(user["email"], msg)















# headers = {
#     "x-app-id": APP_ID,
#     "x-app-key": API_KEY,
#     "Authorization": "Bearer asdasd1d1d12d2dasrw4atb4a3ayb435g$#@!%QV#%#!@VR#@bf"
# }




######

# today_date = datetime.now().strftime("%d/%m/%Y")
# now_time = datetime.now().strftime("%X")


# sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

# print(sheet_response.text)