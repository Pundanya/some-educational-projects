import requests
import os
from datetime import datetime

GENDER = "male"
WEIGHT_KG = "71"
HEIGHT_CM = "180"
AGE = "23"

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = "https://api.sheety.co/74fb0a658b282c2eb356888c03db8bb7/myWorkouts/workouts"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Authorization": os.environ.get("Authorization")
}

exercise_params = {
    "query": exercise_text,
    "gender": "male",
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

r = requests.post(url=exercise_endpoint, json=exercise_params, headers=headers)
result = r.json()

######

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

    print(sheet_response.text)
