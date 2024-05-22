const express = require('express');
const fs = require('fs');
const app = express();
const PORT = 8081;

app.get('/', function (req,res) {
    res.redirect('/config');
});

app.get('/config', function(req,res){
    fs.readFile('/etc/server-scripts/backup-config.json','utf-8',function (err, data) {
        console.log(data);
        res.end(data);
    });
});

app.listen(PORT, function (err) {
    if (err) console.log(err);
    console.log("Config api server op PORT",PORT);
});