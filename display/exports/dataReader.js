const fs = require('fs');
const moment = require('moment');

module.exports = {
    readJsonDir: function (dirPath, tweetPath, history) {
        const files = fs.readdirSync(dirPath);
        let obj = {items: {}, tweets: {}, moreLeft: false};

        let historyInt = Number.parseInt(history);
        if (Number.isNaN(historyInt)) throw RangeError("History parameter is not valid");
        historyInt = Math.max(historyInt, 0);
        index = !!history ? historyInt * 7 : 0;

        if (index > files.length - 7) {
            return obj
        }
        for (var i = index; i < index + 7; i++) {
            const file = files[files.length - 1 - i];
            const date = file.split(".").shift().split("_").shift();
            const formattedDate = moment(date).subtract(1, "days").format("MMM D");
            obj["items"][formattedDate] = JSON.parse(fs.readFileSync(dirPath + file, "utf8"));
            obj["tweets"][formattedDate] = JSON.parse(fs.readFileSync(tweetPath + file, "utf8"));
        }
        obj["moreLeft"] = files.length >= index + 14; // is there another full week left?

        return obj
    }
};