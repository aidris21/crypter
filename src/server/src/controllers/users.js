const users = {
    1: {
        _id: 1,
        name: "Olha",
        publicKey: 123,
    },
    2: {
        _id: 2,
        name: "Amir",
        publicKey: 321,
    },
};

function listUsersController(req, res) {
    const { currUserId } = req.query;

    if (currUserId) {
        return res.json({
            users: Object.values(users).filter(
                ({ _id }) => String(_id) !== currUserId,
            ),
        });
    }

    res.json({
        users: Object.values(users),
    });
}

function getUserController(req, res) {
    const user = users[req.params.id];

    if (!user) {
        return res.status(404).json({
            code: 404,
            reason: "User not found.",
        });
    }

    res.json({
        user: users[req.params.id],
    });
}

module.exports = { listUsersController, getUserController };
