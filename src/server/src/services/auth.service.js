const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");

const { ResponseError } = require("../shared/errors");

const VERY_PRIVATE_KEY = "321blah";

class AuthService {
    constructor() {
        this._storage = {
            olha: {
                _id: "1",
                username: "olha",
                password:
                    "$2b$05$oGr2FohljfSoOgQzKaFxh.LQt1QRsBrXCvY8l1C5bzjjAmMhWTwgC", // hello
            },
            amir: {
                _id: "2",
                username: "amir",
                password:
                    "$2b$05$.VLWSDL6tKLqFHeVcSQE5OfuctxsDakIMYsH7nUGqf4wVpY5fbBga", // columbia
            },
        };
    }

    async login(username, password) {
        const user = this._storage[username];

        if (
            !(await bcrypt.compare(
                password,
                user ? user.password : "gdfjhsgfjh",
            ))
        ) {
            throw new ResponseError("Invalid username or password.", 401);
        }

        return Promise.resolve(
            jwt.sign({ username, _id: user._id }, VERY_PRIVATE_KEY),
        );
    }

    validate(token) {
        try {
            return Promise.resolve(jwt.verify(token, VERY_PRIVATE_KEY));
        } catch (e) {
            throw new ResponseError("Invalid access token.", 401);
        }
    }
}

module.exports = new AuthService();
