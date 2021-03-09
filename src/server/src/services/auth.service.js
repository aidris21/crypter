const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt");

const { ResponseError } = require("../shared/errors");
const UserModel = require("../models/User.model");

const VERY_PRIVATE_KEY = "321blah";

class AuthService {
    constructor(model) {
        this.model = model;
    }

    async login(username, password) {
        const user = await this.model.where({ username }).findOne();

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

    async signup(name, username, password, publicKey) {
        if (await this.model.where({ username }, {}).findOne()) {
            throw new ResponseError("User name is taken", 400);
        }

        const user = new this.model({
            password: await bcrypt.hash(password, 5),
            name,
            username,
            publicKey,
        });

        await user.save();
    }

    validate(token) {
        try {
            return Promise.resolve(jwt.verify(token, VERY_PRIVATE_KEY));
        } catch (e) {
            throw new ResponseError("Invalid access token.", 401);
        }
    }
}

module.exports = new AuthService(UserModel);
