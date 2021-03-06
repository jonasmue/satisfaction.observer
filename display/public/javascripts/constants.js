const fontFamily = "'Georgia', 'Cambria', 'Times New Roman', 'Times', serif";
const fontFamilySans = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'";
const fontColor = "black";
const fontSize = 13;

const colorPalette = [
    "#8c1526",
    "#d6604d",
    "#faaa87",
    "#c6c6c6",
    "#d1e5f0",
    "#87bad3",
    "#2f7c9c",
    "#0a2840"
];

const pointStyles = [
    "circle",
    "rectRot",
    "rect",
    "triangle"
];

const ctx = document.getElementById("myChart");
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: []
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
            labels: {
                fontFamily: fontFamily,
                fontColor: fontColor,
                fontSize: fontSize,
                fontWeight: "bold"
            },
            position: "bottom",
            onHover: (e) => {
                e.target.style.cursor = 'pointer';
            }
        },
        scales: {
            xAxes: [{
                ticks: {
                    fontFamily: fontFamily,
                    fontColor: fontColor
                },
                scaleLabel: {
                    display: true,
                    labelString: "Date",
                    fontFamily: fontFamilySans,
                    fontSize: fontSize
                }
            }],
            yAxes: [{
                ticks: {
                    fontFamily: fontFamily,
                    fontColor: fontColor,
                    fontSize: fontSize
                },
                scaleLabel: {
                    display: true,
                    labelString: "% Satisfaction",
                    fontFamily: fontFamilySans
                }
            }]
        },
        tooltips: {
            callbacks: {
                afterLabel: (tooltipItem, data) => {
                    function getTweet(t) {
                        if (typeof t !== "object") return t;
                        const tweetText = Object.values(t)[0];
                        const tweetId = Object.keys(t)[0];
                        return tweetText
                            + "<div class='block mt-1'>"
                            + "<a class='uppercase text-blue-700 font-bold text-xs' target='_blank' href='https://twitter.com/i/status/" + tweetId + "'>Open on Twitter</a>"
                            + "</div>"
                    }

                    const dataset = data["datasets"][tooltipItem.datasetIndex];

                    const positiveTweet = getTweet(dataset.tweets["positive"][tooltipItem.index][0]);
                    const negativeTweet = getTweet(dataset.tweets["negative"][tooltipItem.index][0]);

                    $(".item-tweet").html(dataset.label);
                    $(".date-tweet").html(data.labels[tooltipItem.index]);
                    $(".positive-tweet").find(".content").html(positiveTweet);
                    $(".negative-tweet").find(".content").html(negativeTweet);
                    $(".tweet-box").slideDown("fast");
                }

            }
        }
    }
});