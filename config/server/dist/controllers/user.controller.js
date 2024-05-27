"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteUserById = exports.updateUserById = exports.getUserByID = exports.getUserByEmail = exports.getAllUsers = exports.createUser = void 0;
const crypto_1 = __importDefault(require("crypto"));
const db_server_1 = require("../utils/db.server");
const excludehelper = require('../utils/helperfunctions.js');
const createUser = async (req, res) => {
    let salt = crypto_1.default.randomBytes(16).toString('base64');
    let hash = crypto_1.default.createHmac('sha512', salt).update(req.body.password).digest("base64");
    req.body.password = salt + "$" + hash;
    req.body.permissionLevel = 257;
    const { firstName, lastName, emailAddress, password, permissionLevel } = req.body;
    const foundUser = await db_server_1.db.registeredUsers.findMany({
        where: {
            emailAddress: emailAddress
        },
    });
    if (Object.keys(foundUser).length === 0) {
        // user bestaat nog niet, aanmaken.
        const newUser = await db_server_1.db.registeredUsers.create({
            data: req.body
        })
            .catch((error) => {
            console.error(error);
            return res.status(500).json(error.message);
        });
        const newUserWithoutPassword = excludehelper.exclude(newUser, ['password']);
        return res.status(201).json(newUserWithoutPassword);
    }
    else {
        return res.status(400).json('email address al aanwezig in database');
    }
};
exports.createUser = createUser;
const getAllUsers = async (req, res) => {
    try {
        const allUsers = await db_server_1.db.registeredUsers.findMany();
        return res.status(200).json(allUsers);
    }
    catch (error) {
        return res.status(500).json(error.message);
    }
};
exports.getAllUsers = getAllUsers;
const getUserByEmail = async (req, res) => {
    try {
        const foundUser = await db_server_1.db.registeredUsers.findMany({
            where: {
                emailAddress: req.params.emailAddress
            },
        });
        const newUserWithoutPassword = excludehelper.exclude(foundUser, ['password']);
        return res.status(200).json(newUserWithoutPassword);
    }
    catch (error) {
        return res.status(500).json(error.message);
    }
};
exports.getUserByEmail = getUserByEmail;
const getUserByID = async (req, res) => {
    try {
        const userId = parseInt(req.params.userId);
        console.log('User ID: ' + userId);
        const foundUser = await db_server_1.db.registeredUsers.findMany({
            where: {
                id: userId
            },
        });
        const newUserWithoutPassword = excludehelper.exclude(foundUser, ['password']);
        return res.status(200).json(newUserWithoutPassword);
    }
    catch (error) {
        return res.status(500).json(error.message);
    }
};
exports.getUserByID = getUserByID;
const updateUserById = async (req, res) => {
    let salt = crypto_1.default.randomBytes(16).toString('base64');
    let hash = crypto_1.default.createHmac('sha512', salt).update(req.body.password).digest("base64");
    req.body.password = salt + "$" + hash;
    const userId = parseInt(req.params.userId);
    try {
        const updatedUser = await db_server_1.db.registeredUsers.update({
            where: {
                id: userId,
            },
            data: req.body
        });
        const newUserWithoutPassword = excludehelper.exclude(updatedUser, ['password']);
        return res.status(200).json(newUserWithoutPassword);
    }
    catch (error) {
        return res.status(500).json(error.message);
    }
};
exports.updateUserById = updateUserById;
const deleteUserById = async (req, res) => {
    const userId = parseInt(req.params.userId);
    try {
        await db_server_1.db.registeredUsers.delete({
            where: {
                id: userId,
            },
        });
        return res.status(200).json('user deleted');
    }
    catch (error) {
        return res.status(500).json(error.message);
    }
};
exports.deleteUserById = deleteUserById;
//# sourceMappingURL=user.controller.js.map