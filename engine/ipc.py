import gevent

from engine import host

def start(port=14924):
    host_queue = host.ChessHost.start()
    def handle(socket, addr):
        print "New connection from", socket, addr
    server = gevent.server.StreamServer(("127.0.0.1", port), handle)
    server.serve_forever()
