class ResponseError extends Error {
    constructor(message, code) {
        super(message);
        this.code = code;
    }
}

function jsonError(res, reason, code) {
    return res.status(code).json({ code, reason });
}

module.exports = { ResponseError, jsonError };
