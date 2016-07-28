"use strict";

var FINGERTIP = (function(){

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

    const HOST = window.location.hostname + ":8887/";
    const BASE_HTTP_URL = "http://" + HOST;
    const ACTUAL_LOCATION_URL = BASE_HTTP_URL + "actual_location";
    const STATUS_URL = "ws://" + HOST + "status";

    function postFingertip() {
        var request = {};
        try {
            request.x = toNumber($("#x").val());
            request.y = toNumber($("#y").val());
            request.z = toNumber($("#z").val());
            request.mac = toUpperCaseMAC($("#mac").val());
        } catch (err) {
            log(err);
            return;
        }
        CORS.post({
            url: ACTUAL_LOCATION_URL,
            data: request,
            onSuccess: logSuccess,
            onError: logError
        });

    }

    function deleteFingertip() {
        CORS.delete({
            url: ACTUAL_LOCATION_URL,
            onSuccess: logSuccess,
            onError: logError
        });
    }

    function getStatus() {
        var ws = new WebSocket(STATUS_URL);
        FINGERTIP.statusWebSocket = ws;
        ws.onopen = function(evt) {
            $("#end_status_btn").prop("disabled", false);
            $("#status_btn").prop("disabled", true);
        };
        ws.onmessage = function (evt) {
            log(evt.data);
        };
        ws.onclose = function(evt) {
            $("#end_status_btn").prop("disabled", true);
            $("#status_btn").prop("disabled", false);
        };

    }

    function endStatus() {
        if (FINGERTIP.statusWebSocket) {
            FINGERTIP.statusWebSocket.close()
        }
    }

    return {
        postFingertip: postFingertip,
        deleteFingertip: deleteFingertip,
        getStatus: getStatus,
        endStatus: endStatus
    }
})();