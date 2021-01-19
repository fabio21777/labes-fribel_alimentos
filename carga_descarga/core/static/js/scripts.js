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
    navmod=document.getElementById("navmod")
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
    /*if(path== '/'){
        navmod.innerHTML=''
    }*/
    
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
    if(industria.value.length>0 && industria.value[0]==' '){
        window.alert("O campo industria tem um espaço em branco no inicio por favor remove-lo")
        controle = false
    }
    if (industria.value.length==0){
        window.alert("Campo industria está vazio")
        controle = false
    }

    if (NotaFiscal.value.length > 45){
        controle = false
        window.alert("O tamanho máximo da NF é 40 caracteres!")
    }
    if (NotaFiscal.value.length==0 && controle != false){
        if (window.confirm("Campo nota fiscal está  vazio deseja confirmar? ")){
        }
        else{
            controle = false
        }
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

//Notifica via email sobre as descargas do dia posterior
function notificar_cargas_previstas(lista_cargas, qtde_cargas){
    let lista_dia_descarga = [];
    
    //console.log(lista_cargas);
    
    /*for(i=0; i<qtde_cargas; i++){
        console.log(lista_cargas[i].industria);
    }*/
}

function checar_descarga_cargas(lista_cargas, qtde_cargas){
    //CHECAR CONFLITO DE DIA DE DESCARGA
    var conflito = 0;
    let lista_dia_descarga = [];
    var counts = {};
    //Configurar limite_descargas para alterar o limite de descargas por dia 
    var limite_descargas = 1;
    
    for(i=0; i<qtde_cargas; i++){
        lista_dia_descarga.push(lista_cargas[i].dia_descarga);
    }

    for(i=0; i<lista_dia_descarga.length; i++){
        var num = lista_dia_descarga[i];
        counts[num] = counts[num] ? counts[num] + 1 : 1;
    }

    for(i=0; i<qtde_cargas; i++){
        if(counts[lista_cargas[i].dia_descarga] > limite_descargas){
            window.alert("Existe conflito de dia de descarga!");
            break;
        }
    }

    //CHECAR DIA DE DESCARGA PARA NOTIFICAR POR EMAIL
    var data = new Date();
    var hora = 22;
    var data_posterior = (data.getDate()+1).toString();
    var texto_email = "As cargas abaixo estão previstas para serem descarregadas amanhã ("+data_posterior+"/"+data.getMonth()+"/"+data.getFullYear()+")!\n\n";
    
    //A checagem acontece em um horário específico
    if(data.getHours() == hora){
        for(i=0; i<qtde_cargas; i++){
            if((lista_cargas[i].dia_descarga.substring(2, -5).trim()) == data_posterior){
                texto_email = texto_email + (i+1).toString() + ' - Indústria: ' + 
                lista_cargas[i].industria + ', Número da Nota Fiscal: ' + 
                lista_cargas[i].numero_nf + '\n';
            }
        }
    }
    texto_email = texto_email + "\n\nEste email é automático, por favor não responda."
    
    console.log(texto_email);
}

function msgCargaExcluida(){
    window.alert("Carga excluída com sucesso!");
}