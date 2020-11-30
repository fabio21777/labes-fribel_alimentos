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

function validar_add_carga(){
    window.alert('Falta colocar as validações!')
    document.getElementById("formulario").submit();
}

function checar_conflito_cargas(lista_cargas, qtde){
    //context_dict['lista_cargas']=json.dumps(lista_cargas);
    console.log(lista_cargas);
    console.log("numero nf 1a carga: " + lista_cargas[0].numero_nf);
    //for(i=0; i<qtde; i++){
        //console.log(lista_cargas[i]);
    //}
}