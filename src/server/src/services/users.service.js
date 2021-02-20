class UsersService {
    constructor() {
        this._storage = {
            1: {
                _id: "1",
                name: "Olha",
                publicKey: 123,
            },
            2: {
                _id: "2",
                name: "Amir",
                publicKey: 321,
            },
        };
    }

    list(exclude) {
        if (exclude) {
            return Promise.resolve(
                Object.values(this._storage).filter(
                    ({ _id }) => _id !== exclude,
                ),
            );
        }

        return Promise.resolve(Object.values(this._storage));
    }

    get(id, throwOnMissing = false) {
        const user = this._storage[id];

        if (throwOnMissing && !user) {
            return Promise.reject("User not found.");
        }

        return Promise.resolve(user || null);
    }

    exists(id) {
        return Promise.resolve(!!this._storage[id]);
    }
}

module.exports = new UsersService();
