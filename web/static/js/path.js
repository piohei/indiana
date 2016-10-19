var PATH = (function(){

    const HOST = window.location.hostname + ":8887/";
    const BASE_HTTP_URL = "http://" + HOST;
    const PATH_URL = BASE_HTTP_URL + "path";

    function startRecording() {
        var request = {};
        try {
            request.name = $("#name").val();
            request.mac = toUpperCaseMAC($("#mac").val());
        } catch (err) {
            log(err);
            return;
        }
        CORS.post({
            url: PATH_URL,
            data: request,
            onSuccess: logSuccess,
            onError: logError
        });

    }

    function stopRecording() {
        CORS.delete({
            url: PATH_URL,
            onSuccess: logSuccess,
            onError: logError
        });
    }

    return {
        startRecording: startRecording,
        stopRecording: stopRecording
    }
})();