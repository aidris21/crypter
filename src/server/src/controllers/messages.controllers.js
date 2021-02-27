// Here we interpret the request
const authService = require("../services/auth.service");
const messagesService = require("../services/messages.service");
const { jsonError } = require("../shared/errors");

async function listMessages(req, res) {
    if (!req.query.accessToken) {
        return jsonError(res, "'accessToken' is a required query param", 400);
    }

    const { _id: currUser } = await authService.validate(req.query.accessToken);

    if (!req.query.otherUser) {
        return jsonError(res, "'otherUser' is a required query param", 400);
    }

    const startFrom = Number(req.query.startFrom);

    if (req.query.startFrom && isNaN(startFrom)) {
        return jsonError(res, "'startFrom' must be of type int", 400);
    }

    res.json({
        messages: await messagesService.list(
            currUser,
            req.query.otherUser,
            startFrom || 0,
        ),
    });
}

async function sendMessage(req, res) {
    const { message: incomingMessage } = req.body;

    if (!req.query.accessToken) {
        return jsonError(res, "'accessToken' is a required query param", 400);
    }

    const { _id: currUser } = await authService.validate(req.query.accessToken);

    if (!incomingMessage) {
        return jsonError(
            res,
            "'message' is a required param in request body.",
            400,
        );
    }

    if (typeof incomingMessage.text !== "string" || !incomingMessage.to) {
        return jsonError(
            res,
            "'text' and/or 'to' are required params in 'message'.",
            400,
        );
    }

    await messagesService.send(
        currUser,
        incomingMessage.to,
        incomingMessage.text,
    );

    res.json({
        status: "Success!",
    });
}

module.exports = { listMessages, sendMessage };
