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

    def on_connect_error(self):
        self.application.add_system_private_message('Échec de la connexion')

    def on_disconnect(self):
        self.application.add_system_private_message('Déconnecté')


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

        self.system_message_public_font = tk_font.Font(font='TkDefaultFont')
        self.system_message_public_font.configure(slant='italic')

        self.system_message_private_font = tk_font.Font(font='TkDefaultFont')
        self.system_message_private_font.configure(slant='italic')

        self.messages.tag_configure('nickname', font=self.nickname_font)
        self.messages.tag_configure('system-public', foreground='dark green', font=self.system_message_public_font)
        self.messages.tag_configure('system-private', foreground='grey', font=self.system_message_private_font)

        self.add_system_public_message('Epoc a rejoint le chat')
        self.add_chat_message('Epoc', 'yo')

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

    def init_socketio(self):
        self.sio = socketio.Client(logger=self.dev)
        self.sio.register_namespace(SocketIoClientNamespace(self, '/'))

        try:
            self.add_system_private_message('Connexion à {}...'.format(self.url))

            self.sio.connect(self.url, transports=('websocket',))
        except KeyboardInterrupt:
            print('Shutting down client...')
        except Exception as e:
            self.add_system_private_message(str(e))
