    /**
     * Created by david on 12/07/17.
     */
var host = window.location.hostname;

var ws = new WebSocket('ws://'+host+':8080/echo');

ws.onopen = function () {

};

ws.onmessage = function (message) {

if(message.data == 'OK')
{
  ws.send('pong');
  alert("aqui");
}
console.log('New message:' + message.data);
};

