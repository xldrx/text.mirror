/**
 * Created by xl on 12/8/14.
 */

function init(){
    d3.json("/get/time_range", function(error, data){
        var min_date = new Date(data['min']);
        var max_date = new Date(data['max']);
        $("#datePicker").dateRangeSlider({
            "bounds": {min: min_date, max: Date.now()},
            "defaultValues": {min: min_date, max: max_date}
        });
        $(".slider").simpleSlider({
            pauseOnHover: true
        });
        update_overview();
        update_times();
        initilize_map();
    });
}


$(document).ready(function() {
    init();
});

function update_all(){
    update_overview();
    update_times();
    update_map();
}