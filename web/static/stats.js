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
        return chart;
    });

    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label; })
            .y(function(d) { return d.value; })
            .showYAxis(false)
            .color(function(d, i) { return "#000"; })
            .tooltips(false)
            ;
        var length_data = [{
            key: "Game length",
            values: [],
        }];
        for (var i = 0; i < play_stats.game_lengths.length; i++) {
            gl = play_stats.game_lengths[i];
            length_data[0].values.push({
                label: gl[0],
                value: gl[1],
            });
        }
        console.log(length_data)
        d3.select("#moves").datum(length_data).call(chart);
        return chart;
    });
});
