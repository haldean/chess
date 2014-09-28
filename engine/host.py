import chess
import gevent.queue

from engine import store
from engine import event

class ChessHost(object):
    def __init__(self, store, queue):
        self._store = store
        self._queue = queue

    def loop(self):
        for ev in self._queue:
            if ev.kind == "move":
                self._do_move(ev)
            elif ev.kind == "start":
                self._do_start(ev)
            else:
                print "Can't handle event type \"%s\"" % ev.kind
                ev.respond(event.Response(event.status_bad_event))

    def _do_start(self, ev):
        game_id, game = self._store.begin()
        ev.respond(event.Response(event.status_ok, game_id, game))

    def _do_move(self, ev):
        game = self._store.get(ev.game_id)
        if not game:
            ev.respond(event.Response(event.status_bad_game))
            return
        try:
            game.algebraic_move(ev.move)
            ev.respond(event.Response(event.status_ok, ev.game_id, game))
        except chess.InvalidMoveError as e:
            ev.respond(event.Response(
                event.status_bad_move, ev.game_id, game, str(e)))

    @classmethod
    def start(cls):
        s = store.InMemoryStore()
        queue = gevent.queue.Queue()
        return cls(s, queue), queue
