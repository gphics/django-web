import requests



def send_request(url, payload, headers={}, method="post"):
    
    try:
        response = requests.request(method, url, json=payload, headers=headers)
        print(response)
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                print("Data sent successfully")
            else:
                print(result)
        return result
    except Exception as e:
        raise e