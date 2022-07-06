from urllib.parse import parse_qs
import socketio


class SocketIoServerNamespace(socketio.Namespace):
    def on_connect(self, sid, environ, auth):
        query_string = parse_qs(environ.get('QUERY_STRING', ''))

        nickname = query_string.get('nickname', [''])[0]
        color = query_string.get('color', [''])[0]

        self.emit('joined', (sid, nickname, color))

    def on_disconnect(self, sid):
        self.emit('leaved', sid)

    def on_out_message(self, sid, message, time):
        self.emit('in_message', (sid, message, time))


class SocketIoServer(socketio.Server):
    def __init__(self, *args, **kvargs):
        super(SocketIoServer, self).__init__(*args, **kvargs)

        self.register_namespace(SocketIoServerNamespace('/'))

        self.wsgi_app = socketio.WSGIApp(self)
