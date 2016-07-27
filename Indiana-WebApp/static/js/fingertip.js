"use strict";

var FINGERTIP = (function(){
    function toNumber(x) {
        var n = Number(x);
        if (isNaN(n)) {
            throw "not a number " + x;
        }
        return n;
    }

    function validateMAC(s) {
        var format = /^([a-fA-F0-9]{2}:){5}([a-fA-F0-9]{2})$/;
        if (!format.test(s)) {
            throw "invalid MAC: " + s;
        }
    }

    function log(msg) {
        $("#result").append(msg + "\n");
    }

    function postFingertip() {
        var request = {};
        try {
            request.x = toNumber($("#x").val());
            request.y = toNumber($("#y").val());
            request.z = toNumber($("#z").val());
            request.mac = validateMAC($("#mac").val());
        } catch (err) {
            log(err);
            return;
        }

        $.ajax({
            url: "http://localhost:8887/actual_location",
            type: "POST",
            crossDomain: true,
            data: JSON.stringify(request),
            contentType : 'application/json',
            success: function (response) {
                log("status: " + response.status + "; message: " + response.data);
                $("#delete_btn").prop("disabled", false);
            },
            error: function (xhr, status) {
                var msg = "status: " + status + "; code: " + xhr.status;
                if (xhr && xhr.responseJSON && xhr.responseJSON.data) {
                    msg = msg +"; message: " + xhr.responseJSON.data
                }
                log(msg);
            }
        });

    }

    function deleteFingertip() {
        $.ajax({
            url: "http://localhost:8887/actual_location",
            type: "DELETE",
            crossDomain: true,
            success: function (response) {
                log("status: " + response.status + "; message: " + response.data);
                $("#delete_btn").prop("disabled", true);
            },
            error: function (xhr, status) {
                var msg = "status: " + status + "; code: " + xhr.status;
                if (xhr && xhr.responseJSON && xhr.responseJSON.data) {
                    msg = msg +"; message: " + xhr.responseJSON.data
                }
                log(msg);
            }
        });

    }

    function getStatus() {
        var ws = new WebSocket("ws://localhost:8887/status");
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


    var init = function(){
        $("#delete_btn").prop("disabled", true);
        $("#end_status_btn").prop("disabled", true);
    };


    return {
        init: init,
        postFingertip: postFingertip,
        deleteFingertip: deleteFingertip,
        getStatus: getStatus,
        endStatus: endStatus
    }
})();