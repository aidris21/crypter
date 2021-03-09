const authService = require("../services/auth.service");
const { jsonError } = require("../shared/errors");

async function loginController(req, res) {
    const { username, password } = req.body;

    if (!username || !password) {
        return jsonError(
            res,
            "'username' and 'password' are required body params.",
            400,
        );
    }

    res.json({
        accessToken: await authService.login(username, password),
    });
}

async function signupController(req, res) {
    const { name, username, password, publicKey } = req.body;

    if (!username || !password || !name || !publicKey) {
        return jsonError(
            res,
            "'username', 'password', 'name', 'publicKey' are required body params.",
            400,
        );
    }

    await authService.signup(name, username, password, publicKey);

    res.status(201).send();
}

module.exports = { loginController, signupController };
