// creates a node.js based server used to render the incoming firefly data from the POETS engine

const express = require('express');
const app = express();
const WebSocket = require('ws');

// create named pipe for sending messages back to the executive
// var fs = require('fs')
// const wstream = fs.createWriteStream('./to_poets_devices.sock')

// reading from STDIN: https://stackoverflow.com/questions/20086849/how-to-read-from-stdin-line-by-line-in-node
var readline = require('readline');
var r1 = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

// var fs = require('fs');
var path = require('path');

// open our web socket
const wss = new WebSocket.Server({port: 8079});

// send flash to the rendered instance
function update(wss, json) {
    // https://github.com/websockets/ws#simple-server
    wss.clients.forEach(function each(client) {
        if(client !== wss && client.readyState == WebSocket.OPEN) {
            client.send(json);
        }
    });
}

inputChunks = [];
svgSize = [];
lines = [];
// get stdin data which will be passed to the rendered graph
// this will be the output of the executive
r1.on('line', function(line) {
  inputChunks += line;
  if (line == "}") {
    var d = JSON.parse(inputChunks);
    if (d.hasOwnProperty('volume')) {
      svgSize = inputChunks;
    } else if (d.hasOwnProperty('lines')) {
      lines = inputChunks;
    } else {
      update(wss, inputChunks);
    }
    inputChunks = [];
  }
});

wss.on('connection', function() {
  update(wss, svgSize);
  update(wss, lines);
});
// stdin.on('data', function (chunk) {
//     inputChunks += chunk;
//     update(wss, inputChunks);
// });

// stdin.on('end', function () {
//     // console.log("Ended" + inputChunks);
//     var d = JSON.parse(inputChunks);
//     inputChunks = [];
//     console.log(d);
//     update(wss, inputChunks);
// });



app.get('/', (req, res) => res.sendFile(path.join(__dirname+'/index.html')));
// app.get('/data.json', (req, res) => res.sendFile(path.join(__dirname+'/data.json')));

app.listen(3000, () => console.log('listening on port 3000'))

