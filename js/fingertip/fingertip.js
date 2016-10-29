import {CORS} from './../helpers/cors'
import {Logger} from './../helpers/logger'

export class Fingertip {
  constructor(host, port, elementId) {
    switch(port) {
      case 80:
        this.url = "http://${host}";
        break;
      case 443:
        this.url = "https://${host}";
        break;
      default:
        this.url = "http://${host}:${port}";
    }
    this.elementId = elementId;

    this.dataUrl = "${this.url}/actual_location";
    this.statusUrl = "ws://${host}/status";

    this.cors = new CORS();
    this.logger = new Logger("result");
  }

  post() {
    var data = _getData(this.elementId);

    if(data != null) {
      this.cors.post({
        url: this.dataUrl,
        data: data,
        onSuccess: this.logger.requestSuccess,
        enError: this.logger.requestError,
      });
    }
  }

  delete() {
    this.cors.delete({
      url: this.dataUrl,
      onSuccess: this.logger.requestSuccess,
      onError: this.logger.requestError,
    });
  }

  getStatus() {
    this.ws = _createWebSocket(this);
  }

  endStatus() {
    if(this.ws) {
      this.ws.close();
    }
  }

  clearLog() {
    this.logger.clear();
  }

  reloadLocation() {
    var data = _getData();

    if(data != null) {
      window.location = data.location;
    }
  }
}

function _getData(elementId) {
  var data = { location: {} };

  try {
    request.location.x = _toNumber($("#${elementId} #x").val());
    request.location.y = _toNumber($("#${elementId} #y").val());
    request.location.z = _toNumber($("#${elementId} #z").val());

    request.mac = _toUpperCaseMAC($("#${elementId} #mac").val());
  } catch (err) {
    window.logger.log(err);
    return null;
  }

  return data;
}

function _toNumber(x) {
  var n = Number(x);
  if (isNaN(n)) {
    throw "not a number " + x;
  }
  return n;
}

function _toUpperCaseMAC(rawMAC) {
  if(!/^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/.test(rawMAC)) {
    throw "invalid MAC: ${rawMAC}";
  }

  return rawMAC.toUpperCase();
}

function _createWebSocket(_this) {
  var ws = new WebSocket(_this.statusUrl);

  var elementId = _this.elementId; // closure copy
  ws.onopen = function(evt) {
    $("#${elementId} #end_status_btn").prop("disabled", false);
    $("#${elementId} #status_btn").prop("disabled", true);
  };

  ws.onmessage = function(evt) {
    this.logger.log(evt.data);
  };

  ws.onclose = function(evt) {
    $("#${elementId} #end_status_btn").prop("disabled", true);
    $("#${elementId} #status_btn").prop("disabled", false);
  }

  return ws;
}
