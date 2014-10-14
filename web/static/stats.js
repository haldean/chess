$(document).ready(function() {
    function color(d, i) {
        var val = d.data[0];
        if (val == "1-0") {
            return "#EEE";
        } else if (val == "0-1") {
            return "#888";
        } else if (val == "1/2-1/2") {
            return "#BBB";
        }
    }
    nv.addGraph(function() {
        var chart = nv.models.pieChart()
            .width(300)
            .height(300)
            .x(function(d) { return d[0]; })
            .y(function(d) { return d[1]; })
            .showLabels(true)
            .showLegend(false)
            .tooltips(false)
            .donut(true)
            .donutRatio(0.4)
            .color(color)
            ;
        d3.select("#victories").datum(victories).call(chart);
    });
});
