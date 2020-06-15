const fontFamily = "'Georgia', 'Cambria', 'Times New Roman', 'Times', serif";
const fontColor = "black";
const fontSize = 13;

const colorPalette = [
    "#8c1526",
    "#d6604d",
    "#faaa87",
    "#f9f9f9",
    "#d1e5f0",
    "#87bad3",
    "#2f7c9c",
    "#0a2840"
];
const monthNames = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
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
                    fontFamily: fontFamily,
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
                    fontFamily: fontFamily
                }
            }]
        }
    }
});