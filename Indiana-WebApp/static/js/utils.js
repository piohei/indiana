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
