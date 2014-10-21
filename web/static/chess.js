function loc_str(rank, file) {
    rank_str = "" + (rank + 1);
    file_str = ["a", "b", "c", "d", "e", "f", "g", "h"][file];
    return file_str + rank_str
}

function file_from_str(str) {
    return str.charCodeAt(0) - "a".charCodeAt(0);
}

function rank_from_str(str) {
    return str[1] - 1;
}

function load_board(b) {
    for (var r = 0; r < 8; r++) {
        for (var f = 0; f < 8; f++) {
            var square_elem = document.getElementById(loc_str(r, f));
            var piece = b[r*8+f];
            if (piece) {
                square_elem.innerHTML = (
                    "<img class='piece' src='/static/" + piece + ".svg' " +
                    "data-piece='" + piece + "' " +
                    "data-color='" + piece[0] + "' " +
                    "data-rank='" + r + "' data-file='" + f + "'>");
            } else {
                square_elem.innerHTML = "";
            }
        }
    }
}

var last_move_start = undefined;
var last_move_rank = undefined;
var last_move_file = undefined;

function start_move(start_elem) {
    reset_move();
    if (start_elem === last_move_start) {
        last_move_start = undefined;
        return;
    }
    last_move_start = start_elem;
    last_move_rank = start_elem.data().rank;
    last_move_file = start_elem.data().file;
    var start_loc = loc_str(last_move_rank, last_move_file);
    for (var r = 0; r < 8; r++) {
        for (var f = 0; f < 8; f++) {
            if (is_accessible(r, f, start_loc)) {
                var square_elem = $("#" + loc_str(r, f));
                square_elem.addClass("selected");
                square_elem.unbind("click").click(function(ev) {
                    reset_move();
                    if ($(ev.target).hasClass("piece")) {
                        ev.target = $(ev.target).parent()[0];
                    }
                    console.log("target", ev.target);
                    var new_r = rank_from_str(ev.target.id);
                    var new_f = file_from_str(ev.target.id);
                    do_move(last_move_rank, last_move_file, new_r, new_f);
                });
            }
        }
    }
}

function reset_move() {
    $(".selected").removeClass("selected");
    $("#board td").unbind("click").click(function() {
        reset_move();
    });
}

function do_move(r, f, new_r, new_f) {
    console.log("do move", r, f, new_r, new_f);
    var start_loc = loc_str(r, f);
    var good = false;
    var move_name = is_accessible(new_r, new_f, start_loc);
    if (!move_name) {
        init_board(current_board);
        return;
    }
    // Make a copy of the old board.
    old_board = [];
    for (var i = 0; i < 64; i++) {
        old_board.push(current_board[i]);
    }
    current_board[new_r * 8 + new_f] = current_board[r * 8 + f];
    current_board[r * 8 + f] = "";
    load_board(current_board);
    $("#alert *").unbind("click");
    $("#alert_move").text(move_name);
    $("#alert button.confirm").click(function() {
        $.post(window.location.pathname,
               { "move": move_name, });
    });
    $("#alert button.cancel").click(function() {
        $("#popup").hide();
        init_board(old_board);
    });
    $("#popup").show();
    prevent_drag();
}

function prevent_drag() {
    $(".piece").on("dragstart", function(ev) {
        ev.preventDefault();
    });
}

function is_accessible(r, f, start_loc) {
    for (var i = 0; i < accessibility[r][f].length; i++) {
        var access = accessibility[r][f][i];
        if (access.start == start_loc) {
            return access.name;
        }
    }
    return undefined;
}

