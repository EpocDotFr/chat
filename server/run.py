from server import SocketIoServer
import argparse


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--host', default='localhost')
    arg_parser.add_argument('--port', type=int, default=5000)
    arg_parser.add_argument('--dev', action='store_true')
    arg_parser.add_argument('--keyfile', default=None, nargs='?')
    arg_parser.add_argument('--certfile', default=None, nargs='?')

    args = arg_parser.parse_args()

    print('Initializing server...')

    server = SocketIoServer(logger=args.dev)

    if args.dev:
        from geventwebsocket.handler import WebSocketHandler
        from gevent.pywsgi import WSGIServer

        wsgi_args = (
            (args.host, args.port),
            server.wsgi_app
        )

        wsgi_kvargs = {
            'handler_class': WebSocketHandler
        }

        if args.keyfile and args.certfile:
            wsgi_kvargs['keyfile'] = args.keyfile
            wsgi_kvargs['certfile'] = args.certfile

        wsgi = WSGIServer(
            *wsgi_args,
            **wsgi_kvargs
        )

        try:
            wsgi.serve_forever()
        except KeyboardInterrupt:
            print('Shutting down server...')
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    run()
