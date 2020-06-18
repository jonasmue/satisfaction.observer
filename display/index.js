const express = require('express');
const app = express();
const port = 3000;

const dataReader = require("./exports/dataReader");

app.get('/recent', (req, res) => {
    let dirPath = './data/recent/';
    let tweetPath = './data/example_tweets/recent/';
    try {
        res.json(dataReader.readJsonDir(dirPath, tweetPath, req.query.history));
    } catch (e) {
        res.statusMessage = "The request contained bad parameters";
        res.status(400).end();
    }
});

app.get('/popular', (req, res) => {
    let dirPath = './data/popular/';
    let tweetPath = './data/example_tweets/popular/';
    try {
        res.json(dataReader.readJsonDir(dirPath, tweetPath, req.query.history));
    } catch (e) {
        res.statusMessage = "The request contained bad parameters";
        res.status(400).end();
    }
});

app.use(express.static(__dirname + '/public/'));

app.listen(port, () => console.log("Listening on", port));