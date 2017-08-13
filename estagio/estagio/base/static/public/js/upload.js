/**
 * Created by david on 08/08/17.
 */
ws = new WebSocket("ws://localhost:8081/ws");
var upload = function (ws)
{

    ws.onopen = function () {
        console.log("Abriu uma conexão");
    }
};
upload(ws);

var sendWebSocket = function () {
    console.log("Teste");
    ws.send(JSON.stringify({"upload":"iniciou"}));

    ws.onmessage = function (message) {
        console.log(message.data);
    }
};

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
