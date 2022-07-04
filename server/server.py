from urllib.parse import parse_qs
import socketio


class SocketIoServerNamespace(socketio.Namespace):
    def on_connect(self, sid, environ, auth):
        query_string = parse_qs(environ.get('QUERY_STRING', ''))

        nickname = query_string.get('nickname', [''])[0]

        self.save_session(sid, {'nickname': nickname})

        self.emit('joined', nickname)

    def on_disconnect(self, sid):
        nickname = self.get_session(sid).get('nickname', '')

        self.emit('leaved', nickname)

    def on_out_message(self, sid, nickname, color, message, time):
        self.emit('in_message', (sid, nickname, color, message, time))


class SocketIoServer(socketio.Server):
    def __init__(self, *args, **kvargs):
        super(SocketIoServer, self).__init__(*args, **kvargs)

        self.register_namespace(SocketIoServerNamespace('/'))

        self.wsgi_app = socketio.WSGIApp(self)
