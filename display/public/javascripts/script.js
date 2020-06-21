const SatisfactionObserver = (function () {
    'use strict';
    let recent = false;
    let currentHistory = 0;
    let currentCategory = -1;

    function prettyPrintDates(data) {
        const result = [];
        for (const date of data) {
            const split = date.split("_").shift().split("-");
            result.push(monthNames[Number.parseInt(split[1]) - 1] + " " + (Number.parseInt(split[2]) - 1));
        }
        return result
    }

    function getItemNames(data) {
        if (data.length === 0) return [];
        return Object.keys(data[Object.keys(data)[0]]);
    }

    function getDataForItem(leader, data) {
        const result = [];
        for (var day of Object.values(data)) {
            result.unshift(Math.round((day[leader] + Number.EPSILON) * 100) / 100);
        }
        return result;
    }

    function getTweetsForItem(leader, tweets) {
        const result = {positive: [], negative: []};
        for (var day of Object.values(tweets)) {
            result.positive.unshift(day[leader]["pos"]);
            result.negative.unshift(day[leader]["neg"]);
        }
        return result;
    }

    function addItemImages(chart) {
        const datasets = chart.config.data.datasets;
        for (let i in datasets) {
            let dataset = datasets[i];
            const dataForItem = dataset._meta[0].data;
            const itemName = dataset.label;
            const itemLogo = new Image(30, 30);
            let itemImg = itemName.split(" ").join("-").toLowerCase().replace(/[^\x00-\x7F]/g, "");
            itemLogo.src = "/images/" + currentCategory + "/" + itemImg + ".svg";
            dataForItem[dataForItem.length - 1]._model.pointStyle = itemLogo;
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
        $(".tweet-box").hide();
        const type = recent ? "recent" : "popular";
        $.get("/" + type + "?history=" + currentHistory + "&category=" + currentCategory, (response) => {
            const data = response["items"];
            const tweets = response["tweets"];
            const moreLeft = response["moreLeft"];
            setWeekButtons(moreLeft);
            if (Object.keys(data).length === 0) return;
            const labels = prettyPrintDates(Object.keys(data));
            const datasets = [];
            let itemNames = getItemNames(data);
            for (let i in itemNames) {
                const item = itemNames[i];
                datasets.push({
                    label: item,
                    data: getDataForItem(item, data),
                    fill: false,
                    backgroundColor: colorPalette[i],
                    borderColor: colorPalette[i],
                    pointStyle: pointStyles[i % pointStyles.length],
                    pointRadius: 6,
                    lineTension: 0.15,
                    tweets: getTweetsForItem(item, tweets)
                })
            }
            myChart.data.datasets = datasets;
            myChart.data.labels = labels.reverse();
            myChart.update();
        });
    }

    function getCategories() {
        $.get("/categories", (response) => {
            if (!response.length) return;
            $('.placeholder').html(response[0].title);
            for (let cat of response) {
                $('.select-list__ul').append(
                    "<li><a href='' style='color: " + colorPalette[1] + "' data-category-name='" + cat.name + "'>" + cat.title + "</a><hr>"
                )

            }
            currentCategory = response[0].name;
            initializeCategorySelect();
            getData();
        });
    }

    function initialize() {
        registerEvents();
        getCategories();
    }

    function initializeCategorySelect() {

        let placeHolderSel = '.placeholder';
        let listUlSel = '.select-list__ul';

        $(placeHolderSel).click(() => {
            $(placeHolderSel).css('opacity', '0');
            $(listUlSel).toggle();
        });

        $(listUlSel + ' a').click(function (e) {
            e.preventDefault();
            var index = $(this).parent().index();

            let text = $(this).text();
            $(placeHolderSel).text(text).css('opacity', '1');

            $(listUlSel).find('li').eq(index).prependTo(listUlSel);
            $(listUlSel).toggle();
            currentCategory = $(this).attr("data-category-name");
            getData();
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
        intilialize: initialize,
        updateCallback: addItemImages
    }

}());

SatisfactionObserver.chartPluginServices = (function () {
    function registerUpdateCallback(callback) {
        Chart.pluginService.register({
            afterUpdate: (chart) => {
                callback(chart);
            }
        })
    }

    return {registerUpdateCallback: registerUpdateCallback}
}());

/************************************
 *          ONLOAD EVENTS
 ************************************/

$(document).ready(() => {
    SatisfactionObserver.chartPluginServices.registerUpdateCallback(SatisfactionObserver.updateCallback);
    SatisfactionObserver.intilialize();
});