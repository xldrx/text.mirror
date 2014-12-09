/**
 * Created by xl on 12/8/14.
 */

function get_json(url, call_back){
    var args = {
            to_date: $("#datePicker").dateRangeSlider('max'),
            from_date: $("#datePicker").dateRangeSlider('min')
    };

    d3.json(url)
    .header("Content-Type", "application/json")
    .post(JSON.stringify(args), function(error, data) {
            call_back(data);
    });
}

