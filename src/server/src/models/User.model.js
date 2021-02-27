const { Schema, model } = require("mongoose");

const UserSchema = new Schema({
    name: String,
    username: String,
    password: String,
    publicKey: Number,
});

const UserModel = model("User", UserSchema);

module.exports = UserModel;
