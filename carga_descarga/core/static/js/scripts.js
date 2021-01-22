
$(document).ready(function(){
    var filter = $('#filter');
    var ordenador = $('#ordenador');
    var btnSearch = $('#btnSearch');
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

    Url = baseUrl.split('?');
    baseUrl = Url[0];

    (filter).change(function() {
        var filter = $(this).val();
        window.location.href = baseUrl + '?filter=' + filter;
    });

    (ordenador).change(function() {
        var ordenador = $(this).val();
        
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
function notificar_cargas_previstas(texto_email){
    //É necessário ativar "acesso a app menos seguro" na conta gmail
    Email.send({
        Host : "smtp.gmail.com",
        Username : "labes.fribel@gmail.com",
        Password : "Projetofribel10.",
        To : 'yannfabricio@gmail.com',
        From : "labes.fribel@gmail.com",
        Subject : "Cargas previstas",
        Body : texto_email
    });
    console.log('Email de notificação enviado!');
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
    var hora = 10;
    var minuto = 26;
    var data_posterior = (data.getDate()+1).toString();
    var texto_email = "As cargas abaixo estão previstas para serem descarregadas amanhã ("+data_posterior+"/"+(data.getMonth()+1).toString()+"/"+data.getFullYear()+")!<br><br>";
    var controle = false;
    var indice_carga = 1;

    //A checagem acontece em um horário específico
    if(data.getHours() == hora && data.getMinutes() == minuto){
        for(i=0; i<qtde_cargas; i++){
            if((lista_cargas[i].dia_descarga.substring(2, -5).trim()) == data_posterior){
                texto_email = texto_email + (indice_carga).toString() + ' - Indústria: ' + 
                lista_cargas[i].industria + ', Número da Nota Fiscal: ' + 
                lista_cargas[i].numero_nf + '<br>';
                controle = true;
                indice_carga ++;
            }
        }
        texto_email = texto_email + "<br><br>Este email é automático, por favor não responda."
        
        if(controle == true){
            notificar_cargas_previstas(texto_email);
        }
    }
}

function msgCargaExcluida(){
    window.alert("Carga excluída com sucesso!");
}
var cont=0;
function adiconar_itens(){
    conthtml=cont+1
    var html = "";
    html+="<h3 style='text-align: center;'>item  "+conthtml +"</h3>"
    html += "<div style='margin-top: 8px;' class='row' >";
    html += "<h5 style='padding-right:5px; padding-left: 5px;'>numero_pedido:</h5>"
    html += "<input id='numero_pedido"+cont+"' name='numero_pedido' class='itenadd'>";
    html += "<h5 style='padding-right:5px; padding-left: 5px;'>Codigo do produto:</h5>"
    html += "<input id='cod_prod"+cont+"' name='cod_prod' class='itenadd'>";
    html += "<h5 style='padding-right:11px; padding-left: 5px;'>Descrição:</h5>"
    html += "<input id='descricao"+cont+"' name='descricao' class='itenadd'>";
    html += "<h5 style='padding-right:10px; padding-left: 5px;'>Embalagem:</h5>"
    html += "<input id='embalagem"+cont+"' name='embalagem' class='itenadd'>";
    html += "<h5 style='padding-right:16px; padding-left: 5px;'>Departamento:</h5>"
    html += "<input id='departamento"+cont+"' name='departamento' class='itenadd'>";
    html += "<h5 style='padding-right:64px; padding-left: 5px;'>QTD Unitaria:</h5>"
    html += "<input id='QTD_unitaria"+cont+"' name='QTD_unitaria' class='itenadd'>";
    html += "<h5 style='padding-right:5px; padding-left: 5px;'>QTD Caixa:</h5>"
    html += "<input id='QTD_caixa"+cont+"' name='QTD_caixa' class='itenadd'>";
    html += "<h5 style='padding-right:5px; padding-left: 5px;'>QTD_pedida:</h5>"
    html += "<input id='QTD_pedida"+cont+"' name='QTD_pedida' class='itenadd'>";
    html += "</div>";
    html+="<div id='adiciona_itens"+cont+"' style='padding-top: 10px;'> "
    html +="</div>"
    if (cont > 0){
        cont_id=cont-1
        id="adiciona_itens"+cont_id
        document.getElementById(id).innerHTML=html
        cont=cont+1
    }
    else{
        document.getElementById("adiciona_itens").innerHTML=html
        cont=cont+1
    }
    htmlcont=""
    htmlcont+="<input id='cont' name='cont' type='hidden' value='"+cont+"'>"
    document.getElementById("cont").innerHTML=htmlcont

}
function atualizarCargas(){
    window.location.reload();
}