
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function (n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}


function agregar_info_tabla_lateral(mes, temp_min, temp_max, humedad, viento) {
  $('#temperatura_min_' + mes).html(temp_min + ' °')
  $('#temperatura_max_' + mes).html(temp_max + ' °')
  $('#humedad_' + mes).html(humedad + ' %')
  $('#viento_' + mes).html(viento + ' m/s')
}



function agregar_grafico_produccion(mes, cant_carneros, cant_corderos, cant_ovejas) {
  var ctx = document.getElementById("myPieChart_" + mes);
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Cantidad de Carneros", "Cantidad de Corderos", "Cantidad de Ovejas"],
      datasets: [{
        data: [cant_carneros, cant_corderos, cant_ovejas],
        backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
        hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
  });
}



function crear_grafico_baras(mes, dias, lluvia) {
  var datos = []
  for (let index = 0; index < dias.length; index++) {
    const element = dias[index];
    datos.push('Dia: ' + element)

  }
  var ctx = document.getElementById("myBarChart_" + mes);
  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: datos,
      datasets: [{
        label: "Revenue",
        backgroundColor: "#536895",
        hoverBackgroundColor: "#49678d",
        borderColor: "#536895",
        data: lluvia,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'day'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 6,
            // Include a dollar sign in the ticks
            callback: function (value, index, values) {
              return value
            }
          },
          maxBarThickness: 25,
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 20,
            maxTicksLimit: 40,
            padding: 2,
            // Include a dollar sign in the ticks
            callback: function (value, index, values) {
              return value + 'mm.'
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function (tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return 'mm. de lluvia: ' + tooltipItem.yLabel;
          }
        }
      },
    }
  });
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

function crear_grafico_lineas(mes, dias, temperaturas_min, temperaturas_max) {
  var datos = []
  for (let index = 0; index < dias.length; index++) {
    const element = dias[index];
    datos.push(element + ' de ' + mes)

  }
  var ctx = document.getElementById("myAreaChart_" + mes);
  var myLineChart = new Chart(ctx, {
    type: 'line',


    data:  {
      labels: datos,
      datasets: [

          {
              label: 'Maxima',
              data: temperaturas_max,
              borderColor: CHART_COLORS.red,
   
          },
          {
            label: 'Minima',
            data: temperaturas_min,
            borderColor: CHART_COLORS.blue,
        },
      ]
  },


    
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 40,
            maxTicksLimit: 20,
            padding: 10,
            // Include a dollar sign in the ticks
            callback: function (value, index, values) {
              return value + '°';
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        intersect: false,
        mode: 'index',
        caretPadding: 10,
        callbacks: {
          label: function (tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + tooltipItem.yLabel + '°';
          }
        }
      }
    }
  });
}


function crear_grafico_barras_lana(lana, labels) {
  var ctx = document.getElementById("myBarChartLana");
  var myBarChartLana = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: "kg lana producida",
        data: lana,
        backgroundColor: "#4682b4",
        hoverBackgroundColor: "#4e77ac",
        borderColor: "#4682b4",
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          },
          scaleLabel: {
            display: false,
            labelString: 'kg'
          }
        }]
      },
      tooltips: {
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function (tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return 'Kg. de Lana: ' + tooltipItem.yLabel;
          }
        }
      },
    }
  });

};

function crear_grafico_barras_carne(carne, labels) {
  var ctx = document.getElementById("myBarChartCarne");
  var myBarChartLana = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: "kg carne producida",
        data: carne,
        backgroundColor: "#324c6e",
        hoverBackgroundColor: "#3e5f8a",
        borderColor: "#324c6e",
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          },
          scaleLabel: {
            display: false,
            labelString: 'kg'
          }
        }]
      },
      tooltips: {
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function (tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return 'Kg. de Carne: ' + tooltipItem.yLabel;
          }
        }
      },
      responsive: true
    }
  });
};


function crear_grafico_funnel_lluvia(labels, lluvia) {
  var barChartData = {
    labels: labels,
    datasets: [{
      label: 'mm lluvia',
      backgroundColor: "#0B84A5",
      borderColor: '#F6C85F',
      data: lluvia
    }]

  };

  window.onload = function () {
    var ctx = document.getElementById('canvas')
    var chart = new Chart(ctx, {
      type: 'barFunnel',
      data: barChartData,
      options: {
        // Elements options apply to all of the options unless overridden in a dataset
        // In this case, we are setting the border of each bar to be 2px wide and green
        elements: {
          rectangle: {
            borderWidth: 2,
            borderColor: '0B84A5',
            borderSkipped: 'bottom',
            stepLabel: {
              display: true,
              fontSize: 10,
            }
          }
        },
        region: {
          display: true
        },
        responsive: true,
        legend: {
          position: 'top',
        },
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            },
            scaleLabel: {
              display: false,
              labelString: 'mm'
            }
          }]
        },
      }
    });
  }
}




function crear_grafico_barras(elemento_html, dataset1, dataset2, labels, label1, label2) {
  var myBarChartLana = new Chart(elemento_html, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label1,
        data: dataset1,
        hoverBackgroundColor: '#243144',
        borderColor: '#2c3f5a',
      }, {
        label: label2,
        data: dataset2,
        hoverBackgroundColor: '##0495c4',
        borderColor: '#178bb1',
      }

      ],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          },
          gridLines: {
            color: "#dee2eb",
            zeroLineColor: "#dee2eb",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          },
          scaleLabel: {
            display: false,
            labelString: 'kg'
          }
        }]
      },
      tooltips: {
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function (tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + tooltipItem.yLabel;
          }
        }
      },
      responsive: true
    }
  });
};


  //backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
//hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],