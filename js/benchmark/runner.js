import {CORS} from './../helpers/cors'
import {Logger} from './../helpers/logger'

export class Runner {
    constructor(host, port) {
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

        this.dataUrl = `${this.url}/api/benchmark_runner`;

        this.cors = new CORS();
        this.logger = new Logger("result");
    }

    post() {
        var self = this;
        this.cors.post({
            url: self.dataUrl,
            onSuccess: function(evt) { self.logger.requestSuccess(evt); },
            onError: function(xhr, err) { self.logger.requestError(xhr, err); }
        });
    }

    delete() {
        var self = this; // closure copy
        this.cors.delete({
            url: self.dataUrl,
            onSuccess: function(evt) { self.logger.requestSuccess(evt); },
            onError: function(xhr, err) { self.logger.requestError(xhr, err); }
        });
    }

    getStatus() {
        var self = this; // closure copy
        this.cors.get({
            url: self.dataUrl,
            onSuccess: function(evt) { self.logger.requestSuccess(evt); },
            onError: function(xhr, err) { self.logger.requestError(xhr, err); }
        });
    }

    clearLog() {
        this.logger.clear();
    }
}