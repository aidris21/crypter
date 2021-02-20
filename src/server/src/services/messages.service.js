// here we check that all params are correct (logic-wise)

const { ResponseError } = require("../shared/errors");
const usersService = require("./users.service");

// all business logic goes here
class MessagesService {
    constructor() {
        this._storage = [
            {
                _id: 1,
                text: "Hello, I am Olha!",
                from: "1",
                to: "2",
                sentAt: 1613859989227,
            },
            {
                _id: 2,
                text: "Hello, I am Amir!",
                from: "2",
                to: "1",
                sentAt: 1613859989300,
            },
        ];
    }

    async list(currentUser, from, startFrom = 0) {
        if (!(await usersService.exists(currentUser))) {
            throw new ResponseError(
                "You are trying to get messages of a user who doesn't exist.",
                400,
            );
        }

        if (!(await usersService.exists(from))) {
            throw new ResponseError(
                "You are trying to get messages from a user who doesn't exist.",
                400,
            );
        }

        console.log(this._storage);

        return this._storage.filter(
            (message) =>
                message.sentAt > startFrom &&
                ((message.from === from && message.to === currentUser) ||
                    (message.from === currentUser && message.to === from)),
        );
    }

    async send(from, to, text) {
        if (!text) {
            throw new ResponseError("Can't send an empty message.", 400);
        }

        if (!(await usersService.exists(to))) {
            throw new ResponseError(
                "You are trying to send a message to the user who doesn't exist.",
                400,
            );
        }

        if (!(await usersService.exists(from))) {
            throw new ResponseError(
                "You are trying to send a message from the user who doesn't exist.",
                400,
            );
        }

        this._storage.push({
            from,
            to,
            text,
            sentAt: Date.now(),
            _id: this._storage.length + 1,
        });
    }
}

module.exports = new MessagesService();
