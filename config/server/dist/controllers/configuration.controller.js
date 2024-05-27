"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.updateConfiguration = exports.getConfiguration = void 0;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
// const config = path.join(__dirname + '../../../config-example.json');
const config = path_1.default.join('/etc/server-scripts/backup-config.json');
const getConfiguration = async function (req, res) {
    fs_1.default.readFile(config, 'utf-8', function (err, data) {
        console.log(data);
        res.send(JSON.parse(data));
    });
};
exports.getConfiguration = getConfiguration;
const updateConfiguration = async function (req, res) {
    const jsonInput = req.body;
    console.log(req);
    console.log(jsonInput);
    try {
        const jsonString = JSON.stringify(jsonInput.data, null, 2);
        console.log(jsonString);
        fs_1.default.writeFile(config, jsonString, (err) => {
            if (err) {
                console.log('Error writing JSON file: ', err);
                return;
            }
            console.log('JSON file has been saved successfully!');
        });
        res.status(201).send(jsonString);
    }
    catch (error) {
        console.log('An error has occurred: ', error);
    }
};
exports.updateConfiguration = updateConfiguration;
//# sourceMappingURL=configuration.controller.js.map