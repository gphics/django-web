from sender import send_request
from pathlib import Path

transaction_categories =  [
    "Housing",            # Rent, mortgage, repairs
    "Transportation",      # Gas, public transit, car maintenance
    "Food & Groceries",    # Supermarkets, farmers markets
    "Dining Out",          # Restaurants, cafes, takeout
    "Utilities",           # Electricity, water, internet, phone
    "Health & Medical",    # Pharmacy, doctors, insurance
    "Entertainment",       # Streaming, movies, concerts
    "Personal Care",       # Haircuts, toiletries, gym
    "Shopping",            # Clothing, electronics, household items
    "Debt Payments",       # Credit card interest, student loans
    "Savings & Investing", # Emergency fund, stocks
    "Gifts & Donations"    # Charity, birthdays
]

url = "http://127.0.0.1:8000/transaction/category"

def category_creation():
    # Authorizations ...
    tokens = []
    base_dir =str(Path(__file__).resolve().parent)
    with open(f"{base_dir}/tokens.txt", "r+") as file:
        tokens = file.read().splitlines()
    headers = {"Authorization": f"Token {tokens[0]}"}
    for category in transaction_categories:
        payload = {"title":category}
        send_request(url, payload, headers)