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

$(document).ready(function() {
    var board_elem = document.getElementById("board");
    var current_board = undefined;
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

    function prevent_drag() {
        $(".piece").on("dragstart", function(ev) {
            ev.preventDefault();
        });
    }

    function do_move(r, f, new_r, new_f) {
        var start_loc = loc_str(r, f);
        var good = false;
        var move_name = undefined;
        for (var i = 0; i < accessibility[new_r][new_f].length; i++) {
            access = accessibility[new_r][new_f][i];
            if (access.start == start_loc) {
                good = true;
                move_name = access.name;
                break;
            }
        }
        if (!good) {
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

    function init_board(b) {
        load_board(b);
        if (player == game.to_play) {
            $(".piece[data-color='" + player + "']").draggable();
            $(".piece[data-color!='" + player + "']").on("dragstart", function(ev) {
                ev.preventDefault();
            });
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

    init_board(game.boards[game.boards.length - 1].board);

    var socket = io.connect("http://" + document.domain + ":" + location.port);
    socket.on("connect", function() {
        var path = document.location.pathname.split("/");
        socket.emit("join", {link: path[path.length - 1]});
    });
    socket.on("reload", function() {
        document.location.reload();
    });
});
