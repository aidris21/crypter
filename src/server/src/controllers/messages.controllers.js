// Here we interpret the request
const messagesService = require("../services/messages.service");
const { jsonError } = require("../shared/errors");

async function listMessages(req, res) {
    if (!req.query.currUser) {
        return jsonError(res, "'currUser' is a required query param", 400);
    }

    if (!req.query.from) {
        return jsonError(res, "'from' is a required query param", 400);
    }

    const startFrom = Number(req.query.startFrom);

    if (req.query.startFrom && isNaN(startFrom)) {
        return jsonError(res, "'startFrom' must be of type int", 400);
    }

    res.json({
        messages: await messagesService.list(
            req.query.currUser,
            req.query.from,
            startFrom || undefined,
        ),
    });
}

async function sendMessage(req, res) {
    const { message: incomingMessage } = req.body;

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

    if (!req.query.from) {
        return jsonError(res, "'from' is a required query param.", 400);
    }

    await messagesService.send(
        req.query.from,
        incomingMessage.to,
        incomingMessage.text,
    );

    res.json({
        status: "Success!",
    });
}

module.exports = { listMessages, sendMessage };
