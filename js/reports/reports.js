export class Reports {

    constructor() {
        this.dataUrl = '/api/reports';
    }

    fetch(elementId) {
        var container = $(`#${elementId}`);
        $.getJSON(this.dataUrl).done(function (reports) {
            console.log(reports);
            for (const index in reports) {
                container.append(_toHTML(index, reports[index]));
            }
        }).fail(function () {
            alert("Error while getting reports!");
        });
    }
}

function _toHTML(index, report) {
    var number = Number(index) + 1;
    return `<div class="clearfix">
        <div class="col-md-2">&nbsp;</div>
        <div class="col-md-4">
            <div class="centered">
            <h2>Report ${number}</h2>
            <h3>Engine configuration:</h3>
            <pre>${JSON.stringify(report.engine_config, null, 4)}</pre>
            </div>
        </div>
        <div class="col-md-4">
            <div class="centered">
            <h3>Stats</h3>
            Average error: ${report.global_stats.avg_error} <br/>
            Minimal error: ${report.global_stats.min_error} <br/>
            Maximal error: ${report.global_stats.max_error} <br/>
            Errors standard deviation: ${report.global_stats.std_error}
            <br/><br/>
            See full results map <a href="/report/${index}">here</a>
            </div>
        </div>
        <div class="col-md-2">&nbsp;</div>
    </div><hr/>`
}