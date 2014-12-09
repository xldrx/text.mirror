/**
 * Created by xl on 12/6/14.
 */

function update_overview() {
    get_json("/get/overview", function (raw_data) {
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
}


