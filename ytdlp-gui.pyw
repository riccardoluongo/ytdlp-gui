from __future__ import unicode_literals
import sys
from tkinter import Tk, Button, Frame
from tkinter.scrolledtext import ScrolledText
import tkinter
from tkinter import *
from yt_dlp import *
from tkinter import filedialog
import os
from tkinter import messagebox
import traceback
import logging
import logging.handlers
from datetime import datetime
from threading import Thread
from tkinter.scrolledtext import ScrolledText
from dotenv import *
from tkinter import Menu

config = dotenv_values(".env")

if config['check_for_ffmpeg'] == "on":
    os.system("choco install ffmpeg-full -y")

now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

logging.basicConfig(filename=f'Logs/{dt_string}.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level='DEBUG')
logging.info(f'{dt_string} - Program started.')

logs_folder_path = "Logs/"
files = os.listdir(logs_folder_path)
if len(files) > int(config['max_log_files']):
   oldest_file = min(files, key=lambda x: os.path.getctime(os.path.join(logs_folder_path, x)))
   os.remove(os.path.join(logs_folder_path, oldest_file))
   print(f"{oldest_file} was deleted from folder {logs_folder_path}.")
else:
   print(f"{logs_folder_path} folder contains less than {config['max_log_files']} files.")

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def progr_hook(d):
        def my_hook(d):
            if d['status'] == 'downloading':
               print(d['_percent_str']+" ETA:"+d['_eta_str']+" Speed:" + d['_speed_str'])
            if d['status'] == 'finished':
               print('Finishing the download...')   
        Thread(target=my_hook(d)).start()

def on_change(e):
    def download_thread():
        global filename
        if clicked.get() == "MP3":
            if savedir == "":
                messagebox.showwarning(title="ytdlp-gui by Riccardo Luongo", message="No download folder selected!")
                return
            global open_format
            open_format = '.mp3'
            print("Downloading video as " + clicked.get())
            logging.info(f'{dt_string} - Starting the download...')
            global ydl_opts
            ydl_opts = {
            'progress_hooks' : [progr_hook],
            'logger' : MyLogger(),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                f'preferredcodec': config['audio_codec'],
                f'preferredquality': config['audio_quality'],
            }],
            'outtmpl': f'{savedir}/%(title)s'
            }
            with YoutubeDL(ydl_opts) as ydl:
             try:
                  ydl.download(e.widget.get())
                  global meta
                  meta = ydl.extract_info(e.widget.get()) 
                  filename =  ('%s' %(meta['title']))
                  logging.info(f'{dt_string} - Download completed.') 
             except:
                messagebox.showerror(title='ytdlp-gui by Riccardo Luongo', message=f'''An error occurred during the download.
        Check the logs for further information''')
                pop.destroy
                logging.error(f"{dt_string} - An error occurred during the download. {traceback.format_exc()}")
            popup()
            clear_text()
                
        elif clicked.get() == "MP4":
                if savedir == "":
                    messagebox.showwarning(title="ytdlp-gui by Riccardo Luongo", message="No download folder selected!")
                    return
                open_format = '.mp4'
                print("Downloading video as " + clicked.get())
                logging.info(f'{dt_string} - Starting the download...')
                ydl_opts = {
            'progress_hooks' : [progr_hook],
            'logger' : MyLogger(),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': f'{savedir}/%(title)s.mp4'
            }
                with YoutubeDL(ydl_opts) as ydl:
                    try:
                      ydl.download(e.widget.get())
                      meta = ydl.extract_info(e.widget.get()) 
                      filename =  ('%s' %(meta['title']))
                      logging.info(f'{dt_string} - Download completed.')
                    except:
                      messagebox.showerror(title='ytdlp-gui by Riccardo Luongo', message=f'''An error occurred during the download.
        Check the logs for further information''')
                      pop.destroy
                      logging.error(f"{dt_string} - An error occurred during the download. {traceback.format_exc()}")
                popup()
                clear_text()     
    Thread(target=download_thread).start()

def popup():
   global pop
   pop = Toplevel(app.root)
   pop.title("")
   pop.geometry("200x56")
   pop.resizable(False,False)
   pop.iconbitmap("icon.ico")

   poplabel = Label(pop, text="Download completed!")
   poplabel.place(relx=0.5, rely=0.1, anchor=CENTER)

   openfilebtn = Button(pop, text="Open file", command=open_file)
   openfilebtn.place(relx=0.36, rely=0.5, anchor=CENTER)
   
   closebtn = Button(pop, text="Close", command=pop.destroy)
   closebtn.place(relx=0.68, rely=0.5, anchor=CENTER)

def clear_text():
   e.delete(0, END)

def askdir():
   global savedir
   savedir = filedialog.askdirectory()
   cwd.config(text= savedir)

def open_file():
   os.startfile(f'{savedir}/{filename}{open_format}')

def open_settings():
    os.startfile('.env')

class PrintLogger(object):

    def __init__(self, textbox):
        self.textbox = textbox 

    def write(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", text) 
        self.textbox.see("end") 
        self.textbox.configure(state="disabled")

    def flush(self):
        pass

class MainGUI(Tk):
    def __init__(self):
        global e
        global cliptext
        Tk.__init__(self)
        self.iconbitmap("icon.ico")
        self.root = Frame(self)
        self.geometry("715x310")
        self.resizable(False, False) 
        self.title('ytdlp-gui by Riccardo Luongo')
        self.root.grid()

        menubar = Menu(self)
        file_menu = Menu(menubar, tearoff="off")
        self.config(menu=menubar)
        file_menu.add_command(
        label='Modify preferences',
        command=open_settings
        )
        menubar.add_cascade(
        label="File",
        menu=file_menu
        )
        file_menu.add_command(
        label='Quit',
        command=self.destroy
        )

        mainLabel = tkinter.Label(self.root, text='Video/playlist link:')
        mainLabel.grid(row=0, column=0)

        e  = tkinter.Entry(self.root, width=95)
        e.grid(row=1, column=0)
        e.bind("<Return>", on_change)
        bt = Button(self.root,text="Clear", command=clear_text)
        bt.grid(row=1, column=2)

        dl_info = tkinter.Label(self.root, text="Press Enter to download the video")
        dl_info.grid(row=2, column=0)
 
        frm = tkinter.LabelFrame(self.root, padx=5, pady=5)
        frm.grid(row=3, column=0)
        dir_bt = Button(frm, text="Change the download folder", command=askdir)
        dir_bt.grid(row=4, column=0)

        global cwd
        cwd = tkinter.Label(frm,text= f'''{savedir}''')
        cwd.grid(row=5, column=0)
        
        drop_frm = tkinter.LabelFrame(self.root, padx=5, pady=5)
        drop_frm.grid(row=6, column=0)
        global clicked
        clicked = tkinter.StringVar()
        clicked.set("MP4")
        drop = tkinter.OptionMenu(drop_frm, clicked, "MP3", "MP4")
        drop.grid(row=7, column=0)
        drop_label = tkinter.Label(drop_frm, text='File format')
        drop_label.grid(row=5,column=0)
        
        self.log_widget = ScrolledText(self.root, height=0, width=80, font=("consolas", "10", "normal"))
        self.log_widget.grid(row=7, column=0, padx=10, pady=10)
        self.log_widget.config(state="disabled")

        def paste():
          try: 
              e.insert(0, self.clipboard_get())
          except:
              pass
        paste_bt = Button(self.root, text="Paste", command=paste)
        paste_bt.grid(row=1, column=1, padx=5, pady=5)

        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger

savedir = config['default_folder']

if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()