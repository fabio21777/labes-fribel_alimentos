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
    NotaFiscal = document.getElementById("NF")
    industria = document.getElementById("industria")
    Produto = document.getElementById("Produto")
    observacao = document.getElementById("observacao")
    var controle = true

    if (industria.value.length > 40 ){
        window.alert("O tamanho máximo do nome da indústria é 40 caracteres!")
        controle = false
    }
    if (NotaFiscal.value.length > 45){
        controle = false
        window.alert("O tamanho máximo da NF é 40 caracteres!")
    }
    if(Produto.value.length > 40){
        controle = false
        window.alert("O tamanho máximo do produto é 40 cararacteres!")
    }
    if (observacao.value.length > 200){
        controle = false
        window.alert("Foi excedido o tamanho do campo observação!")
    }
    
    if (controle == true && window.confirm("deseja confirmar o cadastro  da carga?") ) {
        document.getElementById("formulario").submit();
    }
}

function checar_conflito_cargas(lista_cargas, qtde_cargas){
    var conflito = 0;
    let lista_dia_descarga = [];
    var counts = {};

    for(i=0; i<qtde_cargas; i++){
        lista_dia_descarga.push(lista_cargas[i].dia_descarga);
    }

    for(i=0; i<lista_dia_descarga.length; i++){
        var num = lista_dia_descarga[i];
        counts[num] = counts[num] ? counts[num] + 1 : 1;
    }

    for(i=0; i<qtde_cargas; i++){
        if(counts[lista_cargas[i].dia_descarga] > 1){
            alert("Existe conflito de dia de descarga!");
            break;
        }
    }
}