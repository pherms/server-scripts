"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.updateSources = exports.getSources = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const sources = path_1.default.join('/etc/server-scripts/sources');
const getSources = async function (req, res) {
    fs_1.default.readFile(sources, 'utf-8', function (err, data) {
        console.log(data);
        res.json(data).send;
    });
};
exports.getSources = getSources;
const updateSources = async function (req, res) {
    const jsonInput = req.body;
    console.log(jsonInput);
    try {
        // const jsonString = JSON.stringify(jsonInput.data,null,2);
        const sourcesData = jsonInput.data.toString();
        console.log(sourcesData);
        fs_1.default.writeFile(sources, sourcesData, (err) => {
            if (err) {
                console.log('Error writing sources file: ', err);
                return;
            }
            console.log('Sources file has been saved successfully!');
        });
        res.status(201).send(sourcesData);
    }
    catch (error) {
        console.log('An error has occurred: ', error);
    }
};
exports.updateSources = updateSources;
//# sourceMappingURL=sources.controller.js.map