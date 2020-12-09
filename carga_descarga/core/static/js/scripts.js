$(document).ready(function(){
    var filter = $('#filter');
    var ordenador = $('#ordenador');
    var btnSearch = $('#btnSearch');
    var campoBusca = $('#campoBusca');
    var baseUrl = window.location.href;
    bt_add_carga=document.getElementById("bt_add_carga")
    h3_add_carga=document.getElementById("h3_add_carga")
    bt_liberar=document.getElementById("bt_liberar")
    h3_liberar=document.getElementById("h3_liberar")
    bt_list_carga=document.getElementById("bt_list_carga")
    h3_list_carga=document.getElementById("h3_list_carga")
    value_list_carga=document.getElementById("bt_list_carga").value
    path=window.location.pathname
    if (path=='/acompanhamento/adicionarCarga/'){
        h3_add_carga.style.color="#89b348"
        bt_add_carga.style.backgroundColor ="#004b97"
    }
    if (path=='/liberar'){
        h3_liberar.style.color="#89b348"
        bt_liberar.style.backgroundColor ="#004b97"
    }
    if (value_list_carga == "acomp"){
        bt_list_carga.style.backgroundColor ="#004b97"
        h3_list_carga.style.color="#89b348"
    }
    /*var listaFilter = document.getElementById("filter");
    var listaOrdenador = document.getElementById("ordenador");*/

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

    $(btnSearch).on('click', function(){
        campoBusca.submit();
    });
});

function validar_add_carga(){
    NotaFiscal=document.getElementById("NF")
    industria=document.getElementById("industria")
    Produto=document.getElementById("Produto")
    observacao=document.getElementById("observacao")
    previsao=document.getElementById("previsao")
    var controle=true
    const ast="*"
    const alerta=document.getElementById("previsao_h3")
    if (!previsao.value){
        alerta.style.color="red"
        controle=false
    }
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