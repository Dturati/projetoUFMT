// console.log($.cookie("botaoPesquisa"));
$("#id_task").text = "-";
$("#status_task").text = "-";

var atualizaClientes = function () {
 $.ajax({
                type: "GET",
                url: 'http://localhost:8081/update',
                dataType : 'html',
                crossDomain: true,
                success: function (data)
                {

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};

var init = function () {
    var ws = new WebSocket('ws://localhost:8080/echo');
    var wsd = new WebSocket('ws://localhost:8081/ws');
    // var wsd = new WebSocket('ws://localhost:8081/update');
    ws.onopen = function () {
        console.log('Conexão aberta');
    };

    wsd.onopen = function () {
        console.log('Conexão aberta');
    };
     wsd.onmessage = function () {
         setTimeout(function () {
             fila();
         },500);

        console.log('Todo Mundo');
    };


    return ws;
};

var compactaTodaPesquisa = function (objeto,ws)
{
    atualizaClientes();

    $("#btnIniciar").attr("disabled","disabled");
    $("#idCancelar").removeAttr("disabled");    
      $.ajax({
            type: "GET",
            url: '/ajax/compacta_toda_pesquisa/',
            data : {

            },
            success: function (data)
            {
                setTimeout(function () {
                     status_celery_task(data);
                },2000);

                fila();
                console.log(data.id);
                $.cookie("id_task",data.id);
                $.cookie("chave",data.chave);
                console.log(data);
                setTimeout(function () {
                     ws.send(JSON.stringify({chave:data.chave,id:data.id}));
                },500);

                ws.onmessage = function (message) {
                console.log('New message:' + message.data);
                if(message.data == 'SUCCESS')
                {
                    console.log('aqui');
                    console.log(data.chave);
                    setTimeout(function () {
                            baixaPesquisa(data.chave);
                    },1000);

                     setTimeout(function () {
                             status_celery_task(data);
                    },2000);

                }
                ws.onclose = function ()
                {
                    ws.close();
                    console.log('close');
                }
                };

            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
      });

};

var baixaPesquisa = function (chave) {
    window.open('baixar_pesquisa/?chave='+chave);
    $.cookie("id_task","");
    $.cookie("chave","");
};


var cancelar_requisicao = function (objeto)
{

    $("#btnIniciar").attr("disabled","disabled");
    $("#idCancelar").attr("disabled","disabled");

     $.ajax({
                type: "GET",
                url: '/ajax/cancelar_requisicao',
                data : {
                    'id': $.cookie("id_task"),
                    'chave':$.cookie("chave")
                },
                success: function (data)
                {
                    dados = {
                        'id' : objeto.value,
                        'chave' : $.cookie("chave")
                    };
                    setTimeout(function () {
                        status_celery_task(dados);
                    },2000);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });

      atualizaClientes();
      $.cookie("id_task","");
      $.cookie("chave","");
};

var status_celery_task = function (dados) {
     $.ajax({
                type: "GET",
                url: 'ajax/status_stak_celery/',
                data : {
                    'id': dados['id']
                },
                success: function (data)
                {
                    $("#id_task").text(data['id']);
                    $("#idCancelar").val(data['id']);

                    if(data.tasks['state'] == 'SUCCESS')
                    {
                         $("#status_task").text("Sua requisição foi processada");
                         $("#id_task").text("");
                         $("#idCancelar").val("");
                    }

                    if(data.tasks['state'] == 'PENDING')
                    {
                        $("#status_task").text("Sua requisição foi agendada e está na fila de processamento");
                    }

                    if(data.tasks['state'] == 'RECEIVED')
                    {
                        $("#status_task").text("Na fila de processamento");
                    }

                    if(data.tasks['state'] == 'STARTED')
                    {
                        $("#status_task").text("Sua requisição está sendo processada");
                    }
                    if(data.tasks['state'] == 'REVOKED')
                    {
                        $("#status_task").text("Sua requisição foi cancelada");
                        $("#id_task").text("-");
                        $("#idCancelar").val("-");
                    }
                    var objeto = data['total_tasks'];
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }

          });
        fila();
};

var fila = function () {
 $.ajax({
                type: "GET",
                url: 'ajax/fila_celery',
                data : {},
                success: function (data)
                {
                    var objeto = data['total_tasks'];
                    var html = "";
                    var cont = 1;
                    var status = "";
                    for(var key in objeto)
                    {
                        if((objeto[key].state != "REVOKED") && (objeto[key].state != "FAILURE") && (objeto[key].state != "SUCCESS"))
                        {
                            if(objeto[key].state == "REVOKED")
                            {
                                status = "Cancelado";
                            }
                            if(objeto[key].state == "SUCCESS")
                            {
                                status = "Sucesso";
                            }
                            if(objeto[key].state == "STARTED")
                            {
                                status = "Iniciado";
                            }
                             if(objeto[key].state == "RECEIVED")
                            {
                                status = "Na fila";
                            }
                            html += "<tr>";
                            html += '<td>' + cont;
                            html += '</td>';
                            if (key === $("#id_task").text()) {
                                html += "<td " + "style=" + "'color:red'" + ">" + key + "</td>";
                            } else {
                                html += "<td " + "style="+"'color:blue'" + ">" + key + "</td>";
                            }
                            html += "<td>" + status+ "</td>";
                            html += "</tr>";
                            cont++;
                        }

                        cont++;

                    }
                    $("#fila").html(html);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};

if(
    $.cookie("id_task") != ""
    && $.cookie("id_task") != undefined
    && $.cookie("chave") != ""
    && $.cookie("chave") != undefined)
{
    var dados = [];
    dados['value'] = $.cookie("id_task");
    dados['chave'] = $.cookie("chave");
    cancelar_requisicao(dados);
}

$.cookie("id_task","");
$.cookie("chave","");