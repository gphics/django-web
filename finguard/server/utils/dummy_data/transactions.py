from faker import Faker
import pandas as pd
import numpy as np
from sender import send_request
from pathlib import Path




fake  = Faker()

total_number = 40

def generate_random_transactions():
    max_list = np.random.randint(3000, 10000, size=50)
    min_list = np.random.randint(500, 2000, size=50)
    # generating fake past random transaction datetimes
    transaction_date = [fake.past_datetime() for i in range(total_number)]

    # generating amounts
    amounts = np.random.randint( np.random.choice(min_list), np.random.choice(max_list), size = total_number)

    # generating category
    category = np.random.randint(1, 13, size=total_number)

    transactions = pd.DataFrame()

    # populating the transactions df
    transactions["amount"] = amounts
    transactions["transaction_date"] = transaction_date
    transactions["category"] = category

    transactions["transaction_date"] = transactions["transaction_date"].astype(str)


    transactions = transactions.to_dict(orient="records")

    return transactions


url = "http://127.0.0.1:8000/transaction/"


def transaction_creation():
    # Authorizations ...
    tokens = []
    base_dir =str(Path(__file__).resolve().parent)
    with open(f"{base_dir}/tokens.txt", "r+") as file:
        tokens = file.read().splitlines()
    
    # tokens = [tokens[0]]
    for token in tokens:
        transactions = generate_random_transactions()
        headers = {"Authorization": f"Token {token}"}
        for transaction in transactions:
            send_request(url, payload=transaction, headers = headers)
