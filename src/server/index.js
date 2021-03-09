// converts all async errors to sync so we can handle them
require("express-async-errors");

const bodyParser = require("body-parser");
const express = require("express");
require("./src/shared/db");

const {
    listUsersController,
    getUserController,
} = require("./src/controllers/users.controllers");
const {
    sendMessage,
    listMessages,
} = require("./src/controllers/messages.controllers");
const { ResponseError, jsonError } = require("./src/shared/errors");
const {
    loginController,
    signupController,
} = require("./src/controllers/auth.controller");

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.get("/", (_, res) => res.send("Welcome to Crypter!"));

app.get("/users", listUsersController);
app.get("/users/:id", getUserController);

app.get("/messages", listMessages);
app.post("/messages", sendMessage);

app.post("/login", loginController);
app.post("/signup", signupController);

// eslint-disable-next-line no-unused-vars
app.use((err, _req, res, _next) => {
    if (err instanceof ResponseError) {
        return jsonError(res, err.message, err.code);
    }

    // TODO: some error parsing
    console.log(err);
    jsonError(res, err.message, 500);
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});

// Mongo setup: https://dev.to/sunilksamanta/rest-api-structure-using-nodejs-mongodb-mongoose-2hka
