export class CORS {
  constructor() {
  }

  post(params) {
    _doRequest("POST", params);
  }

  delete(params) {
    _doRequest("DELETE", params);
  }
}

// Private functions
function _doRequest(type, params) {
  var request = {
    url: params.url,
    type: type,
    crossDomain: true,
    contentType: 'application/json',
    success: params.onSuccess,
    error: params.onError
  };
  if(params.data) {
    request.data = JSON.stringify(params.data);
  }
  $.ajax(request);
}
