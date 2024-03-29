from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from server import SocketIoServer
from environs import Env


def run():
    env = Env()
    env.read_env()

    config = {
        'host': env.str('HOST', default='localhost'),
        'port': env.int('PORT', default=5000),
        'dev': env.bool('DEV', default=False),
        'keyfile': env.str('KEYFILE', default=None),
        'certfile': env.str('CERTFILE', default=None),
    }

    print('Initializing server...')

    server = SocketIoServer(logger=config.get('dev'))

    wsgi_args = (
        (config.get('host'), config.get('port')),
        server.wsgi_app
    )

    wsgi_kvargs = {
        'handler_class': WebSocketHandler
    }

    if config.get('keyfile') and config.get('certfile'):
        wsgi_kvargs['keyfile'] = config.get('keyfile')
        wsgi_kvargs['certfile'] = config.get('certfile')

    wsgi = WSGIServer(
        *wsgi_args,
        **wsgi_kvargs
    )

    try:
        wsgi.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server...')


if __name__ == '__main__':
    run()
