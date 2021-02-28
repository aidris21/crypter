const mongoose = require("mongoose");

const DB_PASS = "-k43VcE!-rgPJED";
const DB_USER = "amir";

mongoose.connect(
    `mongodb+srv://${DB_USER}:${DB_PASS}@main.epni3.mongodb.net/crypter?retryWrites=true&w=majority`,
    {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        useFindAndModify: false,
        useCreateIndex: true,
    },
);
