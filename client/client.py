import tkinter.font as tk_font
from tkinter import ttk
import tkinter as tk
import socketio


class SocketIoClientNamespace(socketio.ClientNamespace):
    def __init__(self, application, *args, **kvargs):
        super(SocketIoClientNamespace, self).__init__(*args, **kvargs)

        self.application = application

    def on_connect(self):
        self.application.add_system_private_message('Connecté')

    def on_connect_error(self, data):
        self.application.add_system_private_message('Échec de la connexion')

    def on_disconnect(self):
        self.application.add_system_private_message('Déconnecté')

    def on_in_message(self, nickname, message):
        self.application.add_chat_message(nickname, message)

    def on_joined(self, nickname):
        self.application.add_system_public_message('{} a rejoint le chat'.format(nickname))

    def on_leaved(self, nickname):
        self.application.add_system_public_message('{} a quitté le chat'.format(nickname))


class Application(tk.Tk):
    def __init__(self, nickname, url, dev=False, *args, **kvargs):
        super(Application, self).__init__(*args, **kvargs)

        self.nickname = nickname
        self.url = url
        self.dev = dev

        self.title('Chat - {}@{}'.format(self.nickname, self.url))
        self.geometry('800x600')

        self.build_gui()
        self.init_events()
        self.init_socketio()

    def add_chat_message(self, nickname, message):
        self.messages.configure(state=tk.NORMAL)

        self.messages.insert(tk.END, '<{}>'.format(nickname), ('nickname',))
        self.messages.insert(tk.END, ' ' + message + '\n')

        self.messages.configure(state=tk.DISABLED)

    def add_system_public_message(self, message):
        self.messages.configure(state=tk.NORMAL)

        self.messages.insert(tk.END, message + '\n', ('system-public',))

        self.messages.configure(state=tk.DISABLED)

    def add_system_private_message(self, message):
        self.messages.configure(state=tk.NORMAL)

        self.messages.insert(tk.END, message + '\n', ('system-private',))

        self.messages.configure(state=tk.DISABLED)

    def build_gui(self):
        # Messages container
        self.messages = tk.Text(self)

        self.nickname_font = tk_font.Font(font='TkDefaultFont')
        self.nickname_font.configure(weight='bold')

        self.system_message_font = tk_font.Font(font='TkDefaultFont')
        self.system_message_font.configure(slant='italic')

        self.messages.tag_configure('nickname', font=self.nickname_font)
        self.messages.tag_configure('system-public', foreground='dark green', font=self.system_message_font)
        self.messages.tag_configure('system-private', foreground='grey', font=self.system_message_font)

        self.messages.pack(fill=tk.BOTH, expand=True)

        # New message input
        self.message_input = ttk.Entry(self)
        self.message_input.pack(fill=tk.BOTH, expand=True)
        self.message_input.focus()

    def init_events(self):
        # Program exit
        def on_closing():
            self.sio.disconnect()

            self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_closing)

        # Send message
        def send_message(event):
            self.sio.emit('out_message', (self.nickname, self.message_input.get()))

            self.message_input.delete(0, tk.END)

        self.message_input.bind('<Return>', send_message)

    def init_socketio(self):
        self.sio = socketio.Client(logger=self.dev, ssl_verify=not self.dev)
        self.sio.register_namespace(SocketIoClientNamespace(self, '/'))

        try:
            self.add_system_private_message('Connexion à {}...'.format(self.url))

            self.sio.connect(self.url + '?nickname=' + self.nickname, transports=('websocket',))
        except KeyboardInterrupt:
            print('Shutting down client...')
        except Exception as e:
            self.add_system_private_message(str(e))
