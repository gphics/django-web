from pathlib import Path
from sender import send_request
import os

base_dir =str(Path(__file__).resolve().parent)

url = "http://127.0.0.1:8000/reg"
tokens = []
usernames = [
    "gphics",
    "xenon",
    "juptain",
    "virus",
    "lanres",
    "bidemi",
    "ayinla",
    "olanrewaju",
    "abdulbasit",
    "chief"
]
 
dummy_user = [ ]
for user in usernames:
    dummy_user.append({"username":user, "password":f"12345{user[:3]}"})

def user_creation():
    for user in dummy_user[:1]:
        result = send_request(url, user)
        token = result["data"]["msg"]["token"]

        tokens.append(token + "\n")

    with open(f"{base_dir}/tokens.txt", "a+") as file:
        file.writelines(tokens)
        file.flush()

        os.fsync(file.fileno())


# user_creation()