$(document).ready(function(){
    var baseUrl = 'http://localhost:8000/';
    var filter = $('#filter');

    (filter).change(function() {
        var filter = $(this).val();
        console.log(filter);
        //window.location.href = baseUrl + '?filter=' + filter;
    });
});