from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from server import SocketIoServer
import argparse


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--host', default='localhost')
    arg_parser.add_argument('--port', type=int, default=5000)

    args = arg_parser.parse_args()

    print('Initializing server...')

    server = SocketIoServer(logger=True)

    wsgi = WSGIServer((args.host, args.port), server.wsgi_app, handler_class=WebSocketHandler)
    wsgi.serve_forever()

if __name__ == '__main__':
    run()
