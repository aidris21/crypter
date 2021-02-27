// here we check that all params are correct (logic-wise)

const MessageModel = require("../models/Message.model");
const { ResponseError } = require("../shared/errors");
const usersService = require("./users.service");

// all business logic goes here
class MessagesService {
    constructor(model) {
        this.model = model;
    }

    async list(currentUser, otherUser, startFrom = 0) {
        if (!(await usersService.exists(currentUser))) {
            throw new ResponseError(
                "You are trying to get messages of a user who doesn't exist.",
                400,
            );
        }

        if (!(await usersService.exists(otherUser))) {
            throw new ResponseError(
                "You are trying to get messages from a user who doesn't exist.",
                400,
            );
        }

        return this.model.find({
            ...(startFrom && { createdAt: { $gt: startFrom } }),
            $or: [
                {
                    from: otherUser,
                    to: currentUser,
                },
                {
                    from: currentUser,
                    to: otherUser,
                },
            ],
        });
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

        const message = new this.model({ from, to, text });
        message.save();
    }
}

module.exports = new MessagesService(MessageModel);
