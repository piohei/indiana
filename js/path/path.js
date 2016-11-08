import {CORS} from './../helpers/cors'
import {Logger} from './../helpers/logger'

export class Path {
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

    this.dataUrl = `${this.url}/path`;

    this.cors = new CORS();
    this.logger = new Logger("result");
  }

  startRecording() {
    var data = _getData(this);

    if(data != null) {
      var self = this; // closure copy
      this.cors.post({
        url: self.dataUrl,
        data: data,
        onSuccess: function(evt) { self.logger.requestSuccess(evt); },
        onError: function(xhr, err) { self.logger.requestError(xhr, err); }
      });
    }
  }

  stopRecording() {
    var self = this; // closure copy
    this.cors.delete({
      url: self.dataUrl,
      onSuccess: function(evt) { self.logger.requestSuccess(evt); },
      onError: function(xhr, err) { self.logger.requestError(xhr, err); }
    });
  }

  clearLog() {
    this.logger.clear();
  }
}

function _getData(_this) {
  var data = {};

  try {
    data.name = $(`#${_this.elementId} #name`).val();
    data.mac = _toUpperCaseMAC($(`#${_this.elementId} #mac`).val());
  } catch (err) {
    _this.logger.log(err);
    return null;
  }

  return data;
}

function _toUpperCaseMAC(rawMAC) {
  if(!/^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/.test(rawMAC)) {
    throw `invalid MAC: ${rawMAC}`;
  }

  return rawMAC.toUpperCase();
}
