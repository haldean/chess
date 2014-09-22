import chess
import unittest

class MoveTest(unittest.TestCase):
    def testAlgebraic(self):
        board = """
        __ bN bB bK bQ bB bN __
        bp __ bp bp __ bp bp bp
        __ __ __ __ bR __ __ __
        __ __ wR __ __ __ __ wR
        __ bp bR __ __ __ __ __
        wp __ __ __ bR __ __ __
        __ wp wp wp wp wp wp wp
        __ wN wB wK wQ wB wN __
        """
        b = chess.Board.parse(board)
        m = chess.Move.on_board((2, 0), (3, 1), b)
        self.assertEqual("axb4", str(m))
        m = chess.Move.on_board((4, 2), (4, 6), b)
        self.assertEqual("Rcg5", str(m))
        m = chess.Move.on_board((3, 2), (3, 4), b)
        self.assertEqual("Rce4", str(m))
        m = chess.Move.on_board((2, 4), (4, 4), b)
        self.assertEqual("R3e5", str(m))

if __name__ == '__main__':
    unittest.main()
