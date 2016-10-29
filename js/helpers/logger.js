export class Logger {
  constructor(elementId) {
    this.elementId = elementId;
  }

  log(msg) {
    $("#${this.elementId}").append(msg + "\n");
  }

  clear() {
    $("#${this.elementId}").text("");
  }

  requestSuccess(response) {
    this.log("status: ${response.status}; message: ${response.data}");
  }

  requestError(xhr, status) {
    var msg = "status: ${status}; code: ${xhr.status}";
    if(xhr && xhr.responseJSON && xhr.responseJSON.data) {
      msg = msg + "; message: ${xhr.responseJSON.data}";
    }
    this.log(msg);
  }
}
