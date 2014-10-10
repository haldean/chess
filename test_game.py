import chess
import unittest

class GameTest(unittest.TestCase):
    def testGame(self):
        g = chess.Game.new()
        pre_summary = g.summary()
        g = chess.Game.from_json_dict(g.to_json_dict())
        self.assertEqual(g.summary(), pre_summary)


if __name__ == '__main__':
    unittest.main()
