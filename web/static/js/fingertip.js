"use strict";

var FINGERTIP = (function(){

    const HOST = window.location.hostname + ":8887/";
    const BASE_HTTP_URL = "http://" + HOST;
    const ACTUAL_LOCATION_URL = BASE_HTTP_URL + "actual_location";
    const STATUS_URL = "ws://" + HOST + "status";

    function postFingertip() {
        var request = {location:{}};
        try {
            request.location.x = toNumber($("#x").val());
            request.location.y = toNumber($("#y").val());
            request.location.z = toNumber($("#z").val());
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

    function clearLog() {
        $("#result").text("");
    }

    return {
        postFingertip: postFingertip,
        deleteFingertip: deleteFingertip,
        getStatus: getStatus,
        endStatus: endStatus,
        clearLog: clearLog
    }
})();