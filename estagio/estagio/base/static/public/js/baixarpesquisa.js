/**
 * Created by david on 08/06/17.
 */
 vetorSelecionados = [];
 vetorDados =[];
var seleciona = function (elem)
{
    vetorSelecionados[elem.id]=elem.value;
    console.log(vetorSelecionados[elem.id]);
};

var compactaPesquisa = function (elem)
{
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