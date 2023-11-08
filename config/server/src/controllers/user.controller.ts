import crypto from 'crypto';
import type { Request, Response } from "express";
import { db } from "../utils/db.server";

export const createUser = async (req: Request, res: Response) => {
    let salt = crypto.randomBytes(16).toString('base64');
    let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
    req.body.password = salt + "$" + hash;
    // req.body.permissionLevel = 1;
  
    try {
        const newUser = await db.user.create({
            data: req.body
        });
        return res.status(201).json(newUser);
    } catch (error) {
        // return error.message;
        return res.status(500).json(error.message);
    }
};

export const getAllUsers = async (req: Request, res: Response) => {
    try {
        const allUsers = await db.user.findMany();
        return res.status(200).json(allUsers);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const getUserByEmail = async (req: Request, res: Response) => {
    try {
        const foundUser = await db.user.findMany({
            where: {
                emailAddress: req.params.emailAddress
            },
        });
        return res.status(200).json(foundUser);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const getUserByID = async (req: Request, res: Response) => {
    try {
        const userId: number = parseInt(req.params.userId);
        console.log('User ID: ' + userId);
        const foundUser = await db.user.findMany({
            where: {
                id: userId
            },
        });
        return res.status(200).json(foundUser);
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
        const updatedUser = await db.user.update({
            where: {
                id: userId,
            },
            data: req.body
        });
        return res.status(200).json(updatedUser);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const deleteUserById = async (req: Request, res: Response) => {
    const userId: number = parseInt(req.params.userId);
    try {
        await db.user.delete({
            where: {
                id: userId,
            },
        });
        return res.status(200).json('user deleted');
    } catch (error) {
        return res.status(500).json(error.message);
    }
};