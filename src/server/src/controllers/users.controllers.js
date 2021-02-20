const { usersService } = require("../services/users.service");
const { jsonError } = require("../shared/errors");

async function listUsersController(req, res) {
    const { currUserId } = req.query;

    res.json({
        users: await usersService.list(currUserId),
    });
}

async function getUserController(req, res) {
    const user = await usersService.get(req.params.id);

    if (!user) {
        return jsonError(res, 404, " User not found.");
    }

    res.json({ user });
}

module.exports = { listUsersController, getUserController };
