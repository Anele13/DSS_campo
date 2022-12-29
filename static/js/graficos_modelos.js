
function crear_grafico_lineas_lana(anios, real, prediccion, anios2){
    console.log('Holaaa');
    console.log(anios2);
    var ctx = document.getElementById("canvas");
    const CHART_COLORS = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };
    let labels;
    if(anios2){
        console.log('Kio');
        labels = [anios, anios2];
        console.log(labels);
    }else{
        console.log('perro');
        labels = anios;
    }  
    const data = {
        labels: labels,
        datasets: [
        {
            label: 'Real',
            data: real,
            borderColor: CHART_COLORS.red, 
        },
        {
            label: 'Predicción',
            data: prediccion,
            borderColor: CHART_COLORS.blue,
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