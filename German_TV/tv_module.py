import requests
from bs4 import BeautifulSoup
import pandas as pd
import settings as s



class TvScraper:

    def __init__(self):
        self.soup = None
        self.titles_list = []
        self.genres_list = []
        self.times_list = []
        self.channels_list = []

    def process_html(self, page):
        url = "https://www.tvspielfilm.de/tv-programm/sendungen/?page=" + str(page) + "&order=title&date=" + "thisWeek" + "&freetv=1&cat%5B%5D=SE&time=day&channel="
        source_code = requests.get(url)
        plain_text = source_code.text
        self.soup = BeautifulSoup(plain_text, "lxml")

    def get_titles(self):
        added_title = "off"
        for link in self.soup.findAll('td', {'class': 'col-3'}):
            title = link.text
            title = title.rstrip()
            title = title.lstrip()
            letter_index = 0
            for letter in title:
                if letter == ' ' and title[letter_index +1] == ' ':
                    only_title = title[:letter_index]
                    self.titles_list.append(only_title)
                    added_title = "on"
                    break
                else:
                    letter_index += 1
            if added_title == "off":
                self.titles_list.append(title)
            else:
                added_title = "off"

    def get_genres(self):
        for link in self.soup.findAll('td', {'class': 'col-4'}):
                genre = link.text
                self.genres_list.append(genre[1:-1])

    def get_times(self):
        for link in self.soup.findAll('td', {'class': 'col-2'}):
            time = link.text
            time = time.rstrip()
            time = time.lstrip()
            time = time.replace('\n', ' ')
            self.times_list.append(time)

    def get_channels(self):
        for link in self.soup.findAll('td', {'class': 'programm-col1'}):
            anchor = link.findChildren("a" , recursive=False)
            anchor = anchor[0]
            anchor_attributes = anchor.attrs
            self.channels_list.append(anchor_attributes["title"][:-9])


class TvFilter:

    def __init__(self):
        self.final_channels_list = []
        self.final_titles_list = []
        self.final_genres_list = []
        self.final_times_list = []
        self.my_series_titles = []
        self.my_series_genres = []
        self.my_series_channels = []
        self.my_series_times = []

    def filter_my_channels(self, 
                        channels_list,
                        titles_list,
                        genres_list,
                        times_list):
        index_list = []
        for index, channel in enumerate(channels_list):
            if channel in s.MY_FREE_CHANNELS:
                self.final_channels_list.append(channel)
                index_list.append(index)
        for digit in index_list:
            self.final_titles_list.append(titles_list[digit])
            self.final_genres_list.append(genres_list[digit])
            self.final_times_list.append(times_list[digit])

    def filter_my_series(self):
        for index, final_title in enumerate(self.final_titles_list):
            title = final_title.lower()
            for my_title in s.MY_SERIES:
                if my_title in title:
                    self.my_series_titles.append(self.final_titles_list[index])
                    self.my_series_genres.append(self.final_genres_list[index])
                    self.my_series_channels.append(self.final_channels_list[index])
                    self.my_series_times.append(self.final_times_list[index])


class TvResultsSaver:

    def save_as_df(self, 
                    final_titles_list,
                    final_genres_list,
                    final_channels_list,
                    final_times_list, 
                    today,
                    df_name):
        results_dataframe = pd.DataFrame({'Title': final_titles_list,
                                        'Genre': final_genres_list,
                                        'Program': final_channels_list,
                                        'Time': final_times_list
                                        })
        results_dataframe.to_csv(df_name + '_' + today + '.tsv', sep="	")