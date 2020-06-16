const fs = require('fs');

module.exports = {
    readJsonDir: function (dirPath, tweetPath, history) {
        const files = fs.readdirSync(dirPath);
        let obj = {items: {}, tweets: {}};
        var index = 0;
        try {
            let historyInt = Number.parseInt(history);
            historyInt = Math.max(historyInt, 0);
            index = !!history ? historyInt * 7 : 0
        } catch (e) {
            return {moreLeft: false, items: {}}
        }
        if (index > files.length - 7) {
            return {moreLeft: false, items: {}}
        }
        for (var i = index; i < index + 7; i++) {
            const file = files[files.length - 1 - i];
            const date = file.split(".").shift();
            obj["items"][date] = JSON.parse(fs.readFileSync(dirPath + file, "utf8"));
            obj["tweets"][date] = JSON.parse(fs.readFileSync(tweetPath + file, "utf8"));
        }
        obj["moreLeft"] = files.length >= index + 14; // is there another full week left?

        return obj
    }
};