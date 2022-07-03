import tkinter.font as tk_font
from tkinter import ttk
import tkinter as tk
import socketio


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

    def build_gui(self):
        # Messages container
        self.messages = tk.Text(self)

        nickname_font = tk_font.Font(font='TkDefaultFont')
        nickname_font.configure(weight='bold')

        system_message_public_font = tk_font.Font(font='TkDefaultFont')
        system_message_public_font.configure(slant='italic')

        system_message_private_font = tk_font.Font(font='TkDefaultFont')
        system_message_private_font.configure(slant='italic')

        self.messages.tag_configure('nickname', font=nickname_font)
        self.messages.tag_configure('system-public', foreground='dark green', font=system_message_public_font)
        self.messages.tag_configure('system-private', foreground='grey', font=system_message_private_font)

        self.messages.insert(tk.END, 'Connexion à {}...'.format(self.url), ('system-private',))
        self.messages.insert(tk.END, '\nConnecté', ('system-private',))

        self.messages.insert(tk.END, '\nEpoc a rejoint le chat', ('system-public',))

        self.messages.insert(tk.END, '\n<Epoc>', ('nickname',))
        self.messages.insert(tk.END, ' Yo')

        self.messages.configure(state=tk.DISABLED)

        self.messages.pack(fill=tk.BOTH, expand=True)

        # New message input

        self.message_input = ttk.Entry(self)

        self.message_input.pack(fill=tk.BOTH, expand=True)

    def init_events(self):
        def on_closing():
            self.sio.disconnect()

            self.destroy()

        self.protocol('WM_DELETE_WINDOW', on_closing)

    def init_socketio(self):
        self.sio = socketio.Client(logger=self.dev)

        try:
            self.sio.connect(self.url, transports=('websocket',))
        except KeyboardInterrupt:
            print('Shutting down client...')

        @self.sio.event
        def connect():
            print('Connected')

        @self.sio.event
        def connect_error(data):
            print('Connection failed')

        @self.sio.event
        def disconnect():
            print('Disconnected')
