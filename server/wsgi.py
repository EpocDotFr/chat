from server import SocketIoServer

server = SocketIoServer()

application = server.wsgi_app
