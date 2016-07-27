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

    function postFingertip() {
        console.log("post");
        var request = {};
        try {
            request.x = toNumber($("#x").val());
            request.y = toNumber($("#y").val());
            request.z = toNumber($("#z").val());
            request.mac = validateMAC($("#mac").val());
        } catch (err) {
            $("#result").append(err + "\n");
            return;
        }

        $.ajax({
            url: "http://" + window.location.hostname + ":8887/actual_location",
            type: "POST",
            crossDomain: true,
            data: JSON.stringify(request),
            contentType : 'application/json',
            success: function (response) {
                $("#result").append("status: " + response.status + "; message: " + response.data + "\n");
                $("#delete_btn").prop("disabled", false);
            },
            error: function (xhr, status) {
                var span = $("#result");
                span.append("status: " + status + "; code: " + xhr.status);
                if (xhr && xhr.responseJSON && xhr.responseJSON.data) {
                    span.append("; message: " + xhr.responseJSON.data);
                }
                span.append("\n");


            }
        });

    }
    var init = function(){
        $("#delete_btn").prop("disabled", true);
        $("#end_status_btn").prop("disabled", true);
    };


    return {
        init: init,
        postFingertip: postFingertip
    }
})();