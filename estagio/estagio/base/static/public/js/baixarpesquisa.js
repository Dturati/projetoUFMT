/**
 * Created by david on 08/06/17.
 */
// console.log($.cookie("botaoPesquisa"));
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

vetorSelecionados = [];

var seleciona = function (elem)
{

    if($(elem).data("status") === 'ativado')
    {
        $(elem).data("status",'desativado');
        // delete vetorSelecionados[parseInt(elem.id)];
        vetorSelecionados.splice([parseInt(elem.id)]);
        return;
    }
    if($(elem).data("status") === 'desativado')
    {
        $(elem).data("status",'ativado');
        vetorSelecionados[elem.id]=elem.value;
        return;
    }

};


var baixaPesquisa = function (id,chave) {
  window.open('ajax/baixar_pesquisa/?chave='+chave);
};

var define_sessao = function (e) {
     $.ajax({
                type: "GET",
                url: '/ajax/define_sessao/',
                data : {
                    'status':e.value
                },
                success: function (data)
                {

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
    return true;
};

var compactaPesquisa = function (elem,chave)
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
         console.log(vetorDados);

        $.ajax({
            type: "GET",
            url: '/ajax/compacta_pesquisa/',
            data : {
                'data':vetorDados
            },
            success: function (data)
            {
                // console.log(data);
                // verifica_arquivo_individual(data['id'],data['chave']);
                 baixaPesquisa(data['id'],data['chave']);
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
        }
  });

};


var verifica_arquivo_individual = function (id,chave) {
     $.ajax({
                type: "GET",
                url: '/ajax/resultado/',
                data : {
                    'id':id
                },
                success: function (data)
                {
                         baixaPesquisa(id,chave);

                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log(xhr.status);
                    console.log(thrownError);
                }
          });
};
