"use strict";

function toNumber(x) {
    var n = Number(x);
    if (isNaN(n)) {
        throw "not a number " + x;
    }
    return n;
}

var MAC_FORMAT = /^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/;

function toUpperCaseMAC(s) {
    if (!MAC_FORMAT.test(s)) {
        throw "invalid MAC: " + s;
    }
    return s.toUpperCase()
}

function log(msg) {
    $("#result").append(msg + "\n");
}

function logSuccess(response) {
    log("status: " + response.status + "; message: " + response.data);
}

function logError(xhr, status) {
    var msg = "status: " + status + "; code: " + xhr.status;
    if (xhr && xhr.responseJSON && xhr.responseJSON.data) {
        msg = msg +"; message: " + xhr.responseJSON.data
    }
    log(msg);
}

function clearLog() {
    $("#result").text("");
}

var CORS = (function(){
    var CORS = {};

    function doRequest(params, type) {
        var request = {
            url: params.url,
            type: type,
            crossDomain: true,
            contentType : 'application/json',
            success: params.onSuccess,
            error: params.onError
        };
        if (params.data) {
            request.data = JSON.stringify(params.data)
        }
        $.ajax(request);
    }

    CORS.post = function(params) {
        doRequest(params, "POST")
    };

    CORS.delete = function(params) {
        doRequest(params, "DELETE")
    };

    return CORS;
})();
