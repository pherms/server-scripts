import crypto from 'crypto';
import type { Request, Response } from "express";
import { db } from "../utils/db.server";
import { Prisma } from '@prisma/client';

export const createUser = async (req: Request, res: Response) => {
    let salt = crypto.randomBytes(16).toString('base64');
    let hash = crypto.createHmac('sha512', salt).update(req.body.password).digest("base64");
    req.body.password = salt + "$" + hash;
    req.body.permissionLevel = 1;
  
    // const {firstName, lastName, emailAddress, password, permissionLevel} = req.body;
    try {
        const newUser = await db.user.create({
            data: req.body
        });
        return res.status(201).json(newUser);
    } catch (error) {
        // return error.message;
        return res.status(500).json(error.message);
    }

    // .then((result) => {
    //     res.status(201).send({id: result.id});
    // })
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
                emailAddress: req.body.emailAddress
            },
        });
        return res.status(200).json(foundUser);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const getUserByID = async (req: Request, res: Response) => {
    try {
        const id: number = parseInt(req.params.id);
        const foundUser = await db.user.findMany({
            where: {
                id: id
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
    // req.body.permissionLevel = 1;
    const id: number = parseInt(req.params.id);
    try {
        const updatedUser = await db.user.update({
            where: {
                id: id,
            },
            data: req.body
        });
        return res.status(200).json(updatedUser);
    } catch (error) {
        return res.status(500).json(error.message);
    }
};

export const deleteUserById = async (req: Request, res: Response) => {
    const id: number = parseInt(req.params.id);
    try {
        await db.user.delete({
            where: {
                id: id,
            },
        });
        return res.status(200).json('user deleted');
    } catch (error) {
        return res.status(500).json(error.message);
    }
};