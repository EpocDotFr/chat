import socketio


class SocketIoServerNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print('Connected')

    def on_disconnect(self, sid):
        print('Disconnected')


class SocketIoServer(socketio.Server):
    def __init__(self, *args, **kvargs):
        super(SocketIoServer, self).__init__(*args, **kvargs)

        self.register_namespace(SocketIoServerNamespace('/'))

        self.wsgi_app = socketio.WSGIApp(self)
