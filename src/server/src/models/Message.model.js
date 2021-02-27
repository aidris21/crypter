const { Schema, model } = require("mongoose");

const MessageSchema = new Schema(
    {
        text: String,
        from: String,
        to: String,
    },
    { timestamps: true },
);

const MessageModel = model("Message", MessageSchema);

module.exports = MessageModel;
