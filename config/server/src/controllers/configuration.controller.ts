import type { Request, Response } from "express";
import fs from 'fs';
import path from 'path';

// const config = path.join(__dirname + '../../../config-example.json');
const config = path.join('/etc/server-scripts/backup-config.json');

export const getConfiguration = async function(req: Request, res: Response){
    fs.readFile(config,'utf-8',function (err, data) {
        console.log(data);
        res.send(JSON.parse(data));
    });
};

export const updateConfiguration = async function(req: Request, res: Response){
    const jsonInput = req.body;
    console.log(req);
    console.log(jsonInput);

    try {
        const jsonString = JSON.stringify(jsonInput.data,null,2);
        console.log(jsonString);

        fs.writeFile(config, jsonString, (err) => {
            if (err) {
                console.log('Error writing JSON file: ', err);
                return;
            }
            console.log('JSON file has been saved successfully!');
        });
        res.status(201).send(jsonString);
    } catch (error) {
        console.log('An error has occurred: ', error);
    }
};