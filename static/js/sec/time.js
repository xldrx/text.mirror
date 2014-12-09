$(document).ready(function(){
d3.json("/get/times", function (error, raw_data) {
    var categories = [];
    var serie_m = [];
    var serie_f = [];
    raw_data[0].forEach(function(d){
       if (d["gender"]=="m") {
           categories.push(d["Name"]);
           serie_m.push(-d["percentage"] * 100);
       }
       if (d["gender"]=="f")
           serie_f.push(d["percentage"]*100);
    });

    $('#time-div-1').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Day of the Week'
        },
        subtitle: {
            text: 'Message Count'
        },
        xAxis: [{
            categories: categories,
            reversed: false,
            labels: {
                step: 1
            }
        }, { // mirror axis on right side
            opposite: true,
            reversed: false,
            categories: categories,
            linkedTo: 0,
            labels: {
                step: 1
            }
        }],
        yAxis: {
            title: {
                text: null
            },
            labels: {
                formatter: function () {
                        return Math.abs(this.value);
                },
                step: 1
            },
            min: -100,
            max: 100
        },

        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },

        //tooltip: {
        //    formatter: function () {
        //        return '<b>' + this.series.name + ', age ' + this.point.category + '</b><br/>' +
        //            'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
        //    }
        //},

        series: [{
            name: 'Male',
            data: serie_m
        }, {
            name: 'Female',
            data: serie_f
        }]
    });

    // 2
    categories = [];
    serie_m = [];
    serie_f = [];
    raw_data[1].forEach(function(d){
       if (d["gender"]=="m") {
           categories.push(d["Name"]);
           serie_m.push(-d["percentage"] * 100);
       }
       if (d["gender"]=="f")
           serie_f.push(d["percentage"]*100);
    });

    $('#time-div-2').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Day of the Week'
        },
        subtitle: {
            text: 'Message Count'
        },
        xAxis: [{
            categories: categories,
            reversed: false,
            labels: {
                step: 1
            }
        }, { // mirror axis on right side
            opposite: true,
            reversed: false,
            categories: categories,
            linkedTo: 0,
            labels: {
                step: 1
            }
        }],
        yAxis: {
            title: {
                text: null
            },
            labels: {
                formatter: function () {
                        return Math.abs(this.value);
                },
                step: 1
            },
            min: -100,
            max: 100
        },

        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },

        //tooltip: {
        //    formatter: function () {
        //        return '<b>' + this.series.name + ', age ' + this.point.category + '</b><br/>' +
        //            'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
        //    }
        //},

        series: [{
            name: 'Male',
            data: serie_m
        }, {
            name: 'Female',
            data: serie_f
        }]
    });



    // 3
        categories = [];
    serie_m = [];
    serie_f = [];
    raw_data[2].forEach(function(d){
       if (d["gender"]=="m") {
           categories.push(d["Name"]);
           serie_m.push(-d["percentage"] * 100);
       }
       if (d["gender"]=="f")
           serie_f.push(d["percentage"]*100);
    });

    $('#time-div-3').highcharts({
        chart: {
            type: 'bar'
        },
        chartOptions:{
          width: "80vw"
        },
        title: {
            text: 'Day of the Week'
        },
        subtitle: {
            text: 'Message Count'
        },
        xAxis: [{
            categories: categories,
            reversed: false,
            labels: {
                step: 1
            }
        }, { // mirror axis on right side
            opposite: true,
            reversed: false,
            categories: categories,
            linkedTo: 0,
            labels: {
                step: 1
            }
        }],
        yAxis: {
            title: {
                text: null
            },
            labels: {
                formatter: function () {
                        return Math.abs(this.value);
                },
                step: 1
            },
            min: -100,
            max: 100
        },

        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },

        //tooltip: {
        //    formatter: function () {
        //        return '<b>' + this.series.name + ', age ' + this.point.category + '</b><br/>' +
        //            'Population: ' + Highcharts.numberFormat(Math.abs(this.point.y), 0);
        //    }
        //},

        series: [{
            name: 'Male',
            data: serie_m
        }, {
            name: 'Female',
            data: serie_f
        }]
    });

  $('.bxslider').bxSlider({
      'controls': true
  });
})
});