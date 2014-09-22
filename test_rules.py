import chess
import unittest

class RulesTest(unittest.TestCase):
    def testMoveIsValid(self):
        b = chess.Board()
        m = chess.Move.on_board((1, 0), (3, 0), b)
        self.assertTrue(chess.move_is_valid(b, m))
        m = chess.Move.on_board((1, 0), (1, 1), b)
        self.assertFalse(chess.move_is_valid(b, m))
        m = chess.Move.on_board((2, 0), (2, 1), b)
        self.assertFalse(chess.move_is_valid(b, m))
        m = chess.Move.on_board((2, 0), (4, 0), b)
        self.assertFalse(chess.move_is_valid(b, m))
        m = chess.Move.on_board((1, 0), (4, 0), b)
        self.assertFalse(chess.move_is_valid(b, m))

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
        self.assertTrue(chess.move_is_valid(b, m))
        m = chess.Move.on_board((1, 1), (3, 1), b)
        self.assertFalse(chess.move_is_valid(b, m))
        m = chess.Move.on_board((1, 4), (3, 4), b)
        self.assertFalse(chess.move_is_valid(b, m))
        m = chess.Move.on_board((0, 0), (1, 0), b)
        self.assertTrue(chess.move_is_valid(b, m))
        m = chess.Move.on_board((0, 0), (0, 4), b)
        self.assertFalse(chess.move_is_valid(b, m))

if __name__ == '__main__':
    unittest.main()
