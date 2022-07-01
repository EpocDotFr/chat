import tkinter.font as tk_font
import tkinter as tk


class Application(tk.Tk):
    def __init__(self, *args, **kvargs):
        super(Application, self).__init__(*args, **kvargs)

        self.title('Chat')
        self.geometry('800x600')

        self.build_gui()

    def build_gui(self):
        self.text_widget = tk.Text(self)

        nickname_font = tk_font.Font(font='TkDefaultFont')
        nickname_font.configure(weight='bold')

        system_font = tk_font.Font(font='TkDefaultFont')
        system_font.configure(slant='italic')

        self.text_widget.tag_configure('nickname', font=nickname_font)
        self.text_widget.tag_configure('system', font=system_font)

        self.text_widget.insert(tk.END, '<Epoc>', ('nickname',))
        self.text_widget.insert(tk.END, ' Hey')

        self.text_widget.insert(tk.END, '\nMastock a rejoint le chat', ('system',))

        self.text_widget.insert(tk.END, '\n<Mastock>', ('nickname',))
        self.text_widget.insert(tk.END, ' yo')

        self.text_widget.insert(tk.END, '\nMastock a quitté le chat', ('system',))

        self.text_widget.configure(state=tk.DISABLED)

        self.text_widget.pack(fill=tk.BOTH, expand=True)
