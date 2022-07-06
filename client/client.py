from urllib.parse import urlencode
from colorhash import ColorHash
import tkinter.font as tk_font
from datetime import datetime
from tkinter import ttk
import tkinter as tk
import socketio


class SocketIoClientNamespace(socketio.ClientNamespace):
    def __init__(self, application, *args, **kvargs):
        super(SocketIoClientNamespace, self).__init__(*args, **kvargs)

        self.application = application

    def on_connect(self):
        self.application.messages_list.add_system_private_message('Connecté')

    def on_connect_error(self, data):
        self.application.messages_list.add_system_private_message('Échec de la connexion')

    def on_disconnect(self):
        self.application.messages_list.add_system_private_message('Déconnecté')

    def on_in_message(self, sender_sid, nickname, color, message, time):
        self.application.messages_list.add_chat_message(sender_sid, nickname, color, message, time)

    def on_joined(self, nickname):
        self.application.messages_list.add_system_public_message('{} a rejoint le chat'.format(nickname))

    def on_leaved(self, nickname):
        self.application.messages_list.add_system_public_message('{} a quitté le chat'.format(nickname))


class MessagesList:
    def __init__(self, application):
        self.application = application

        self.text_widget = tk.Text(self.application)

        self.nickname_font = tk_font.Font(font='TkDefaultFont')
        self.nickname_font.configure(weight='bold')

        self.system_message_font = tk_font.Font(font='TkDefaultFont')
        self.system_message_font.configure(slant='italic')

        self.text_widget.tag_configure('time', foreground='grey')
        self.text_widget.tag_configure('nickname', font=self.nickname_font)
        self.text_widget.tag_configure('system-public', foreground='dark green', font=self.system_message_font)
        self.text_widget.tag_configure('system-private', foreground='grey', font=self.system_message_font)

        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.nicknames_color = []

    def add_chat_message(self, sender_sid, nickname, color, message, time):
        if sender_sid not in self.nicknames_color:
            self.text_widget.tag_configure('nickname-' + sender_sid, foreground=color)

            self.nicknames_color.append(sender_sid)

        self.text_widget.configure(state=tk.NORMAL)

        self.text_widget.insert(tk.END, '{}'.format(time), ('time',))
        self.text_widget.insert(tk.END, ' ')
        self.text_widget.insert(tk.END, '{}'.format(nickname), ('nickname', 'nickname-' + sender_sid))
        self.text_widget.insert(tk.END, ': ' + message + '\n')

        self.text_widget.configure(state=tk.DISABLED)

    def add_system_public_message(self, message):
        self.text_widget.configure(state=tk.NORMAL)

        self.text_widget.insert(tk.END, message + '\n', ('system-public',))

        self.text_widget.configure(state=tk.DISABLED)

    def add_system_private_message(self, message):
        self.text_widget.configure(state=tk.NORMAL)

        self.text_widget.insert(tk.END, message + '\n', ('system-private',))

        self.text_widget.configure(state=tk.DISABLED)


class MessageInput:
    def __init__(self, application):
        self.application = application

        self.entry_widget = ttk.Entry(self.application)
        self.entry_widget.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.entry_widget.focus()

        self.entry_widget.bind('<Return>', self.send_message)

    def send_message(self, event):
        self.application.sio.emit('out_message', (
            self.application.nickname,
            self.application.color,
            self.entry_widget.get(),
            datetime.now().strftime('%H:%M')
        ))

        self.entry_widget.delete(0, tk.END)


class Application(tk.Tk):
    def __init__(self, nickname, url, dev=False, *args, **kvargs):
        super(Application, self).__init__(*args, **kvargs)

        self.nickname = nickname
        self.url = url
        self.dev = dev

        self.color = ColorHash(self.nickname).hex

        self.title('Chat - {}@{}'.format(self.nickname, self.url))
        self.geometry('800x600')
        self.iconphoto(False, tk.PhotoImage(file='resources/images/icon.png'))

        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        self.messages_list = MessagesList(self)
        self.message_input = MessageInput(self)

        self.init_socketio()

    def on_closing(self):
        self.sio.disconnect()
        self.destroy()

    def init_socketio(self):
        self.sio = socketio.Client(logger=self.dev, ssl_verify=not self.dev)
        self.sio.register_namespace(SocketIoClientNamespace(self, '/'))

        try:
            self.messages_list.add_system_private_message('Connexion à {}...'.format(self.url))

            params = {
                'nickname': self.nickname,
            }

            self.sio.connect(self.url + '?' + urlencode(params), transports=('websocket',))
        except KeyboardInterrupt:
            print('Shutting down client...')
        except Exception as e:
            self.messages_list.add_system_private_message(str(e))
