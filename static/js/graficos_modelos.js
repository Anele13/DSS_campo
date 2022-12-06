
function crear_grafico_lineas_lana(anios, real, prediccion){
    console.log('Holaaa');
    var ctx = document.getElementById("canvas");

    const numbers = [1,2,3,4,5,6,7]
    const MONTHS = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ];
    function months(config) {
        var cfg = config || {};
        var count = cfg.count || 12;
        var section = cfg.section;
        var values = [];
        var i, value;

        for (i = 0; i < count; ++i) {
        value = MONTHS[Math.ceil(i) % 12];
        values.push(value.substring(0, section));
        }

        return values;
    }
    const CHART_COLORS = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };
    const labels = months({count: 7});;
    const data = {
        labels: labels,
        datasets: [
        {
            label: 'Dataset 1',
            data: numbers,
            borderColor: CHART_COLORS.red,
            backgroundColor: CHART_COLORS.red,
        },
        {
            label: 'Dataset 2',
            data: numbers,
            borderColor: CHART_COLORS.blue,
            backgroundColor: CHART_COLORS.blue,
        }
        ]
    };
    const config = {
        type: 'line',
        data: data,
        options: {
        responsive: true,
        plugins: {
            legend: {
            position: 'top',
            },
            title: {
            display: true,
            text: 'Chart.js Line Chart'
            }
        }
        },
    };
    new Chart(ctx,config)
}