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
    NotaFiscal=document.getElementById("NF")
    industria=document.getElementById("industria")
    Produto=document.getElementById("Produto")
    observacao=document.getElementById("observacao")
    var controle=true

    if (industria.value.length > 40 ){
        window.alert("O tamanho maximo do nome da industria é 40 Caracteres")
        controle=false
    }
    if (NotaFiscal.value.length > 45){
        controle=false
        window.alert("O tamanho maximo da NF é 40 Caracteres")

    }
    if(Produto.value.length > 40){
        controle=false
        window.alert("O tamanho maximo do produto é 40 cararacteres")
    }
    if (observacao.value.length > 200){
        controle=false
        window.alert("foi e excedido o tamanho do campo observação")
    }
    
    if (controle == true && window.confirm("deseja confirmar o cadastro  da carga?") ) {
        document.getElementById("formulario").submit();
    }
}