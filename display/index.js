const express = require('express');
const app = express();
const port = 3000;
const fs = require('fs');

const categories = JSON.parse(fs.readFileSync("./data/categories.json"))["categories"];
const dataReader = require("./exports/dataReader");

function returnBadRequest(res) {
    res.statusMessage = "The request contained bad parameters";
    res.status(400).end();
}

function isCategoryValid(categoryName) {
    for (let category of categories) {
        if (category.name === categoryName) {
            return true;
        }
    }
    return false;
}

function checkCategory(category, res) {

    if (!category) {
        returnBadRequest(res);
        return false;
    }
    if (!isCategoryValid(category)) {
        returnBadRequest(res);
        return false;
    }
    return true;
}

app.get('/categories', (req, res) => {
    res.json(categories);
});

app.get('/recent', (req, res) => {
    const category = req.query.category;
    if (!checkCategory(category, res)) return;
    try {
        let dataDir = './data/' + category;
        const dirPath = dataDir + '/recent/';
        const tweetPath = dataDir + '/example_tweets/recent/';
        res.json(dataReader.readJsonDir(dirPath, tweetPath, req.query.history));
    } catch (e) {
        returnBadRequest(res);
    }
});

app.get('/popular', (req, res) => {
    const category = req.query.category;
    if (!checkCategory(category, res)) return;
    try {
        let dataDir = './data/' + category;
        const dirPath = dataDir + '/popular/';
        const tweetPath = dataDir + '/example_tweets/popular/';
        res.json(dataReader.readJsonDir(dirPath, tweetPath, req.query.history));
    } catch (e) {
        returnBadRequest(res);
    }
});

app.use(express.static(__dirname + '/public/'));

app.listen(port, () => console.log("Listening on", port));