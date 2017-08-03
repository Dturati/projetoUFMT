    /**
     * Created by david on 12/07/17.
     */

var ws = new WebSocket('ws://localhost:8080/echo');

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

