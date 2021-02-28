import requests as rq

API_ENDPOINT = "http://localhost:3000/users"

r = rq.get(API_ENDPOINT)

foo = r.json()


def post_message(message, user_from = "6039a7c8cfcf715977b2365a", user_to = "6039a891cfcf715977b2365c"):
    endpoint = "http://localhost:3000/messages?currUser=6039a7c8cfcf715977b2365a?accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFtaXIiLCJfaWQiOiI2MDM5YTg5MWNmY2Y3MTU5NzdiMjM2NWMiLCJpYXQiOjE2MTQzOTI4NDF9._jut8uuDV9MWV4rGzBJnXSDmmFarE92P_P4gGVW7Eq8"
    data = {
        "message": {
            "to": "6039a891cfcf715977b2365c",
            "text": message
        }
    }
    rq.post(url = endpoint, data=data)


if __name__ == "__main__":
    post_message(message = "Hello Hello")

    endpoint = "http://localhost:3000/messages"
    r = rq.get(endpoint)
    foo = r.json()
    print(foo)


    