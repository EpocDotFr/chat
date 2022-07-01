import socketio


class SocketIoNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid):
        pass


class SocketIoServer(socketio.Server):
    def __init__(self, *args, **kvargs):
        super(SocketIoServer, self).__init__(*args, **kvargs)

        self.register_namespace(SocketIoNamespace('/'))

        self.wsgi_app = socketio.WSGIApp(self)
