import {Logger} from './../helpers/logger'

export class PositionUpdater {
  constructor(host, port, mac) {
    this.dataUrl = `ws://${host}:${port}/position/${mac.toLowerCase().replace(/:/g,'-')}`;
    this.logger = new Logger("result");
  }

  run() {
    this.ws = _createWebSocket(this);
  }
}

function _createWebSocket(_this) {
  var ws = new WebSocket(_this.dataUrl);

  ws.onopen = function(evt) {
    ws.send("start");
  }

  ws.onmessage = function(evt) {
    var received = evt.data.split(":").map( function (v) { return parseFloat(v) } );
    window.currentPosition.x = received[0];
    window.currentPosition.y = received[1];
    window.currentPosition.z = received[2];
    console.log("New postiion: ", window.currentPosition);
  };

  return ws;
}
