$(document).ready(function(){
    var controle = 0;
    var filter = $('#filter');

    if(controle>0){
        var baseUrl = window.location.href;
    }

    (filter).change(function() {
        controle = controle + 1;
        var filter = $(this).val();
        window.location.href = baseUrl + '?filter=' + filter;
    });
});