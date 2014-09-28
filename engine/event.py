status_ok = 0
status_bad_game = 1
status_bad_move = 2
status_bad_event = 3

class Event(object):
    def __init__(self, kind, response_queue):
        self.kind = kind
        self.response_queue = response_queue

    def respond(response):
        self.response_queue.put(response)

class MoveEvent(Event):
    def __init__(self, game_id, player, move, response_queue):
        Event.__init__(self, "move", response_queue)
        self.game_id = game_id
        self.player = player
        self.move = move

class StartEvent(Event):
    def __init__(self):
        Event.__init__(self, "start", response_queue)

class Response(object):
    def __init__(self, status, game_id=None, game=None, details=None):
        self.status = status
        self.game_id = game_id
        self.game = game
        self.details = details
