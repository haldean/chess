import chess
import unittest

class RulesTest(unittest.TestCase):
    def testPawn(self):
        b = chess.Board.new()
        m = chess.Move.on_board((1, 0), (3, 0), b)
        self.assertTrue(m.is_valid(b))
        m = chess.Move.on_board((1, 0), (1, 1), b)
        self.assertFalse(m.is_valid(b))
        m = chess.Move.on_board((2, 0), (2, 1), b)
        self.assertFalse(m.is_valid(b))
        m = chess.Move.on_board((2, 0), (4, 0), b)
        self.assertFalse(m.is_valid(b))
        m = chess.Move.on_board((1, 0), (4, 0), b)
        self.assertFalse(m.is_valid(b))

        board = """
        bR bN bB bK bQ bB bN bR
        bp __ bp bp __ bp bp bp
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ bp __ __ __ __ __ __
        wp __ __ __ bp __ __ __
        __ wp wp wp wp wp wp wp
        wR wN wB wK wQ wB wN wR
        """
        b = chess.Board.parse(board)
        m = chess.Move.on_board((2, 0), (3, 1), b)
        self.assertTrue(m.is_valid(b))
        m = chess.Move.on_board((1, 1), (3, 1), b)
        self.assertFalse(m.is_valid(b))
        m = chess.Move.on_board((1, 4), (3, 4), b)
        self.assertFalse(m.is_valid(b))
        m = chess.Move.on_board((0, 0), (1, 0), b)
        self.assertTrue(m.is_valid(b))
        m = chess.Move.on_board((0, 0), (0, 4), b)
        self.assertFalse(m.is_valid(b))

    def testBishop(self):
        board = """
        bR bN bB bK bQ bB bN bR
        bp __ bp bp __ bp bp bp
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ bp __ __ __ __ __ __
        __ __ __ __ bp __ __ __
        __ __ wp wp wp wp wp wp
        wR wN wB wK wQ wB wN wR
        """
        b = chess.Board.parse(board)
        m = chess.Move.on_board((0, 2), (2, 0), b)
        self.assertTrue(m.is_valid(b))

    def testCastle(self):
        board = """
        bR __ __ bK bQ bB bN bR
        bp __ bp bp __ bp bp bp
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ bp __ __ __ __ __ __
        wp __ __ __ bp __ __ __
        __ wp wp wp wp wp wp wp
        wR wN wB wK wQ wB wN wR
        """
        b = chess.Board.parse(board)
        m = chess.Move.on_board((7, 3), (7, 1), b)
        self.assertTrue(m.is_valid(b))
        m = chess.Move.on_board((7, 3), (7, 5), b)
        self.assertFalse(m.is_valid(b))

        board = """
        bR __ __ bK bQ bB bN bR
        bp __ bp bp __ bp bp bp
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ wR __ __ __ __ __ __
        wp __ __ __ bp __ __ __
        __ wp wp wp wp wp wp wp
        wR wN wB wK wQ wB wN wR
        """
        b = chess.Board.parse(board)
        m = chess.Move.on_board((7, 3), (7, 1), b)
        self.assertFalse(m.is_valid(b))

    def testEnPassant(self):
        board = """
        __ __ __ bK __ __ __ __
        __ __ bp __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wp __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        m = chess.Move.on_board((6, 2), (4, 2), b)
        self.assertTrue(m.is_valid(b))
        b = b.apply(m)
        m = chess.Move.on_board((4, 3), (5, 2), b)
        self.assertTrue(m.is_valid(b))
        b = b.apply(m)
        self.assertFalse(list(b.find(chess.Piece(chess.black, chess.pawn))))

    def testInCheck(self):
        board = """
        __ __ __ bK __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        wB __ __ wp __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        self.assertTrue(chess.in_check(b, chess.black))

        board = """
        __ __ __ bK __ __ __ __
        __ __ bp __ __ __ __ __
        __ __ __ __ __ __ __ __
        wB __ __ wp __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        self.assertFalse(chess.in_check(b, chess.black))

        board = """
        __ __ __ __ __ __ __ __
        __ __ __ bK __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wp __ __ __ __
        wB __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        self.assertTrue(chess.in_check(b, chess.black))

    def testCheckmate(self):
        board = """
        __ __ __ bK __ __ __ __
        __ __ __ wQ __ __ __ __
        __ __ __ __ __ __ __ __
        wB __ __ wp __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        # Kxd7 is a valid move.
        self.assertFalse(chess.in_checkmate(b, chess.black))

        board = """
        __ __ __ bK __ __ __ __
        __ __ __ wQ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wp __ __ __ __
        wB __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        self.assertTrue(chess.in_checkmate(b, chess.black))

        board = """
        __ __ __ bK __ __ __ __
        bR __ __ wQ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wp __ __ __ __
        wB __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ __ __ __ __ __
        __ __ __ wK __ __ __ __
        """
        b = chess.Board.parse(board)
        self.assertFalse(chess.in_checkmate(b, chess.black))


if __name__ == '__main__':
    unittest.main()
