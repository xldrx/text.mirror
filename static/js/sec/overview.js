/**
 * Created by xl on 12/6/14.
 */

//
//var width = $("#overview-div").width(),
//    height = $("#overview-div").height(),
//    radius = Math.min(width, height) / 2;
//
//var color = d3.scale.ordinal()
//    .range(["pink", "green"]);
//
//var arc = d3.svg.arc()
//    .outerRadius(radius - 10)
//    .innerRadius(radius - 70)
//
//var arc2 = d3.svg.arc()
//    .outerRadius(radius - 10)
//    .innerRadius(radius - 80);
//
//var pie = d3.layout.pie()
//    .sort(null)
//    .value(function (d) {
//        return d.count;
//    });
//
//
//var svg = d3.select("div#overview-div")
//    .append("div")
//    .classed("svg-container", true) //container class to make it responsive
//    .append("svg")
//    //responsive SVG needs these 2 attributes and no width and height attr
//    .attr("preserveAspectRatio", "xMinYMin meet")
//    .attr("viewBox", "0 0 " + width + " " + height)
//    //class to make it responsive
//    .classed("svg-content-responsive", true)
//    .append("g")
//    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
//
//d3.json("/get/overview", function (error, raw_data) {
//    data = raw_data[2];
//    data.forEach(function (d) {
//        d.count = +d.count;
//        d.name = d.name;
//    });
//
//    var g = svg.selectAll(".arc")
//        .data(pie(data))
//        .enter().append("g")
//        .attr("class", "arc");
//
//    g.append("path")
//        .attr("d", arc)
//        .style("fill", function (d) {
//            return color(d.data.name);
//        });
//
//    g.append("text")
//        .attr("transform", function (d) {
//            return "translate(" + arc.centroid(d) + ")";
//        })
//        .attr("dy", ".35em")
//        .style("text-anchor", "middle")
//        .text(function (d) {
//            return d.data.name;
//        });
//
//    data2 = raw_data[1];
//    data2.forEach(function (d) {
//        d.count = +d.count;
//        d.name = d.name;
//    });
//
//    var g2 = svg.selectAll(".arc")
//    .data(pie(data2))
//    .enter().append("g")
//    .attr("class", "arc");
//
//
//    g2.append("path")
//        .attr("d", arc2)
//        .style("fill", function (d) {
//            return color(d.data.name);
//        });
//
//    g2.append("text")
//        .attr("transform", function (d) {
//            return "translate(" + arc2.centroid(d) + ")";
//        })
//        .attr("dy", ".35em")
//        .style("text-anchor", "middle")
//        .text(function (d) {
//            return d.data.name;
//        });
//});



$(document).ready(function() {
    d3.json("/get/overview", function (error, raw_data) {
        var data = [];
        var i =0;
        data[i] = [
            [raw_data[i][0].name, +raw_data[i][0].count],
            [raw_data[i][1].name, +raw_data[i][1].count]
        ];
        i+=1;
        data[i] = [
            [raw_data[i][0].name, +raw_data[i][0].count],
            [raw_data[i][1].name, +raw_data[i][1].count]
        ];
        i+=1;
        data[i] = [
            [raw_data[i][0].name, +raw_data[i][0].count],
            [raw_data[i][1].name, +raw_data[i][1].count]
        ];

        $('#overview-div').highcharts({
            chart: {
                type: 'pie'
            },
            title: {
                text: null
            },
            yAxis: {
                title: {
                    text: 'Number of Messages'
                }
            },
            plotOptions: {
                pie: {
                    shadow: false,
                    center: ['50%', '50%']
                }
            },
            tooltip: {
        	    //valueSuffix: '%'
                pointFormat: '{series.name}: <b>{point.y}</b>'
            },
            series: [{
                name: 'All',
                data: data[0],
                size: '40%',
                innerSize: '10%',
                showInLegend: true,

                dataLabels: {
                    formatter: function() {
                        return this.point.name != "Boys"? null: "All";
                    },
                    color: 'white',
                    distance: -40
                }
            }, {
                name: 'Sent',
                data: data[1],
                size: '70%',
                innerSize: '40%',
                dataLabels: {
                    formatter: function() {
                        return this.point.name != "Boys"? null: "Sent";
                    },
                    color: 'white',
                    distance: -35
                }
            }, {
                name: 'Recieved',
                data: data[2],
                size: '100%',
                innerSize: '70%',
                dataLabels: {
                    formatter: function() {
                        return this.point.name != "Boys"? null: "Recieved";
                    },
                    color: 'white',
                    distance: -30
                }
            }]
        });
    });
});


