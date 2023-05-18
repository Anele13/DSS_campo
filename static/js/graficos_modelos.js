function armar_labels(label_real,label_prediccion) {
    const label = label_real.concat(label_prediccion)
    return [... new Set(label)]
}

function completar_data(label_real, y_prediccion) {
    const cantElementsLabelReal = label_real.length
    const listNull = []
    for(let i=1; i<=cantElementsLabelReal; i++){
      listNull.push(null)
    }
    return listNull.concat(y_prediccion)
}

function crear_grafico_lineas(anios, real, prediccion, idElement){
    var ctx = document.getElementById(idElement);
    const CHART_COLORS = {
        red: 'rgb(255, 99, 132)',
        orange: 'rgb(255, 159, 64)',
        yellow: 'rgb(255, 205, 86)',
        green: 'rgb(75, 192, 192)',
        blue: 'rgb(54, 162, 235)',
        purple: 'rgb(153, 102, 255)',
        grey: 'rgb(201, 203, 207)'
    };
    let labels = anios;
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