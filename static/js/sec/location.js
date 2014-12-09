/**
 * Created by xl on 12/6/14.
 */

// Adding 500 Data Points
var map, m_heatmap, f_heatmap;

function initialize() {
    $.getJSON("get/locations", function (data, error) {
        var m_items = [];
        var f_items = [];
        var bound = new google.maps.LatLngBounds();

        $.each(data[2], function (row) {
            var point = new google.maps.LatLng(+data[0][row]['lat'], +data[0][row]['lng']);
            f_items.push(point);
            bound.extend(point);

        });

        $.each(data[1], function (row) {
            var point = new google.maps.LatLng(+data[0][row]['lat'], +data[0][row]['lng']);
            m_items.push(point);
            bound.extend(point);
        });

        initilize_map(m_items, f_items, bound);
    });
}

function initilize_map(m_data, f_data, center) {
    var mapOptions = {
        center: center.getCenter(),
        //mapTypeId: google.maps.MapTypeId.SATELLITE,
        scrollwheel: false,
        styles: get_style()
    };

    map = new google.maps.Map(document.getElementById('map-canvas'),
        mapOptions);
    map.fitBounds(center);

    m_heatmap = new google.maps.visualization.HeatmapLayer({
        data: new google.maps.MVCArray(m_data)
    });

    m_heatmap.set('radius', 12);
    m_heatmap.setMap(map);

    var m_gradient = [
        'rgba(0,0,0,0)',
        'blue',
        'blue',
        'blue',
        'blue'
    ]
    m_heatmap.set('gradient', m_gradient);
    m_heatmap.set('opacity', 1);

    f_heatmap = new google.maps.visualization.HeatmapLayer({
        data: new google.maps.MVCArray(f_data)
    });

    f_heatmap.set('radius', 12);
    f_heatmap.setMap(map);

    var f_gradient = [
        'rgba(0,0,0,0)',
        'red',
        'red',
        'red',
        'red'
    ]
    f_heatmap.set('gradient', f_gradient);
    f_heatmap.set('opacity', 1);
}

google.maps.event.addDomListener(window, 'load', initialize);
