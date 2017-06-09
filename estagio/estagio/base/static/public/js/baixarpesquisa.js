/**
 * Created by david on 08/06/17.
 */
 vetorSelecionados = [];
var criaBotaoDownload = function () {

    if(vetorSelecionados.length > 0)
     {
         $("#idBaixarPesquisa").css('display','block');
        var html = '' +
            '<a class="glyphicon glyphicon-folder-open" style="cursor:pointer" data-dir="/arquivos" onclick="compactaPesquisa(this)" data-toggle="collapse" id="abreUm" data-target="#abre1">Baixar Pesquisa</a>';
        $("#idBaixarPesquisa").html(html);

     }

     if(vetorSelecionados.length == 1)
     {
         $("#idBaixarPesquisa").css('display','none');
     }
};



var seleciona = function (elem)
{

    if($(elem).data("status") === 'ativado')
    {
        $(elem).data("status",'desativado');
        // delete vetorSelecionados[parseInt(elem.id)];
        vetorSelecionados.splice([parseInt(elem.id)]);
        console.log(vetorSelecionados);
        criaBotaoDownload();
        return;
    }
    if($(elem).data("status") === 'desativado')
    {
        $(elem).data("status",'ativado');
        vetorSelecionados[elem.id]=elem.value;
        criaBotaoDownload();
        return;
    }

};

var compactaPesquisa = function (elem)
{

         if(vetorSelecionados.length == 0)
         {
             return;
         }
         vetorDados = [];
         vetorSelecionados.forEach(function (item)
         {
            vetorDados.push(item);
         });

          $.ajax({
                type: "GET",
                url: '/ajax/compacta_pesquisa/',
                data : {
                    'data':vetorDados
                },
                success: function (data)
                {
                    baixaPesquisa();
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });

};
var baixaPesquisa = function () {
  window.open('ajax/baixar_pesquisa/');
};