import numpy as np
from sender import send_request
from pathlib import Path

country = "Nigeria"

states = [
    "Oyo",
    "Ogun",
    "Osun",
    "Kaduna",
    "Kano",
    "Ekiti"
]

random_states = [np.random.choice(states) for _ in [*states, *states]]

cities = [
    "Ibadan",
    "Ogbomosho",
    "Kaduna",
    "Zaria",
    "Kano",
    "Wudil",
    "Ado-Ekiti",
    "Ikere-Ekiti"
]

random_cities = [np.random.choice(cities) for _ in [*cities, *cities]]
# A list of 10 common ISO 4217 currency codes
currencies = ["NGN", "USD", "EUR", "GBP", "JPY", "CNY", "CAD", "AUD", "CHF", "INR"]


def update_profile():

    base_path = str(Path(__file__).resolve().parent)

    with open(f"{base_path}/tokens.txt", "r") as file:
        tokens = file.read().splitlines()

        for token in tokens:
            headers = {"Authorization": f"Token {token}"}

            payload = {
                "profile":{
                "state":str(np.random.choice(random_states)),
                "country":country,
                "city":str(np.random.choice(random_cities)),
                "currency":str(np.random.choice(currencies))
            }}
           
            url = "http://127.0.0.1:8000/profile"
            send_request(url, payload, headers, "put")


    