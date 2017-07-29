    /**
     * Created by david on 12/07/17.
     */

var ws = new WebSocket('ws://localhost:8080/echo');

ws.onopen = function () {
console.log('Conexão aberta');
  ws.send('ping');
};

ws.onmessage = function (message) {
console.log('New message:' + message.data);
if(message.data == 'ping')
{
  ws.send('pong');
}
};

