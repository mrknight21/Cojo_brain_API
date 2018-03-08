import urllib.request
import cgi
import os
import multithreader
from bs4 import BeautifulSoup


class Downloader:

    def __init__(self):
        self.orig_torrent_list = []
        self.current_torrent_list = []
        self.threads = multithreader.MultiThreader(command=self.thread_save_links, num_threads=5)
        self.url_head = ''

    # example 'https://www.nyaa.se/?page=search&cats=1_37&filter=2&term=MASAMUNE-KUN+NO+REVENGE+1080p'
    def get_links(self, url):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
            response = urllib.request.urlopen(request)
            html = response.read().decode("utf-8")
        except Exception as e:
            empty_torrent_list = self.create_empty_list()
            empty_torrent_list[0]['title'] = "Error in URL: " + str(e)
            self.current_torrent_list = empty_torrent_list
            print(self.current_torrent_list)
            return

        self.url_head = self.get_url_head(url)

        i = html.find("<tbody>")  # go to body
        j = html.find("</tbody", i+7)  # find end

        table_body = BeautifulSoup(html[i:j+9], 'html.parser')
        table_rows = table_body.find_all('tr')

        self.orig_torrent_list = self.categorize_links(table_rows)
        self.current_torrent_list = self.orig_torrent_list[:]

    def categorize_links(self, table_rows):
        torrent_list = []
        for row in table_rows:
            torrent = {}
            column = row.find_all('td', recursive=False)
            torrent['title'] = column[1].find('a', class_=None).string
            torrent['link'] = column[2].find('a')['href']
            if torrent['link'][0] == '/':
                torrent['link'] = self.url_head + torrent['link']
            torrent['link-magnet'] = column[2].find('a').find_next_sibling('a')['href']
            torrent['size'] = column[3].string
            torrent['date'] = column[4].string
            torrent['seeders'] = int(column[5].string)
            torrent['downloaded'] = column[6].string
            torrent_list.append(torrent)
        return torrent_list

    @staticmethod
    def create_empty_list():
        my_list = []
        my_dictionary = {}
        keys = ['title', 'link', 'link-magnet', 'size', 'date', 'seeders', 'downloaded']
        for key in keys:
            my_dictionary[key] = ''
        my_list.append(my_dictionary)
        return my_list

    @staticmethod
    def get_url_head(url):
        pos1 = url.find('://')
        if pos1 != -1:
            pos2 = url.find('/', pos1+3)
            return url[:pos2]
        elif url.find('/'):
            return url[:url.find('/')]
        else:
            return url

    def sanitize_list(self, my_filter):
        new_list = []
        if len(my_filter) == 0:  # clear filter
            self.current_torrent_list == self.orig_torrent_list
            return
        for torrent in self.orig_torrent_list:
            title = torrent['title']
            if title.find(my_filter) != -1:  # now see if this is what we want
                new_list.append(torrent)
        self.current_torrent_list = new_list

    def save_links(self, path):
        command_list = []
        for torrent in self.current_torrent_list:
            link = torrent['link']
            command_list.append((link, path))
        self.threads.start(command_list)

    # example C:/Users/Sean Z/Downloads/Autodownload/
    @staticmethod
    def thread_save_links(link, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            response = urllib.request.urlopen(link)
            _, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
            filename = urllib.parse.unquote(params['filename'])
            if not os.path.isfile(path + filename):
                output_file = open(path + filename, "wb")
                output_file.write(response.read())
                output_file.close()
                print("Saved: ", filename)
            else:
                print("Already Exists:", path + filename)
        except Exception as e:
            print(e)
