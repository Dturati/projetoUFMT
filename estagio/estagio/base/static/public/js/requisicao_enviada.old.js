// console.log($.cookie("botaoPesquisa"));
$("#id_task").text = "-";
$("#status_task").text = "-";

var compactaTodaPesquisa = function (objeto)
{

    $("#btnIniciar").attr("disabled","disabled");
    $("#idCancelar").removeAttr("disabled");    
      $.ajax({
            type: "GET",
            url: '/ajax/compacta_toda_pesquisa/',
            data : {
                'email':''
            },
            success: function (data)
            {
               status_celery_task(data);
               interval = setInterval(function () {
                      verifica_arquivo(data['id'],data['chave']);
                      fila();
                },1000);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
      });

};

var verifica_arquivo = function (id,chave)
{
    $.cookie("task_id",id);
     $.ajax({
                type: "GET",
                url: '/ajax/resultado/',
                data : {
                    'id':id
                },
                success: function (data)
                {
                    if(data['status'] == 'SUCCESS'){
                        clearInterval(interval);
                        baixaPesquisa(id,chave);
                    }
                    if(data['status'] == 'REVOKED')
                    {
                        clearInterval(interval);
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};
var baixaPesquisa = function (id,chave) {
  window.open('baixar_pesquisa/?chave='+chave);
};

var status_celery_task = function (dados) {
     $.ajax({
                type: "GET",
                url: 'ajax/status_stak_celery/',
                data : {
                    'id': dados.id
                },
                success: function (data)
                {
                    $("#id_task").text(data['id']);
                    $("#idCancelar").val(data['id']);

                    if(data.tasks['state']== 'SUCCESS')
                    {
                         $("#status_task").text("Sua requisição foi processada");
                         $("#id_task").text("");
                         $("#idCancelar").val("");
                    }

                    if(data.tasks['state']== 'PENDING')
                    {
                        $("#status_task").text("Sua requisição foi agendada e está na fila de processamento");
                    }

                    if(data.tasks['state']== 'RECEIVED')
                    {
                        $("#status_task").text("Na fila de processamento");
                    }

                    if(data.tasks['state']== 'STARTED')
                    {
                        $("#status_task").text("Sua requisição está sendo processada");
                    }
                    if(data.tasks['state']== 'REVOKED')
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

var status_celery_task_para_cacelamento_ao_atualizar_pagina = function (dados) {
    $.cookie("task_id","-");
    $.ajax({
                type: "GET",
                url: 'ajax/status_stak_celery/',
                data : {
                    'id': dados['id']
                },
                success: function (data)
                {
                    $("#id_task").text("");
                    $("#idCancelar").val("");
                    if(data.tasks['state'] === 'PENDING' || data.tasks['state'] === 'STARTED')
                    {
                        cancelar_requisicao({'value':data['id']});
                        fila();
                    }

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};

var cancelar_requisicao = function (objeto)
{
    $("#btnIniciar").attr("disabled","disabled");
    $("#idCancelar").attr("disabled","disabled");
     $.ajax({
                type: "GET",
                url: '/ajax/cancelar_requisicao',
                data : {
                    'id':objeto.value
                },
                success: function (data)
                {
                    dados = {
                        'id' : objeto.value
                    };
                    status_celery_task(dados);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};

//Verifica toda a fila do celery
var fila = function () {
 $.ajax({
                type: "GET",
                url: 'ajax/fila_celery',
                data : {},
                success: function (data)
                {
                    // console.log(data['total_tasks']);
                    var objeto = data['total_tasks'];
                    var html = "";
                    var cont = 1;
                    for(var key in objeto)
                    {
                        if((objeto[key].state !== "REVOKED") && (objeto[key].state !== "SUCCESS"))
                        {
                            html += "<tr>";
                            html += '<td>' + cont;
                            html += '</td>';
                            if (key === $("#id_task").text()) {
                                html += "<td " + "style=" + "'color:red'" + ">" + key + "</td>";
                            } else {
                                html += "<td " + "style="+"'color:blue'" + ">" + key + "</td>";
                            }
                            html += "<td>" + objeto[key].state + "</td>";
                            html += "</tr>";
                            cont++;
                        }

                    }
                    $("#fila").html(html);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};


var dados=[];
dados['id'] = $.cookie("task_id");
if(dados['id'] !== "-")
{
    status_celery_task_para_cacelamento_ao_atualizar_pagina(dados);
    $("#id_task").text = "-";
    $("#status_task").text = "-";
}

fila();


