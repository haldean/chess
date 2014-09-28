import json

status_ok = 0
status_bad_game = 1
status_bad_move = 2
status_bad_event = 3

max_event_size = 1024

class Event(object):
    def __init__(self, kind, response_queue):
        self.kind = kind
        self.response_queue = response_queue

    def respond(self, response):
        self.response_queue.put(response)

    @classmethod
    def from_json(cls, jstr, response_queue):
        json_obj = json.loads(jstr)
        if "kind" not in json_obj:
            print "No kind specified in event", jstr
            return None
        kind = json_obj["kind"]
        if kind == "move":
            return MoveEvent.from_json(json_obj, response_queue)
        if kind == "start":
            return StartEvent.from_json(json_obj, response_queue)
        print "Can't handle event kind", kind, "in", jstr
        return None

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

    def to_json(self):
        res = {"status": self.status}
        if self.game_id is not None:
            res["game_id"] = self.game_id
        if self.game is not None:
            res["game"] = self.game
        if self.details is not None:
            res["details"] = self.details
        return json.dumps(res)
