# Crypter Server

## Initial Install

```
yarn
```

## How to Run the Server

```
yarn start
```

## Run Server with Autorestart

```
yarn dev
```

## Endpoints

<hr>

### List Users

**GET http://localhost:3000/users** - Returns a list of users.

**Params:**

-   `accessToken` - **optional** query param, retrieved from login endpoint.

Examples:

-   GET: http://localhost:3000/users
-   GET: http://localhost:3000/users?currUser=1

<hr>

### Get User

**GET http://localhost:3000/users/{id}** - Returns a user.

**Params:**

-   `id` - path param, id of a user to filter out.

Responds with 404 if user not found

Examples:

-   GET: http://localhost:3000/users/1

<hr>

### List User's Messages

**GET http://localhost:3000/messages** - Returns a list of messages between two users.

**Params:**

-   `accessToken` - **required** query param, retrieved from login endpoint.
-   `otherUser` - **required** query param, id of another user
-   `startFrom` - **optional** query param, timestamp in milliseconds of the last message that client has. Filters out messages with `sentAt` older than that

Examples:

-   GET: http://localhost:3000/messages?currUser=1&otherUser=2
-   GET: http://localhost:3000/messages?currUser=1&otherUser=2&startFrom=1613859989227

<hr>

### Send Message

**POST http://localhost:3000/messages** - Sends a message

**Params:**

-   `accessToken` - **required** query param, retrieved from login endpoint.
-   `message` - **required** body param, message object JSON
-   `message.to` - **required** body param, id of a user to send a message to
-   `message.text` - **required** body param, text of a message

Examples:

-   POST: http://localhost:3000/messages?currUser=1

```json
{
    "message": {
        "to": "2",
        "text": "Hello, I am Olha"
    }
}
```

<hr>

### Login

**POST http://localhost:3000/login** - login

**Params:**

-   `password` - **required** body param
-   `username` - **required** body param

Examples:

-   POST: http://localhost:3000/login

```json
{
    "password": "helloworld",
    "username": "olha"
}
```

<hr>

### Signup

**POST http://localhost:3000/signup** - signup

**Params:**

-   `password` - **required** body param
-   `username` - **required** body param
-   `name` - **required** body param
-   `publicKey` - **required** body param

Examples:

-   POST: http://localhost:3000/signup

```json
{
    "password": "helloworld",
    "username": "olha",
    "name": "Olha",
    "publicKey": [11, 23]
}
```

**Note:** Response status _201_ when user was successfully created.
