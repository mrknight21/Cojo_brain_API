from gui import *
import configparser
import downloader
import subprocess
import os


class App:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.downloader = downloader.Downloader()
        self.download_location = os.getcwd()+"\Downloads\\"

        root = self.root = Gui(title="URL Link Grabber")
        root.set_version("Version 0.2 6-11-2017")

        root.window.protocol("WM_DELETE_WINDOW", self.quit)

        root.button_get_links.config(command=self.get_links)
        root.button_filter.config(command=self.filter)
        root.button_save.config(command=self.save_links)
        root.button_show_in_explorer.config(command=self.open_explorer)
        root.window.bind('<Return>', self.get_links)

    @staticmethod
    def ignore_event(_):
        return 'break'

    def nyaa_settings(self):
        self.root.entry_url_string.set("https://nyaa.si/?f=0&c=1_2&q=Hellsing+Ultimate")
        # self.root.entry_url_string.set("https://nyaa.si/")
        # self.root.entry_filter_string.set("download")
        self.root.set_title("Nyaa.se downloader")

    def get_links(self, *_):
        url = self.root.entry_url_string.get()
        window = self.root.window
        window.bind('<Return>', self.ignore_event)
        self.root.button_get_links.config(relief=SUNKEN)
        print("Disabled input")
        print("Parsing:", url)
        self.downloader.get_links(url)
        if len(self.root.entry_filter_string.get()) != 0:
            self.filter()
        else:
            self.text_show()

        window.after(1000, lambda: self.reset_button(self.root.button_get_links, self.get_links, '<Return>'))

    def save_links(self):
        self.downloader.save_links(self.download_location)

    def filter(self, *_):
        print("Filtering")
        str_filter = self.root.entry_filter_string.get()
        self.downloader.sanitize_list(str_filter)
        self.text_show()

    def text_show(self):
        sorted_by_seeds = sorted(self.downloader.current_torrent_list, key=lambda k: k['seeders'], reverse=True)
        self.root.table.delete(*self.root.table.get_children())
        for torrent in sorted_by_seeds:
            self.root.table.insert('', 'end', text=torrent['title'],
                                   values=(
                                       torrent['size'],
                                       torrent['seeders'],
                                       torrent['date']
                                   ))

    def open_explorer(self, *_):
        print(self.download_location)
        print('explorer "'+self.download_location+'"')
        subprocess.Popen('explorer "'+self.download_location+'"')

    def reset_button(self, button, command, key=None):
        if key:
            self.root.window.bind(key, command)
        button.config(relief=RAISED)
        print('\nReady for more input')

    def quit(self):
        self.root.quit()

app = App()
app.nyaa_settings()
app.root.window.mainloop()

