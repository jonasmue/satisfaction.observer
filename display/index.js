const express = require('express');
const app = express();
const port = 3000;

const dataReader = require("./exports/dataReader");

app.get('/recent', (req, res) => {
    let dirPath = './data/recent/';
    let tweetPath = './data/example_tweets/recent/';
    res.json(dataReader.readJsonDir(dirPath, tweetPath, req.query.history));
});

app.get('/popular', (req, res) => {
    let dirPath = './data/popular/';
    let tweetPath = './data/example_tweets/popular/';
    res.json(dataReader.readJsonDir(dirPath, tweetPath, req.query.history));
});

app.use(express.static(__dirname + '/public/'));

app.listen(port, () => console.log("Listening on", port));