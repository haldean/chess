import chess
import json
import stats_store

class VictoryStats(object):
    def __init__(self, rstore):
        rstore = stats_store.wrap(rstore)
        self.victories = rstore.terminations()
        total = float(sum(self.victories.itervalues()))
        if total == 0:
            self.white_prop = 0
            self.black_prop = 0
            self.stalemate_prop = 0
        else:
            self.white_prop = self.victories[chess.white_victory] / total
            self.black_prop = self.victories[chess.black_victory] / total
            self.stalemate_prop = self.victories[chess.stalemate] / total

    def json(self):
        return json.dumps([
            [chess.white_victory, self.white_prop],
            [chess.black_victory, self.black_prop],
            [chess.stalemate, self.stalemate_prop],
        ])

class PlayStats(object):
    def __init__(self, rstore):
        rstore = stats_store.wrap(rstore)
        self.game_count = rstore.game_count()
        self.player_count = rstore.player_count()
        self.game_lengths = []
        game_length_dict = rstore.game_lengths()
        for game_len in sorted(int(k) for k in game_length_dict.keys()):
            self.game_lengths.append((game_len, game_length_dict[str(game_len)]))

    def json(self):
        return json.dumps({
            "game_count": self.game_count,
            "player_count": self.player_count,
            "game_lengths": self.game_lengths
        })
