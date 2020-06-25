const SatisfactionObserver = (function () {
    'use strict';
    let recent = true;
    let currentHistory = 0;
    let currentCategory = null;

    function getCurrentHistory() {
        return currentHistory;
    }

    function setCurrentHistory(newHistory) {
        currentHistory = newHistory;
    }

    function getCurrentCategory() {
        return currentCategory;
    }

    function setCurrentCategory(newCategory) {
        currentCategory = newCategory;
    }

    function getRecent() {
        return recent;
    }

    function setRecent(isRecent) {
        recent = isRecent;
    }


    return {
        getRecent: getRecent,
        setRecent: setRecent,
        getCurrentCategory: getCurrentCategory,
        setCurrentCategory: setCurrentCategory,
        getCurrentHistory: getCurrentHistory,
        setCurrentHistory: setCurrentHistory
    }

}());

SatisfactionObserver.apiHandler = (function () {
    function getCategories(callback) {
        $.get("/categories", (response) => {
            if (!response.length) return;
            $('.placeholder').html(response[0].title);
            for (let cat of response) {
                $('.select-list__ul').append(
                    "<li><a href='' style='color: " + colorPalette[6] + "' data-category-name='" + cat.name + "'>" + cat.title + "</a><hr>"
                )

            }
            SatisfactionObserver.setCurrentCategory(response[0].name);
            callback(response);
        });
    }

    function getData() {
        $(".tweet-box").hide();
        const type = SatisfactionObserver.getRecent() ? "recent" : "popular";
        $.get("/" + type
            + "?history=" + SatisfactionObserver.getCurrentHistory()
            + "&category=" + SatisfactionObserver.getCurrentCategory(),
            (response) => {
                SatisfactionObserver.dataHandler.onNewData(response);
            });
    }

    return {
        getCategories: getCategories,
        getData: getData
    }

}());

SatisfactionObserver.dataHandler = (function () {

    function onNewData(response) {
        const data = response["items"];
        const tweets = response["tweets"];
        const moreLeft = response["moreLeft"];
        SatisfactionObserver.interactionHandler.setWeekButtons(moreLeft);
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
    }

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

    function getDataForItem(item, data) {
        const result = [];
        for (var day of Object.values(data)) {
            result.unshift(Math.round((day[item] + Number.EPSILON) * 100) / 100);
        }
        return result;
    }

    function getTweetsForItem(item, tweets) {
        const result = {positive: [], negative: []};
        for (var day of Object.values(tweets)) {
            result.positive.unshift(day[item]["pos"]);
            result.negative.unshift(day[item]["neg"]);
        }
        return result;
    }

    function addItemImages() {
        const datasets = myChart.config.data.datasets;
        for (let i in datasets) {
            let dataset = datasets[i];
            const dataForItem = dataset._meta[0].data;
            const itemName = dataset.label;
            const itemLogo = new Image(30, 30);
            let itemImg = itemName.split(" ").join("-").toLowerCase().replace(/[^\x00-\x7F]/g, "").replace("/", "-");
            itemLogo.src = "/images/" + SatisfactionObserver.getCurrentCategory() + "/" + itemImg + ".svg";
            dataForItem[dataForItem.length - 1]._model.pointStyle = itemLogo;
        }
    }

    return {
        onNewData: onNewData,
        addItemImages: addItemImages
    }
}());

SatisfactionObserver.interactionHandler = (function () {

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
            SatisfactionObserver.setCurrentHistory(0);
            SatisfactionObserver.setCurrentCategory($(this).attr("data-category-name"));
            SatisfactionObserver.apiHandler.getData();
        });
        SatisfactionObserver.apiHandler.getData();
    }

    function toggleData(toRecent) {
        if (SatisfactionObserver.getRecent() === toRecent) return;
        SatisfactionObserver.setRecent(!SatisfactionObserver.getRecent());
        let $recentDataButton = $('.recentDataButton');
        let $popularDataButton = $('.popularDataButton');
        const selectButton = toRecent ? $recentDataButton : $popularDataButton;
        const deselectButton = toRecent ? $popularDataButton : $recentDataButton;
        selectButton.addClass("selected");
        deselectButton.removeClass("selected");
        SatisfactionObserver.apiHandler.getData();
    }

    function incrementHistory() {
        SatisfactionObserver.setCurrentHistory(SatisfactionObserver.getCurrentHistory() + 1);
        SatisfactionObserver.apiHandler.getData();
    }

    function decrementHistory() {
        SatisfactionObserver.setCurrentHistory(SatisfactionObserver.getCurrentHistory() - 1);
        SatisfactionObserver.apiHandler.getData(SatisfactionObserver.dataHandler.onNewData);
    }

    function setWeekButtons(moreLeft) {
        $('.newerButton').toggle(SatisfactionObserver.getCurrentHistory() > 0);
        $('.olderButton').toggle(moreLeft);
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
        setWeekButtons: setWeekButtons,
        initializeCategorySelect: initializeCategorySelect
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
    SatisfactionObserver.chartPluginServices.registerUpdateCallback(SatisfactionObserver.dataHandler.addItemImages);
    SatisfactionObserver.interactionHandler.registerEvents();
    SatisfactionObserver.apiHandler.getCategories(SatisfactionObserver.interactionHandler.initializeCategorySelect);
});