/**
 * Created by xl on 12/6/14.
 */

// Adding 500 Data Points
var map, m_heatmap_array, f_heatmap_array;

function update_map() {
    get_json("/get/locations", function (data) {
        var bound = new google.maps.LatLngBounds();

        m_heatmap_array.clear();
        $.each(data[1], function (row) {
            var point = new google.maps.LatLng(+data[0][row]['lat'], +data[0][row]['lng']);
            m_heatmap_array.push(point);
            bound.extend(point);
        });

        f_heatmap_array.clear();
        $.each(data[2], function (row) {
            var point = new google.maps.LatLng(+data[0][row]['lat'], +data[0][row]['lng']);
            f_heatmap_array.push(point);
            bound.extend(point);
        });

        map.fitBounds(bound);
        map.setCenter(bound.getCenter());
    });
}

function initilize_map() {
    //google.maps.event.addDomListener(window, 'load', function () {
        var mapOptions = {
            //center: center.getCenter(),
            //mapTypeId: google.maps.MapTypeId.SATELLITE,
            scrollwheel: false,
            styles: get_style()
        };

        map = new google.maps.Map(document.getElementById('map-canvas'),
            mapOptions);

        m_heatmap_array = new google.maps.MVCArray([]);
        var m_heatmap = new google.maps.visualization.HeatmapLayer({
            data: m_heatmap_array
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

        f_heatmap_array = new google.maps.MVCArray([]);
        var f_heatmap = new google.maps.visualization.HeatmapLayer({
            data: f_heatmap_array
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

        update_map();
    //});
}

