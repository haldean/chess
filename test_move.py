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
        wp __ __ __ bR __ wp __
        __ wp wp wp wp wp wp __
        __ wN wB wK wQ wB wN __
        """
        b = chess.Board.parse(board)

        m = chess.Move.on_board((1, 1), (2, 1), b)
        self.assertEqual("b3", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.white, "b3"))

        m = chess.Move.on_board((2, 6), (3, 6), b)
        self.assertEqual("g4", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.white, "g4"))

        m = chess.Move.on_board((6, 0), (4, 0), b)
        self.assertEqual("a5", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.black, "a5"))

        m = chess.Move.on_board((2, 0), (3, 1), b)
        self.assertEqual("axb4", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.white, "axb4"))

        m = chess.Move.on_board((4, 2), (4, 6), b)
        self.assertEqual("Rcg5", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.white, "Rcg5"))

        m = chess.Move.on_board((3, 2), (3, 4), b)
        self.assertEqual("Rce4", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.black, "Rce4"))

        m = chess.Move.on_board((2, 4), (4, 4), b)
        self.assertEqual("R3e5", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.black, "R3e5"))

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
        b = chess.Board.parse(board)
        m = chess.Move.on_board((2, 3), (1, 3), b)
        self.assertEqual("Rxd2+", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.black, "Rxd2+"))

        m = chess.Move.on_board((5, 4), (0, 4), b)
        self.assertEqual("Re1#", m.algebraic)
        self.assertEqual(m, chess.parse_algebraic(b, chess.black, "Re1#"))

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
        self.assertEqual("0-0", ks_m.algebraic)
        self.assertEqual(ks_m, chess.parse_algebraic(b, chess.black, "0-0"))
        ks_b = b.apply(ks_m)
        self.assertFalse(ks_b.can_castle(chess.black, chess.kingside))
        self.assertFalse(ks_b.can_castle(chess.black, chess.queenside))
        self.assertEqual(ks_b[7, 2], chess.Piece(chess.black, chess.rook))

        qs_m = chess.Move.on_board((7, 3), (7, 5), b)
        self.assertTrue(qs_m.is_castle)
        self.assertEqual(qs_m.castle, (chess.black, chess.queenside))
        self.assertEqual("0-0-0", qs_m.algebraic)
        self.assertEqual(qs_m, chess.parse_algebraic(b, chess.black, "0-0-0"))
        qs_b = b.apply(qs_m)
        self.assertFalse(qs_b.can_castle(chess.black, chess.kingside))
        self.assertFalse(qs_b.can_castle(chess.black, chess.queenside))
        self.assertEqual(qs_b[7, 4], chess.Piece(chess.black, chess.rook))


if __name__ == '__main__':
    unittest.main()
