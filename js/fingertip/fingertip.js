import {CORS} from './../helpers/cors'
import {Logger} from './../helpers/logger'

export class Fingertip {
  constructor(host, port, elementId) {
    switch(port) {
      case 80:
        this.url = `http://${host}`;
        break;
      case 443:
        this.url = `https://${host}`;
        break;
      default:
        this.url = `http://${host}:${port}`;
    }
    this.elementId = elementId;

    this.dataUrl = `${this.url}/actual_location`;
    this.statusUrl = `ws://${host}:${port}/status`;

    this.cors = new CORS();
    this.logger = new Logger("result");
  }

  post() {
    var data = _getData(this);

    if(data != null) {
      var self = this; // closure copy
      this.cors.post({
        url: self.dataUrl,
        data: data,
        onSuccess: function(evt) { self.logger.requestSuccess(evt); },
        onError: function(xhr, err) { self.logger.requestError(xhr, err); },
      });
    }
  }

  delete() {
    var self = this; // closure copy
    this.cors.delete({
      url: self.dataUrl,
      onSuccess: function(evt) { self.logger.requestSuccess(evt); },
      onError: function(xhr, err) { self.logger.requestError(xhr, err); },
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
    var data = _getData(this);

    if(data != null) {
      window.currentPosition = data.location;
    }
  }
}

function _getData(_this) {
  var data = { location: {} };

  try {
    data.location.x = _toNumber($(`#${_this.elementId} #x`).val());
    data.location.y = _toNumber($(`#${_this.elementId} #y`).val());
    data.location.z = _toNumber($(`#${_this.elementId} #z`).val());

    data.mac = _toUpperCaseMAC($(`#${_this.elementId} #mac`).val());
  } catch (err) {
    _this.logger.log(err);
    return null;
  }

  return data;
}

function _createWebSocket(_this) {
  var ws = new WebSocket(_this.statusUrl);

  var elementId = _this.elementId; // closure copy
  ws.onopen = function(evt) {
    $(`#${elementId} #end_status_btn`).prop("disabled", false);
    $(`#${elementId} #status_btn`).prop("disabled", true);
  };

  ws.onmessage = function(evt) {
    _this.logger.log(evt.data);
  };

  ws.onclose = function(evt) {
    $(`#${elementId} #end_status_btn`).prop("disabled", true);
    $(`#${elementId} #status_btn`).prop("disabled", false);
  };

  return ws;
}


function _toNumber(x) {
  var n = Number(x);
  if (isNaN(n)) {
    throw `not a number ${x}`;
  }
  return n;
}

function _toUpperCaseMAC(rawMAC) {
  if(!/^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/.test(rawMAC)) {
    throw `invalid MAC: ${rawMAC}`;
  }

  return rawMAC.toUpperCase();
}
