"""
Author: Nody Peng
Date: 2024 09 01
Description: This script is a YouTube to MP3 converter application using Tkinter for the GUI and yt-dlp for downloading and converting videos.

License: MIT License
Copyright (c) 2019 Nody Peng

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class YouTubeMP3ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to MP3 Converter")
        
        # Set fixed size for the window
        self.root.geometry("600x500")  # Set the size as per your requirement
        self.root.resizable(False, True)  # Disable resizing of the window


        ### Something wrong with Set app icon.
        # # Set application icon
        # self.set_window_icon("youtube-to-mp3.png")
        
        # Variables
        self.links = []
        self.output_folder = tk.StringVar()

        # UI Elements
        self.create_widgets()

    # def set_window_icon(self, icon_path):
    #     # Load the icon image
    #     self.icon_image = tk.PhotoImage(file=icon_path)
    #     # Set the icon for the window
    #     self.root.iconphoto(True, self.icon_image)
        
    def create_widgets(self):
        # Add Link Entry
        self.link_label = tk.Label(self.root, width=50, text="請輸入歌曲連結: ")
        self.link_label.pack(pady=5)
        self.link_entry = tk.Entry(self.root, width=50)
        self.link_entry.pack(pady=5)
        self.add_link_button = tk.Button(self.root, text="新增歌曲連結", command=self.add_link)
        self.add_link_button.pack(pady=5)

        # Links Listbox with Entry for MP3 name
        self.links_frame = tk.Frame(self.root)
        self.links_frame.pack(pady=0, fill=tk.X)

        # Label for MP3 name Entry
        self.mp3_name_label = tk.Label(self.links_frame, text="請輸入歌曲名稱(預設為YouTube影片原名)", anchor='e')
        self.mp3_name_label.pack(pady=0, fill=tk.X, anchor='e')

        # Frame for Listbox and Entry widgets
        self.links_listbox_frame = tk.Frame(self.links_frame)
        self.links_listbox_frame.pack(pady=5, fill=tk.X)

        self.links_listbox = tk.Listbox(self.links_listbox_frame, selectmode=tk.SINGLE, width=50, height=10)
        self.links_listbox.pack(side=tk.LEFT, fill=tk.Y, anchor='w')

        self.name_entries_frame = tk.Frame(self.links_listbox_frame)
        self.name_entries_frame.pack(side=tk.LEFT, fill=tk.Y, anchor='w')

        self.name_entries = []

        self.delete_link_button = tk.Button(self.root, text="刪除選擇連結", command=self.delete_link)
        self.delete_link_button.pack(pady=5)

        # Background Label for Output Folder Path
        self.bg_frame = tk.Frame(self.root, bg='lightgray', padx=10, pady=10)
        self.bg_frame.pack(pady=5, fill=tk.X)

        # Output Folder Label with Background
        self.output_folder_label = tk.Label(self.bg_frame, textvariable=self.output_folder, bg='lightgray', font=('Arial', 12))
        self.output_folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Select Folder Button
        self.select_folder_button = tk.Button(self.root, text="選擇.mp3輸出資料夾", command=self.select_output_folder)
        self.select_folder_button.pack(pady=5)

        # Convert Button
        self.convert_button = tk.Button(self.root, text="轉換成MP3", command=self.convert_links)
        self.convert_button.pack(pady=10)

    def add_link(self):
        link = self.link_entry.get()
        if link:
            self.links.append(link)
            self.links_listbox.insert(tk.END, link)
            
            # Add an Entry widget for MP3 file name next to the Listbox
            name_entry = tk.Entry(self.name_entries_frame, width=30)
            name_entry.pack(pady=2, anchor='w')
            self.name_entries.append(name_entry)

            self.link_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a YouTube link.")

    def delete_link(self):
        try:
            selected_index = self.links_listbox.curselection()[0]
            self.links_listbox.delete(selected_index)
            self.name_entries[selected_index].destroy()
            del self.name_entries[selected_index]
            del self.links[selected_index]
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a link to delete.")

    def select_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder.set(folder_selected)

    def convert_links(self):
        output_path = self.output_folder.get()
        if not output_path:
            messagebox.showwarning("Folder Error", "Please select an output folder.")
            return

        if not self.links:
            messagebox.showwarning("Link Error", "No links to convert.")
            return

        for link, name_entry in zip(self.links, self.name_entries):
            file_name = name_entry.get() or '%(title)s'
            self.download_youtube_as_mp3(link, output_path, file_name)
        
        messagebox.showinfo("Success", "Conversion completed!")

    def download_youtube_as_mp3(self, youtube_url, output_path, file_name):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, file_name + '.%(ext)s'),
            'ffmpeg_location': 'C:/軟體/FFMPEG/ffmpeg-7.0.2-full_build/ffmpeg-7.0.2-full_build/bin',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeMP3ConverterApp(root)
    root.mainloop()
