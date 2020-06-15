
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var user_received = [];

    //receive details from server
    socket.on('newuser', function(msg) {
        console.log("Received User" + msg.user);
        user_received.push(msg.user);
        user_string = ''
        user_string = user_string + '<p>' + msg.user + '</p>';
        $('#log').html(user_string);
    });

});