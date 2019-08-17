/* globals Chart:false, feather:false */

data_raw = {}

function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      data_raw = JSON.parse(this.responseText);
      setup_chart();
    }
  };
  xhttp.open("GET", "/get_estadistica", true);
  xhttp.send();
}

function setup_chart() {
  'use strict'
  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data_raw.DATA.labels,
      datasets: data_raw.DATA.datasets
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: true
      }
    }
  })
}

loadDoc();
