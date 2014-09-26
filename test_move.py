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

    def testAlgebraicCheck(self):
        board = """
        __ bN __ bK bQ __ bN __
        bp __ bp bp __ bp bp bp
        __ __ __ __ bR __ __ __
        __ __ wR __ __ __ __ wR
        __ bp __ __ __ __ __ __
        wp __ __ bR __ __ __ __
        __ wp wp wp __ bB wp wp
        __ wN wB wK __ wB wN __
        """
        m = chess.Move.on_board((2, 3), (1, 3), b)
        self.assertEqual("Rxd2+", str(m))
        m = chess.Move.on_board((5, 4), (0, 4), b)
        self.assertEqual("Re1#", str(m))

    def testCastle(self):
        board = """
        bR __ __ bK __ __ __ bR
        bp __ bp bp __ bp bp bp
        __ __ __ __ __ __ __ __
        __ __ wR __ __ __ __ wR
        __ bp __ __ __ __ __ __
        wp __ __ __ __ __ __ __
        __ wp wp wp wp wp wp wp
        __ wN wB wK wQ wB wN __
        """
        b = chess.Board.parse(board)
        self.assertTrue(b.can_castle(chess.black, chess.kingside))

        ks_m = chess.Move.on_board((7, 3), (7, 1), b)
        self.assertTrue(ks_m.is_castle)
        self.assertEqual(ks_m.castle, (chess.black, chess.kingside))
        self.assertEqual("0-0", str(ks_m))
        ks_b = b.apply(ks_m)
        self.assertFalse(ks_b.can_castle(chess.black, chess.kingside))
        self.assertFalse(ks_b.can_castle(chess.black, chess.queenside))
        self.assertEqual(ks_b[7, 2], chess.Piece(chess.black, chess.rook))

        qs_m = chess.Move.on_board((7, 3), (7, 5), b)
        self.assertTrue(qs_m.is_castle)
        self.assertEqual(qs_m.castle, (chess.black, chess.queenside))
        self.assertEqual("0-0-0", str(qs_m))
        qs_b = b.apply(qs_m)
        self.assertFalse(qs_b.can_castle(chess.black, chess.kingside))
        self.assertFalse(qs_b.can_castle(chess.black, chess.queenside))
        self.assertEqual(qs_b[7, 4], chess.Piece(chess.black, chess.rook))


if __name__ == '__main__':
    unittest.main()
