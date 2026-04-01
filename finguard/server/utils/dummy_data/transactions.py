from faker import Faker
import pandas as pd
import numpy as np
from sender import send_request
from pathlib import Path



base_dir =str(Path(__file__).resolve().parent)
fake  = Faker()

total_number = 40

def generate_random_transactions(file_path: str |None =None) -> list | None:
    """
    This function generate random transactions and export it as a list unless file_path is provided which would make this function generate a csv file for the transactions.

    """
    max_list = np.random.randint(3000, 10000, size=50)
    min_list = np.random.randint(500, 2000, size=50)
    # generating fake past random transaction datetimes
    transaction_date = [fake.past_datetime() for i in range(total_number)]

    # generating amounts
    amounts = np.random.randint( np.random.choice(min_list), np.random.choice(max_list), size = total_number)

    # generating category
    category = np.random.randint(1, 13, size=total_number)

    transaction_types = ["DEBIT", "CREDIT"]

    transactions = pd.DataFrame()

    # populating the transactions df
    transactions["amount"] = amounts
    transactions["transaction_date"] = transaction_date
    transactions["category"] = category
    transactions["transaction_type"] = np.random.choice(transaction_types, size=total_number)

    transactions["transaction_date"] = transactions["transaction_date"].astype(str)

    if file_path:
        transactions.to_csv(file_path, index=False)
        return

    transactions = transactions.to_dict(orient="records")

    return transactions


url = "http://127.0.0.1:8000/transaction/"


def transaction_creation():
    # Authorizations ...
    tokens = []
    
    with open(f"{base_dir}/tokens.txt", "r+") as file:
        tokens = file.read().splitlines()
    
    # tokens = [tokens[0]]
    for token in tokens:
        transactions = generate_random_transactions()
        headers = {"Authorization": f"Token {token}"}
        for transaction in transactions:
            send_request(url, payload=transaction, headers = headers)



# file_path = f"{base_dir}/dummy_transactions.csv"

# generate_random_transactions(file_path)