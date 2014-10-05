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
                        "data-rank='" + r + "' data-file='" + f + "'>");
                } else {
                    square_elem.innerHTML = "";
                }
            }
        }
        $(".piece").draggable();
        $("#board td").droppable({
            drop: function(ev, ui) {
                var elem = ui.draggable;
                var r = elem.data().rank;
                var f = elem.data().file;
                var new_r = rank_from_str(ev.target.id);
                var new_f = file_from_str(ev.target.id);
                current_board[new_r * 8 + new_f] = current_board[r * 8 + f];
                current_board[r * 8 + f] = "";
                load_board(current_board);
            }
        });
        current_board = b;
    }

    test_board = [
        "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR",
        "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "", "", "", "", "", "", "", "",
        "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
        "bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"];
    load_board(test_board);
});
