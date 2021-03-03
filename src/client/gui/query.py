import requests as rq
import json


def login(username, password):
    endpoint = "http://localhost:3000/login"
    headers = {'Content-type': 'application/json'}
    data = {
        "username": username,
        "password": password
    }

    r = rq.post(url = endpoint, data=json.dumps(data), headers=headers)

    post_return = r.json()

    token = post_return["accessToken"]

    return token

def post_message(message, token, user_to = "6039a891cfcf715977b2365c"):
    endpoint = "http://localhost:3000/messages"
    headers = {'Content-type': 'application/json'}
    data = {
        "message": {
            "to": user_to,
            "text": message
        }
    }
    param = {
        "accessToken": token
    }
    r = rq.post(url = endpoint, data=json.dumps(data), headers = headers, params=param)
    post_return = r.json()

    return post_return["status"]

def get_contacts():
    API_ENDPOINT = "http://localhost:3000/users"

    r = rq.get(API_ENDPOINT)

    get_return = r.json()

    return get_return["users"]



"""----------------------------------------"""

def get_users():
    API_ENDPOINT = "http://localhost:3000/users"

    r = rq.get(API_ENDPOINT)

    foo = r.json()

    return foo

def login_amir():
    endpoint = "http://localhost:3000/login"
    headers = {'Content-type': 'application/json'}
    data = {
        "username": "amir",
        "password": "columbia"
    }

    r = rq.post(url = endpoint, data=json.dumps(data), headers=headers)

    foo = r.json()

    return foo


if __name__ == "__main__":
    #post_message(message = "Hello Hello")

    """token = login_amir()["accessToken"]
    print(token)

    message_send = post_message("hey there", token)
    print(message_send)

    endpoint = "http://localhost:3000/messages"
    data = {
        "accessToken": token,
        "otherUser": "6039a891cfcf715977b2365c"
    }
    r = rq.get(endpoint, params=data)
    foo = r.json()
    print(foo)"""

    print(get_users())


    