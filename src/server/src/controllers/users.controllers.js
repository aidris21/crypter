const authService = require("../services/auth.service");
const usersService = require("../services/users.service");
const { jsonError } = require("../shared/errors");

async function listUsersController(req, res) {
    const token = req.query.accessToken;
    let _id;

    if (token) {
        ({ _id } = await authService.validate(token));
    }

    res.json({
        users: await usersService.list(_id),
    });
}

async function getUserController(req, res) {
    const user = await usersService.get(req.params.id);

    if (!user) {
        return jsonError(res, "User not found.", 404);
    }

    res.json({ user });
}

module.exports = { listUsersController, getUserController };
