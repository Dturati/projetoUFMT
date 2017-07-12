/**
 * Created by david on 12/07/17.
 */

var socket = new WebSocket("ws://localhost:8080/123");

socket.onopen = function () {
  console.log('Conexão aberta');
  socket.send('ping');
};

socket.onmessage = function (message) {
    console.log('New message:' + message.data);
    if(message.data == 'ping')
    {
      socket.send('pong');
    }
};
