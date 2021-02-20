const express = require("express");
const {
    listUsersController,
    getUserController,
} = require("./src/controllers/users");

const app = express();
const port = 3000;

app.get("/", (_, res) => res.send("Welcome to Crypter!"));
app.get("/users", listUsersController);
app.get("/users/:id", getUserController);

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});
