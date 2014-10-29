import chess
import stats
import stats_store

class PlayerGameStats(stats.Stats):
    def __init__(self, game_id, game, eco_data, player, rstore):
        stats.Stats.__init__(self, game, eco_data)
        self.game = game
        if game.termination is None:
            self.player_win = False
        if game.termination == chess.stalemate:
            self.player_win = False
        white_email, white_link = rstore.get_user(game_id, chess.white)
        black_email, black_link = rstore.get_user(game_id, chess.black)
        if player == white_email:
            self.player_link = white_link
            self.opponent = black_email
            if game.termination == chess.white_victory:
                self.player_win = True
            else:
                self.player_win = False
        else:
            self.player_link = black_link
            self.opponent = white_email
            if game.termination == chess.black_victory:
                self.player_win = True
            else:
                self.player_win = False
        self.public_link = rstore.get_public_link(game_id)
        self.last_move = None

class PlayerStats(object):
    def __init__(self, rstore, player, eco_data):
        self.rstore = stats_store.wrap(rstore)
        self.email = player
        self.player_games = self.rstore.games_for_player(player)
        self.won = set()
        self.lost = set()
        self.stalemate = set()
        self.in_progress = set()
        self.game_stats = dict()
        for game_id in self.player_games:
            game_stats = self.get_game_stats(game_id, eco_data)
            if game_stats.opponent == player:
                # Don't count games played against yourself
                continue
            if game_stats.player_win:
                self.won.add(game_id)
            elif game_stats.game.termination is None:
                self.in_progress.add(game_id)
            elif game_stats.game.termination == chess.stalemate:
                self.stalemate.add(game_id)
            else:
                self.lost.add(game_id)
            self.game_stats[game_id] = game_stats
        self.win_count = len(self.won)
        self.lose_count = len(self.lost)
        self.stalemate_count = len(self.stalemate)
        self.in_progress_count = len(self.in_progress)

    def get_game_stats(self, game_id, eco_data):
        game = self.rstore.get(game_id)
        return PlayerGameStats(game_id, game, eco_data, self.email, self.rstore)
