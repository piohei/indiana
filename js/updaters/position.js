import {Logger} from './../helpers/logger'

export class PositionUpdater {
    constructor(host, port) {
        this.dataUrl = `ws://${host}:${port}/ws/position`;
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
    };

    ws.onmessage = function(evt) {
        var received = evt.data.split(":");
        var mac = received[0].replace(/_/g, ":");
        var location = received.slice(1).map( function (v) { return parseFloat(v) } );
        window.currentPositions[mac] = {x: location[0], y: location[1], z: location[2]};
        console.log(`New postiion of ${mac} =`, window.currentPositions[mac]);
    };

    return ws;
}
