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

if(getCookie("btnPesquisa") === "todos_os_arquivos")
{
    $("#todosOsArquivos").attr('checked', true);
    todosOsArquivos.value = 'ativado';
    document.getElementById("id_porcentagem_um").setAttribute("disabled","disabled");
    document.getElementById("id_porcentagem_dois").setAttribute("disabled","disabled");
    document.getElementById("id_tipoFalha").setAttribute("disabled","disabled");
    document.getElementById("id_tipoFalhaConjunto").setAttribute("disabled","disabled");
    document.getElementById("id_variavelFalhada").setAttribute("disabled","disabled");
    document.getElementById("id_metodoUtilizado").setAttribute("disabled","disabled");
}

if(getCookie("btnPesquisa") === "" || getCookie("btnPesquisa") == undefined)
{
    $("#todosOsArquivos").attr('checked', true);
    todosOsArquivos.value = 'ativado';
    document.getElementById("id_porcentagem_um").setAttribute("disabled","disabled");
    document.getElementById("id_porcentagem_dois").setAttribute("disabled","disabled");
    document.getElementById("id_tipoFalha").setAttribute("disabled","disabled");
    document.getElementById("id_tipoFalhaConjunto").setAttribute("disabled","disabled");
    document.getElementById("id_variavelFalhada").setAttribute("disabled","disabled");
    document.getElementById("id_metodoUtilizado").setAttribute("disabled","disabled");
}


if(getCookie("btnPesquisa") === "individual")
{
    $("#todosOsArquivos").attr('checked', true);
    $("#todosOsArquivos").attr('checked', false);
    todosOsArquivos.value = 'desativado';
    document.getElementById("id_porcentagem_um").removeAttribute("disabled");
    document.getElementById("id_porcentagem_dois").removeAttribute("disabled");
    document.getElementById("id_tipoFalha").removeAttribute("disabled");
    document.getElementById("id_tipoFalhaConjunto").removeAttribute("disabled");
    document.getElementById("id_variavelFalhada").removeAttribute("disabled");
    document.getElementById("id_metodoUtilizado").removeAttribute("disabled");
}

vetorSelecionados = [];
var criaBotaoDownload = function ()
{
    var teste = vetorSelecionados.filter(function (item) {
        return item != null;
    });
    if(teste)
     {
         $("#idBaixarPesquisa").css('display','block');
        var html = '' +
            '<a class=" btn btn-info" style="cursor:pointer" data-dir="/arquivos" onclick="compactaPesquisa(this)" data-toggle="collapse" id="abreUm" data-target="#abre1">Baixar</a>';
        $("#idBaixarPesquisa").html(html);

     }

     if(teste.length == 0)
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


var baixaPesquisa = function (id,chave) {
  window.open('ajax/baixar_pesquisa/?chave='+chave);
};

var pesquiarTodosOsArquivos = function (e)
{

    //Alterar a barra de endereço para não dar pau na paginação
    window.history.pushState("object or string", "Title", "/home/");
    var todosOsArquivos = document.getElementById("todosOsArquivos");
    todosOsArquivos.setAttribute('data-status','ativado');
    define_sessao(e);
    if(todosOsArquivos.value == 'desativado')
    {
        document.cookie = "btnPesquisa = todos_os_arquivos";
        console.log(getCookie("btnPesquisa"));
        todosOsArquivos.value = 'ativado';
        document.getElementById("id_porcentagem_um").setAttribute("disabled","disabled");
        document.getElementById("id_porcentagem_dois").setAttribute("disabled","disabled");
        document.getElementById("id_tipoFalha").setAttribute("disabled","disabled");
        document.getElementById("id_tipoFalhaConjunto").setAttribute("disabled","disabled");
        document.getElementById("id_variavelFalhada").setAttribute("disabled","disabled");
        document.getElementById("id_metodoUtilizado").setAttribute("disabled","disabled");
    }else{
        document.cookie = "btnPesquisa = individual";
        console.log(getCookie("btnPesquisa"));
        todosOsArquivos.value = 'desativado';
        document.getElementById("id_porcentagem_um").removeAttribute("disabled");
        document.getElementById("id_porcentagem_dois").removeAttribute("disabled");
        document.getElementById("id_tipoFalha").removeAttribute("disabled");
        document.getElementById("id_tipoFalhaConjunto").removeAttribute("disabled");
        document.getElementById("id_variavelFalhada").removeAttribute("disabled");
        document.getElementById("id_metodoUtilizado").removeAttribute("disabled");
    }
    // todosOsArquivos.value = "TODOS_OS_ARQUIVOS";

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
