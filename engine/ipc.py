import gevent.server

from engine import event
from engine import host

def start(port=14924):
    _, host_queue = host.ChessHost.start()
    def handle(socket, addr):
        ev_str = socket.recv(event.max_event_size).strip()
        res_queue = gevent.queue.Queue()
        ev = event.Event.from_json(ev_str, res_queue)
        if not ev:
            resp = event.Response(event.status_bad_event)
        else:
            host_queue.put(ev)
            resp = res_queue.get()
        socket.sendall(resp.to_json())
    server = gevent.server.StreamServer(("127.0.0.1", port), handle)
    server.serve_forever()
