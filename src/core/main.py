import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from core.database import Database
from ui.current_week import Home
from ui.weeks_log import WeeksLog
from ui.projects import Projects
from ui.settings import Settings
from core.paths import ICON_PATH
from ui.style import StyleManager
from core.version import install_new_version, check_new_version, REMOTE_URL, CURRENT_VERSION, get_remote_version
from ui.login import Login

import webbrowser
import sys

class Main(tk.Tk):
  def __init__(self):
    super().__init__()
    self.minsize(1200, 700)
    self.title("StudyArc")
    self.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())

    StyleManager(self)

    self.show_projects_var = tk.BooleanVar(value=True)
    self.show_weeks_log_var = tk.BooleanVar(value=True)
    self.show_current_week_var = tk.BooleanVar(value=True)

    try: 
      self.iconbitmap(ICON_PATH)
    except tk.TclError:
      self.iconbitmap("../assets/logo.ico")

    self.database = Database()

    self.user_id = None
    self.withdraw()
    self.login_class = Login(self, self.database.cursor, self.database.conn)
    self.wait_window(self.login_class)

    if self.user_id is not None:
      self.run()
    else:
      self.destroy()

  def run(self):
    for widget in self.winfo_children():
      widget.destroy()

    menubar = tk.Menu(self)

    view_menu = tk.Menu(menubar, tearoff=0)
    view_menu.add_checkbutton(label="Show current week", command=lambda: self.run(), variable=self.show_current_week_var)
    view_menu.add_checkbutton(label="Show week log", command=lambda: self.run(), variable=self.show_weeks_log_var)
    menubar.add_cascade(label="View", menu=view_menu)

    more_menu = tk.Menu(menubar, tearoff=0)
    more_menu.add_command(label="Settings", command=lambda: self.open_settings())
    more_menu.add_command(label="About", command=lambda: self.open_help())
    more_menu.add_command(label="Report bug", command=lambda: self.open_report_bug())
    more_menu.add_separator()
    more_menu.add_command(label="Exit", command=lambda: self.destroy())

    menubar.add_cascade(label="Help", menu=more_menu)

    menubar.add_command(label="Projects", command=lambda: Projects(frame_left_side, self, self.database.cursor, self.database.conn, self.user_id))

    self.config(menu=menubar)

    self.container = ttk.Frame(self)
    self.container.pack(fill="both", expand=True)

    ttk.Label(self.container, text="Study Dashboard", font=(StyleManager.get_current_font(), 20, "bold")).pack(anchor="center", pady=15)

    frame_left_side = ttk.Frame(self.container)
    frame_left_side.pack(side="left", expand=True, fill="both", padx=15, pady=15)

    if self.show_current_week_var.get():
      self.current_week_frame = Home(frame_left_side, self, self.user_id, self.database.cursor, self.database.conn)
      self.current_week_frame.draw_table()

    if self.show_weeks_log_var.get():
      self.weeks_log_frame = WeeksLog(self.container, self, self.user_id, self.database.cursor, self.database.conn)
      self.weeks_log_frame.draw()

    if check_new_version():
      if messagebox.showinfo("Update Available", f"A new version of this app is available!\n\nv{CURRENT_VERSION} -> v{get_remote_version(REMOTE_URL)}\n\nPlease click ok for the installation to begin. The app will close and reopen automatically after the update."):
        install_new_version(self)

    self.mainloop()

  def open_settings(self):
    self.withdraw()
    Settings(self)

  def open_help(self):
    print("TODO help")

  def open_report_bug(self):
    webbrowser.open_new_tab("https://docs.google.com/forms/d/e/1FAIpQLSdgcSgDJqZkh0PHvuEgpQuhq07JhnfQNFKfcyhdwx-WRJWm0g/viewform?usp=sharing&ouid=107040900145910921050")

  def on_closing(self):
    self.database.close()
    self.destroy()
    sys.exit()

if __name__ == "__main__":
  main = Main()