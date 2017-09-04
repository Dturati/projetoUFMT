/**
 * Created by david on 08/08/17.
 */

ws = new WebSocket("ws://192.168.15.16:8081/ws");

var upload = function ()
{
    ws.onopen = function () {
        console.log("Abriu uma conexão de upload");
    }

};
upload();

var sendWebSocketEnviaIdTask = function () {
    ws.send(JSON.stringify({"upload":"iniciou","id": $("#id_task_upload").text()}));
    ws.send(JSON.stringify({'id_tarefa':$("#id_task_upload").text()}));
    ws.onmessage = function (message) {
        if(message.data == 'Sucesso')
        {
            $("#bntDownloadArquivos").removeAttr("disabled");
            $("#uploadGrafico").removeAttr("disabled");
        }
    }
};

var sendWebSocket = function ()
{
    console.log("send upload");
    setTimeout(function () {
        sendWebSocketEnviaIdTask();
    },3000);
};

var  cancelaRequisicaoUploadRefresh = function()
{

          console.log('cancela');
          $.ajax({
                type: "GET",
                url: '/ajax/cancela_requisicao_upload/',
                data : {
                    'id' : $("#id_task_upload").text()
                },
                success: function (data) {
                        fila_de_requisicoes_upload();
                },

                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
            });

};



$(window).ready(function () {
    // cancelaRequisicaoUploadRefresh();
});


var fazerUpload = function (e) {

    $.ajax({
        type: "GET",
        url: '/ajax/gerar_grafico/',
        dataType : 'html',
        success: function (data) {
             $('#grafico').html('<img src="data:image/png;base64,' + data + '" />');
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
};

var  cancelaRequisicaoUpload = function(objeto)
{
      $.ajax({
        type: "GET",
        url: '/ajax/cancela_requisicao_upload/',
        data : {
            'id' : objeto.value
        },
        success: function (data) {
                fila_de_requisicoes_upload();
        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
};

var  status_requisicao_upload = function(objeto)
{
       if($("#id_task_upload").text() == undefined || $("#id_task_upload").text() == "")
      {
          return;
      }

      $.ajax({
        type: "GET",
        url: '/ajax/status_requisicao_upload/',
        data : {
            'id' : $("#id_task_upload").text()
        },
        success: function (data) {
            console.log(data);
            if(data.statusTask.state == 'PENDING')
            {
                $("#status_upload").text("Processando");
            }

            if(data.statusTask.state == 'SUCCESS')
            {
                $("#status_upload").text("Pronto");
            }

        },

        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
};

var fila_de_requisicoes_upload = function () {
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
                    $("#fila_de_rquisicoes_upload").html(html);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};

