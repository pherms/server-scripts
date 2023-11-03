const express = require('express');
const cors = require('cors');
const fs = require('fs');
const app = express();
const PORT = 8081;
const config = 'config-example.json';

app.use(express.json());
app.use(cors());

app.get('/', function (req,res) {
    res.redirect('/config');
});

app.get('/config', function(req,res){
    fs.readFile(config,'utf-8',function (err, data) {
        console.log(data);
        res.send(data);
    });
});

app.put('/update', function(req,res){
    const jsonInput = req.body;

    res.send('Updating config');
    try {
        putFunction(jsonInput,config);
    } catch (error) {
        console.log('An error has occurred: ', error);
    }
});

app.listen(PORT, function (err) {
    if (err) console.log(err);
    console.log("Config api server op PORT",PORT);
});

function putFunction(jsonInput, filePath) {
    const jsonString = JSON.stringify(jsonInput,null,2);

    fs.writeFile(filePath, jsonString, (err) => {
        if (err) {
            console.error('Error writing JSON file: ', err);
            return;
        }
        console.log('JSON file has been saved successfully!');
    });
}