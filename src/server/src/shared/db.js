const mongoose = require("mongoose");

const DB_PASS = "";
const DB_USER = "";

mongoose.connect(
    `mongodb+srv://${DB_USER}:${DB_PASS}@main.epni3.mongodb.net/crypter?retryWrites=true&w=majority`,
    {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useFindAndModify: false,
        useCreateIndex: true,
    },
);
