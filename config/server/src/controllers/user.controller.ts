import crypto from 'crypto';
import type { Request, Response } from "express";
import { db } from "../utils/db.server";
const excludehelper = require('../utils/helperfunctions.ts');
  
export const createUser = async (req: Request, res: Response) => {
    let salt = crypto.randomBytes(16).toString('base64');
    let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
    req.body.password = salt + "$" + hash;
    req.body.permissionLevel = 257;
  
    const { firstName, lastName, emailAddress, password, permissionLevel } = req.body;
    
    const foundUser = await db.registeredUsers.findMany({
        where: {
            emailAddress: emailAddress
        },
    })

    if (Object.keys(foundUser).length === 0) {
        // user bestaat nog niet, aanmaken.
        const newUser = await db.registeredUsers.create({
            data: req.body
        })
        .catch((error) => {
            console.error(error);
            return res.status(500).json(error.message);
        });

        const newUserWithoutPassword = excludehelper.exclude(newUser, ['password']);
        return res.status(201).json(newUserWithoutPassword);
    } else {
        return res.status(400).json('email address al aanwezig in database');
    }
};

export const getAllUsers = async (req: Request, res: Response) => {
    try {
        const allUsers = await db.registeredUsers.findMany();
        return res.status(200).json(allUsers);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const getUserByEmail = async (req: Request, res: Response) => {
    try {
        const foundUser = await db.registeredUsers.findMany({
            where: {
                emailAddress: req.params.emailAddress
            },
        });
        const newUserWithoutPassword = excludehelper.exclude(foundUser, ['password']);
        return res.status(200).json(newUserWithoutPassword);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const getUserByID = async (req: Request, res: Response) => {
    try {
        const userId: number = parseInt(req.params.userId);
        console.log('User ID: ' + userId);
        const foundUser = await db.registeredUsers.findMany({
            where: {
                id: userId
            },
        });
        const newUserWithoutPassword = excludehelper.exclude(foundUser, ['password']);
        return res.status(200).json(newUserWithoutPassword);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const updateUserById = async (req: Request, res: Response) => {
    let salt = crypto.randomBytes(16).toString('base64');
    let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
    req.body.password = salt + "$" + hash;
    const userId: number = parseInt(req.params.userId);
    try {
        const updatedUser = await db.registeredUsers.update({
            where: {
                id: userId,
            },
            data: req.body
        });
        const newUserWithoutPassword = excludehelper.exclude(updatedUser, ['password']);
        return res.status(200).json(newUserWithoutPassword);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const deleteUserById = async (req: Request, res: Response) => {
    const userId: number = parseInt(req.params.userId);
    try {
        await db.registeredUsers.delete({
            where: {
                id: userId,
            },
        });
        return res.status(200).json('user deleted');
    } catch (error) {
        return res.status(500).json(error.message);
    }
};