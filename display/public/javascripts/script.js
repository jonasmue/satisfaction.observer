const SatisfactionObserver = (function () {
    'use strict';
    let recent = true;
    let currentHistory = 0;

    function prettyPrintDates(data) {
        const result = [];
        for (const date of data) {
            const split = date.split("_").shift().split("-");
            result.push(monthNames[Number.parseInt(split[1]) - 1] + " " + (Number.parseInt(split[2]) - 1));
        }
        return result
    }

    function getLeaderNames(data) {
        if (data.length === 0) return [];
        return Object.keys(data[Object.keys(data)[0]]);
    }

    function getDataForLeader(leader, data) {
        const result = [];
        for (var day of Object.values(data)) {
            result.push(Math.round((day[leader] + Number.EPSILON) * 100) / 100);
        }
        return result;
    }

    function addLeaderImages(data) {
        let leaderNames = getLeaderNames(data);
        for (let i in leaderNames) {
            const dataForLeader = myChart.config.data.datasets[i]._meta[0].data;
            const leaderFlag = new Image(30, 30);
            let leaderImg = leaderNames[i].split(" ").join("-").toLowerCase().replace(/[^\x00-\x7F]/g, "");
            leaderFlag.src = "/images/" + leaderImg + ".svg";
            dataForLeader[dataForLeader.length - 1]._model.pointStyle = leaderFlag;
        }
    }

    function incrementHistory() {
        currentHistory += 1;
        getData();
    }

    function decrementHistory() {
        currentHistory -= 1;
        getData();
    }

    function setWeekButtons(moreLeft) {
        $('.newerButton').toggle(currentHistory > 0);
        $('.olderButton').toggle(moreLeft);
    }

    function toggleData(toRecent) {
        if (recent === toRecent) return;
        recent = !recent;
        let $recentDataButton = $('.recentDataButton');
        let $popularDataButton = $('.popularDataButton');
        const selectButton = toRecent ? $recentDataButton : $popularDataButton;
        const deselectButton = toRecent ? $popularDataButton : $recentDataButton;
        selectButton.addClass("selected");
        deselectButton.removeClass("selected");
        getData();
    }

    function getData() {
        const type = recent ? "recent" : "popular";
        $.get("/" + type + "?history=" + currentHistory, (response) => {
            const data = response["items"];
            const moreLeft = response["moreLeft"];
            setWeekButtons(moreLeft);
            if (Object.keys(data).length === 0) return;
            const labels = prettyPrintDates(Object.keys(data));
            const datasets = [];
            let leaderNames = getLeaderNames(data);
            for (let i in leaderNames) {
                const leader = leaderNames[i];
                datasets.push({
                    label: leader,
                    data: getDataForLeader(leader, data).reverse(),
                    fill: false,
                    backgroundColor: colorPalette[i],
                    borderColor: colorPalette[i],
                    pointStyle: pointStyles[i % pointStyles.length],
                    pointRadius: 6,
                    lineTension: 0.15
                })
            }
            myChart.data.datasets = datasets;
            myChart.data.labels = labels.reverse();
            myChart.update();
            addLeaderImages(data);
        });
    }


    function registerEvents() {
        $('.popularDataButton').click(() => {
            toggleData(false);
        });
        $('.recentDataButton').click(() => {
            toggleData(true);
        });
        $('.olderButton').click(() => {
            incrementHistory();
        });
        $('.newerButton').click(() => {
            decrementHistory();
        });
    }

    return {
        registerEvents: registerEvents,
        requestData: getData
    }

}());

/************************************
 *          ONLOAD EVENTS
 ************************************/

$(document).ready(() => {
    SatisfactionObserver.registerEvents();
    SatisfactionObserver.requestData();
});