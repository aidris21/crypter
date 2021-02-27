const UserModel = require("../models/User.model");

class UsersService {
    constructor(model) {
        this.model = model;
        this.defProjection = { name: true, publicKey: true };
    }

    list(exclude) {
        // if exclude is provided use { _id: { $not: exclude } } select statement.
        // else {}
        return this.model.find(
            { ...(exclude && { _id: { $ne: exclude } }) },
            this.defProjection,
        );
    }

    async get(id, throwOnMissing = false) {
        const user = await this.model.findById(id, this.defProjection);

        if (throwOnMissing && !user) {
            return Promise.reject("User not found.");
        }

        return user;
    }

    async exists(id) {
        return !!(await this.model.findById(id, {}));
    }
}

module.exports = new UsersService(UserModel);
