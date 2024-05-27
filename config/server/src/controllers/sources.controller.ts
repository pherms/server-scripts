import type { Request, Response } from "express";
import fs from 'fs';
import path from 'path';

const sources = path.join('/etc/server-scripts/sources');

export const getSources = async function(req: Request, res: Response){
    fs.readFile(sources,'utf-8',function (err, data) {
        console.log(data);
        res.json(data).send;
    });
};

export const updateSources = async function(req: Request, res: Response){
    const jsonInput = req.body;
    console.log(jsonInput);

    try {
        // const jsonString = JSON.stringify(jsonInput.data,null,2);
        const sourcesData = jsonInput.data.toString();
        console.log(sourcesData);

        fs.writeFile(sources, sourcesData, (err) => {
            if (err) {
                console.log('Error writing sources file: ', err);
                return;
            }
            console.log('Sources file has been saved successfully!');
        });
        res.status(201).send(sourcesData);
    } catch (error) {
        console.log('An error has occurred: ', error);
    }
};