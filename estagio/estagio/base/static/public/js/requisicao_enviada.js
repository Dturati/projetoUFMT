// console.log($.cookie("botaoPesquisa"));
$("#id_task").text = "-";
$("#status_task").text = "-";
var host = window.location.hostname;

var compactaTodaPesquisa = function (objeto)
{
  
    $("#btnIniciar").attr("disabled","disabled");
      $.ajax({
            type: "GET",
            url: '/ajax/compacta_toda_pesquisa/',
            data : {

            },
            success: function (data)
            {
                
                fila();
                console.log(data.id);
                $("#id_task").text(data.id);
                console.log(data);
                

            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
      });

};

var baixaPesquisa = function (chave) {
    window.open('baixar_pesquisa/?chave='+chave);
};


var fila = function () {

 $.ajax({
                type: "GET",
                url: 'ajax/fila_celery',
                data : {},
                success: function (data)
                {
                    console.log('fila celery')
                    var objeto = data['total_tasks'];
                    console.log(objeto);
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
