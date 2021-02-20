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

-   `currUser` - **optional** query param, id of a user to filter out.

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

-   `currUser` - **required** query param, id of a current user
-   `otherUser` - **required** query param, id of another user
-   `startFrom` - **optional** query param, timestamp in milliseconds of the last message that client has. Filters out messages with `sentAt` older than that

Examples:

-   GET: http://localhost:3000/messages?currUser=1&otherUser=2
-   GET: http://localhost:3000/messages?currUser=1&otherUser=2&startFrom=1613859989227

<hr>

### Send Message

**POST http://localhost:3000/messages** - Sends a message

**Params:**

-   `currUser` - **required** query param, id of a current user
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
