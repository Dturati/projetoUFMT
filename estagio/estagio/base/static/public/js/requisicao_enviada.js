var compactaTodaPesquisa = function (objeto)
{
    $("#btnIniciar").attr("disabeld","disabled");
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
                      verifica_arquivo(data['id'],data['chave'])
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
                    'id': dados['id']
                },
                success: function (data)
                {
                    $("#id_task").text(data['id']);
                    $("#idCancelar").val(data['id']);
                    if(data.tasks['state']== 'SUCCESS')
                    {
                        $("#status_task").text("Sua requisição foi processada, seus dados estão sendo baixados");
                    }

                    if(data.tasks['state']== 'PENDING')
                    {
                        $("#status_task").text("Sua requisição foi agendada e está na fila de processamento, isso pode demorar um pouco");
                    }

                    if(data.tasks['state']== 'STARTED')
                    {
                        $("#status_task").text("Sua requisição está sendo processada, isso pode demorar um pouco");
                    }
                    if(data.tasks['state']== 'REVOKED')
                    {
                        $("#status_task").text("Sua requisição foi cancelada");
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};

var cancelar_requisicao = function (objeto) {
     $.ajax({
                type: "GET",
                url: '/ajax/cancelar_requisicao',
                data : {
                    'id':objeto.value
                },
                success: function (data)
                {
                    dados = {
                        'id' : $("#idCancelar").val()
                    };

                    status_celery_task(dados);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};


