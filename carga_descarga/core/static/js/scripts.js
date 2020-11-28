$(document).ready(function(){
    var filter = $('#filter');
    var ordenador = $('#ordenador');
    var listaFilter = document.getElementById("filter");
    var listaOrdenador = document.getElementById("ordenador");
    var baseUrl = window.location.href;

    Url = baseUrl.split('?');
    baseUrl = Url[0];

    (filter).change(function() {
        var filter = $(this).val();
        window.location.href = baseUrl + '?filter=' + filter;
    });

    (ordenador).change(function() {
        var ordenador = $(this).val();
        //window.onload(ordenador.val($("#ordenador option").eq(ordenador.val).val()));
        window.location.href = baseUrl + '?ordenador=' + ordenador;
    });
});