var current_board = undefined;
function init_board(b) {
    load_board(b);
    console.log("loading for player " + player);
    $(".piece").unbind("click");
    if (player == game.to_play && !termination) {
        $(".piece[data-color='" + player + "']").draggable({
            delay: 0,
            distance: 1,
            containment: "#board",
        }).click(function(ev) {
            ev.stopPropagation();
            start_move($(ev.target));
        });
        $(".piece[data-color!='" + player + "']").on("dragstart", function(ev) {
            ev.preventDefault();
        });
        if (document.title.substring(0, 4) != "(!!)") {
            $("#favicon").attr("href", "/static/favicon-turn.png");
            document.title = "(!!) " + document.title;
        }
    } else {
        prevent_drag();
    }
    $("#board td").droppable({
        drop: function(ev, ui) {
            var elem = ui.draggable;
            var r = elem.data().rank;
            var f = elem.data().file;
            var new_r = rank_from_str(ev.target.id);
            var new_f = file_from_str(ev.target.id);
            do_move(r, f, new_r, new_f);
        }
    });
    current_board = b;
}

function index_from_hash() {
    board_id = window.location.hash;
    if (!board_id) {
        return game.boards.length - 1;
    }
    board_to_display = +(board_id.split("-")[1]);
    if (!board_to_display
            || board_to_display < 0
            || board_to_display + 1 >= game.boards.length) {
        return game.boards.length - 1;
    }
    return board_to_display;
}

function init_with_current() {
    $(".move_link").css("color", "");
    $("#history_warning").hide();
    init_board(game.boards[game.boards.length - 1].board);
    $("#move" + (game.boards.length - 1)).css("color", "#000");
}

function display_history_at(board_to_display) {
    $(".move_link").css("color", "");
    $("#history_warning").show();
    reset_move();
    prevent_drag();
    load_board(game.boards[board_to_display].board);
    $("#move" + board_to_display).css("color", "#000");
}

function load_from_hash(ev) {
    if (ev) {
        ev.preventDefault();
    }
    board_to_display = index_from_hash();
    if (board_to_display + 1 >= game.boards.length) {
        init_with_current();
        return;
    }
    display_history_at(board_to_display);
}
window.onhashchange = load_from_hash;

$(document).ready(function() {
    // Initialize layout.
    $("#board tr").height($("#board").width() / 8);
    var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
    if (width <= 480) {
        var stats_elem = $("#stats");
        var summary_elem = $("#summary");
        if (stats_elem.height() > summary_elem.height()) {
            summary_elem.height(stats_elem.height());
        } else if (stats_elem.height() < summary_elem.height()) {
            stats_elem.height(summary_elem.height());
        }
        // We reshuffle the divs around the board on mobile; the move warning
        // comes before the summary on mobile.
        $("#history_warning").remove().insertBefore("#summary");
    }

    load_from_hash();

    console.log("connecting to socket server...");
    var socket = io.connect("http://" + document.domain + ":" + location.port);
    console.log("connected.");

    socket.on("connect", function() {
        console.log("got connection event, sending join");
        var path = document.location.pathname.split("/");
        socket.emit("join", {link: path[path.length - 1]});
        console.log("join sent");
    });
    socket.on("reload", function() {
        document.location.reload();
    });

    // Set up stats div toggler.
    var stat_div = $("#stats")
    var stat_link = $("#stats_toggle")
    function set_stats_visibility(visible) {
        if (visible) {
            stat_div.show();
            stat_link.text("Hide stats");
            window.localStorage["show_stats"] = "true";
        } else {
            stat_div.hide();
            stat_link.text("Show stats");
            window.localStorage["show_stats"] = "false";
        }
    }
    stat_link.click(function(ev) {
        ev.preventDefault();
        if (stat_div.css("display") == "none") {
            set_stats_visibility(true);
        } else {
            set_stats_visibility(false);
        }
    });
    set_stats_visibility(window.localStorage["show_stats"] != "false");

    // Set up move paginators
    $("#pager_left").click(function(ev) {
        ev.preventDefault();
        var idx = index_from_hash();
        var new_idx = idx - 1;
        if (new_idx < 0) {
            return;
        }
        window.location.hash = "board-" + new_idx;
    });
    $("#pager_right").click(function(ev) {
        ev.preventDefault();
        var idx = index_from_hash();
        var new_idx = idx + 1;
        window.location.hash = "board-" + new_idx;
    });
});
