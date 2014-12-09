/**
 * Created by xl on 12/8/14.
 */

function init(){
    get_json("/get/time_range", function(data){
        var min_date = new Date(data['min']);
        var max_date = new Date(data['max']);
        $("#datePicker").dateRangeSlider({
            "bounds": {min: min_date, max: Date.now()},
            "defaultValues": {min: min_date, max: max_date}
        });
    })
}

function get_json(url, call_back){
    d3.json(url, function(error, raw_data){
        call_back(raw_data);
    });
}

init();