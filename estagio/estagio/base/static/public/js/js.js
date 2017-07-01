/**
 * Created by david on 24/05/17.
 */
$('#id_numeroSequencial').on('keyup', function ()
{
    var tam = $("#id_numeroSequencial").val();
    tam = tam.replace(/[\.-]/g, "");
    tam = tam.replace(/[\,-]/g, "");
    if(tam > 9999990000)
    {
        $("#c").val('');
        $("#id_numeroSequencial").attr('placeholder','Valor máximo 999.999,0000');
    }
});



var chamaAjax = function (elem)
{
          var caminho =  $(elem).data("dir");
          var html = "";
          var dadosHtml = "";
          $.ajax({
                type: "GET",
                url: '/ajax/lista_diretorios/',
                data :  {
                  'caminho' : caminho
                },
                success: function (data)
                {

                    data.diretorios.forEach(function (dados)
                    {
                        html += '<div'+ ' '+'id='+ dados + ' '+'>';
                            html += "&nbsp;&nbsp";
                            html += '<a'+' ';
                            html += 'class="glyphicon glyphicon-plus-sign"' + 'data-estado='+"fechado" + ' ' + 'onclick="chamaAjax(this)"'  + 'data-dir='+ data.caminho + '/' + dados + ' ' + 'data-toggle="collapse"' + 'data-target=""' + '>' +dados+'</a>';
                            html += "&nbsp;&nbsp;";
                            html += '<div' + ' ' + 'class="collapse"' + '>' + ' ';
                            html +=  + ' '+ '</div>';
                        html += '</div>';
                    });
                    $("#"+$(elem).closest("div").attr("id")).append("<br>"+html);
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });

};

var chamaArquivosAjax = function (elem)
{

            $("#paginacao").fadeOut();
          var caminho =  $(elem).data("dir");
          var html = "";
          var dadosHtml = "";
          var menu = "";

          $.ajax({
                type: "GET",
                url: '/ajax/lista_diretorios/',
                data :  {
                  'caminho' : caminho
                },
                success: function (data)
                {

                     for(i = 0; i <data.diretorios.length; i++)
                    {
                            html += '<tr>';
                            html += '<td>';
                            html += '<a'+' ';
                            html += 'class="glyphicon glyphicon-folder-open"' +'style="cursor:Pointer"' + '' + 'onclick="chamaArquivosAjax(this)"'  + 'data-dir='+ data.caminho + '/' + data.diretorios[i]  + '>' +' '+data.diretorios[i]+'</a>';
                            html += '</td>';
                            html += '<td>';
                            html += data.detalhePastaModificadas[i];
                            html += '</td>';
                            html += '<td>';
                            html += data.detalhePastaCriadas[i];
                            html += '</td>';
                            html += '</tr>';

                    }
                    menu += '<div class="glyphicon glyphicon-arrow-left"></div>';
                    menu += '<a ';
                    menu += 'onclick="chamaArquivosAjax(this)"' + '' + 'style="color:green;cursor:pointer"' + ' ' + 'data-dir=' + data.anterior + ' ' + '/' + ' ';
                    menu += '>';
                    menu += data.caminho;
                    menu += '</a>';
                    menu += "&nbsp;&nbsp;&nbsp;";

                    dadosHtml += "<br>";

                    for(var i = 0; i < data.arquivos.length; i = i+1)
                    {

                        console.log(i);
                         dadosHtml += '<tr>';
                         dadosHtml += '<td>';
                         dadosHtml += '<div'+' ';
                         dadosHtml += 'class="glyphicon glyphicon-file"' + 'style="color:orange;cursor:Pointer"' +' + data-caminho='+data.caminho + '/' +data.arquivos[i]+'>' + '&nbsp;&nbsp' + data.arquivos[i] +"&nbsp;";
                         dadosHtml += '</div>'
                         dadosHtml += '</td>';
                         dadosHtml += '<td>';
                         dadosHtml += data.detalheArquivosModificado[i];
                         dadosHtml += '</td>';
                         dadosHtml += '<td>';
                         dadosHtml += data.detalheArquivosCriados[i];
                         dadosHtml += '</td>';
                         dadosHtml += '<td>';
                         dadosHtml += '<a class = "glyphicon glyphicon-download" ';
                         dadosHtml += ' '+'href=';
                         dadosHtml += "'";
                         dadosHtml += "/home/download/"+"."+data.caminho + '/'+data.arquivos[i];
                         dadosHtml += "'";
                         dadosHtml += ' >';
                         dadosHtml += '</a>';
                         dadosHtml += '</td>';
                         dadosHtml += '<td>';
                         dadosHtml += '<input ';
                         dadosHtml += 'data-status="desativado" ';
                         dadosHtml += 'type="checkbox"';
                         dadosHtml += 'id='+parseInt(i+1);
                         dadosHtml += ' onclick="seleciona(this)"';
                         dadosHtml += ' value='+"."+data.caminho + '/'+data.arquivos[i];
                         dadosHtml += ' >';
                         dadosHtml += '';
                         dadosHtml += '</input>';
                         dadosHtml += '</td>';
                         dadosHtml += '</tr>';


                    }
                    $("#volta_dir").html(menu);

                    $("#tabela").html(html + dadosHtml);


                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};



