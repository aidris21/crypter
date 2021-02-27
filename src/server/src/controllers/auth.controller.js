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

module.exports = { loginController };
