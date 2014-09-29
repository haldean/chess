function loc_str(rank, file) {
    rank_str = "" + (rank + 1);
    file_str = ["a", "b", "c", "d", "e", "f", "g", "h"][file];
    return file_str + rank_str
}

$(document).ready(function() {
    var board_elem = document.getElementById("board");
    function load_board(b) {
        for (var r = 0; r < 8; r++) {
            for (var f = 0; f < 8; f++) {
                var square_elem = document.getElementById(loc_str(r, f));
                var piece = b[r*8+f];
                if (piece) {
                    square_elem.innerHTML = "<img src='/static/" + piece + ".svg'>";
                } else {
                    square_elem.innerHTML = "";
                }
            }
        }
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
