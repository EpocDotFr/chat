from urllib.parse import parse_qs
import socketio


class SocketIoServerNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        query_string = parse_qs(environ.get('QUERY_STRING', ''))

        nickname = query_string.get('nickname', [''])[0]
        color = query_string.get('color', [''])[0]

        self.save_session(sid, {
            'nickname': nickname,
            'color': color,
        })

        self.emit('joined', (sid, nickname, color))

        self.emit('users', list([
            {'sid': s, **self.get_session(s)} for s, _ in self.server.manager.get_participants(self.namespace, None)
        ]), room=sid)

    def on_disconnect(self, sid):
        self.emit('leaved', sid)

    def on_out_message(self, sid, message, time):
        self.emit('in_message', (sid, message, time))


class SocketIoServer(socketio.Server):
    def __init__(self, *args, **kvargs):
        super(SocketIoServer, self).__init__(*args, **kvargs)

        self.register_namespace(SocketIoServerNamespace('/'))

        self.wsgi_app = socketio.WSGIApp(self)
