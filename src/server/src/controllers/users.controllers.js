const usersService = require("../services/users.service");
const { jsonError } = require("../shared/errors");

async function listUsersController(req, res) {
    const { currUser } = req.query;

    res.json({
        users: await usersService.list(currUser),
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
