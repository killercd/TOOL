import tkinter as tk
from tkinter import ttk
import sqlite3

class WinHTTPDrone():

    def __init__(self, root):
        self.root = root
        self.root.title("War Drone")
        #root.geometry("500x500")

        tk.Label(root, text="Session name:").grid(row=0, column=0, padx=1, pady=5, sticky="e")
        self.txt_session_name = tk.Entry(root)
        self.txt_session_name.grid(row=0, column=1, padx=1, pady=5)

        self.txt_session_name.bind("<Control-a>", self.select_all)
        self.txt_session_name.bind("<Control-A>", self.select_all)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copia", command=self.copy_text)
        self.context_menu.add_command(label="Taglia", command=self.cut_text)
        self.context_menu.add_command(label="Incolla", command=self.paste_text)

        self.txt_session_name.bind("<Button-3>", self.show_context_menu)

        self.btn_save = tk.Button(root, text="Save", command=self.save_session)
        self.btn_save.grid(row=1, column=1, padx=1, pady=5, sticky="e")
        self.btn_load = tk.Button(root, text="Load")
        self.btn_load.grid(row=1, column=2, padx=1, pady=5, sticky="e")

        self.lbl_session_name = tk.Label(root, text="N/A")
        self.lbl_session_name.grid(row=2, column=0, sticky="e")

    def save_session(self):
        session_name = f"{self.txt_session_name.get()}.db"
        print(f"[*] Saving {session_name}")
        self.db_connection = sqlite3.connect(session_name)
        self.lbl_session_name.config(text=session_name)

    def select_all(self, event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.see(tk.INSERT)
        return 'break'

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")


def main():
    root = tk.Tk()
    app = WinHTTPDrone(root)
    root.mainloop()

if __name__ == "__main__":
    main()
