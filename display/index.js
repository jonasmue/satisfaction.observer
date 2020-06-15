const express = require('express');
const app = express();
const port = 3000;

const dataReader = require("./exports/dataReader");

app.get('/recent', (req, res) => {
    let dirPath = './data/recent/';
    res.json(dataReader.readJsonDir(dirPath, req.query.history));
});

app.get('/popular', (req, res) => {
    let dirPath = './data/popular/';
    res.json(dataReader.readJsonDir(dirPath, req.query.history));
});

app.use(express.static(__dirname + '/public/'));

app.listen(port, () => console.log("Listening on", port));