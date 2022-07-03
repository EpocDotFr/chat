from server import SocketIoServer
import argparse


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--host', default='localhost')
    arg_parser.add_argument('--port', type=int, default=5000)
    arg_parser.add_argument('--dev', action='store_true')

    args = arg_parser.parse_args()

    print('Initializing server...')

    server = SocketIoServer(logger=args.dev)

    if args.dev:
        from geventwebsocket.handler import WebSocketHandler
        from gevent.pywsgi import WSGIServer

        wsgi = WSGIServer((args.host, args.port), server.wsgi_app, handler_class=WebSocketHandler)

        try:
            wsgi.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down server...')
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    run()
