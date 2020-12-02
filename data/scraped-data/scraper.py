import requests
from bs4 import BeautifulSoup
import os
from csv import DictWriter
import time
import pandas as pd
from datetime import datetime as dt

class Scraper:
    def __init__(self, csv_dir):
        self.field_names = ['name_english', 'name_japanese', 'show_type', 'episodes', 'status', 'aired', 'broadcast_time', 'producers', 
                       'licensors', 'studios', 'source', 'genres', 'episode_length', 'rating', 'score_and_scorers', 
                       'members', 'favorites', 'description']

        self.csv_dir = csv_dir
        self.date = dt.today().strftime(r'%d-%m-%Y')
        self.df = None

    def __parseList(self, element):
        ret_list = [a.text for a in element.find_all('a')]
        
        return ", ".join(ret_list)

    def __parseLabel(self, element):
        string = element.text
        
        split_colens = string.split(':')
        removed_label = split_colens[1:]
        
        for i, label in enumerate(removed_label):
            removed_label[i] = label.replace('\n', '').strip()
        
        joined = " ".join(removed_label)
        
        return joined

    def __createRow(self, url):
        ret_dict = {field_name: '' for field_name in self.field_names}

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html.parser')

        side_panel = soup.find('td', class_='borderClass')
        side_panel_subdiv = side_panel.find('div')
        side_panel_divs = side_panel_subdiv.find_all('div')

        try:
            ret_dict['description'] = soup.find('p', itemprop='description').text

        except Exception as e:
            print(f"Encountered an error '{e}' for description at '{url}'.")

        for panel in side_panel_divs:
            try:
                split = str(panel.text.split(':')[0].strip())

                if split == "English":
                    ret_dict['name_english'] = self.__parseLabel(panel)

                if split == "Japanese":
                    ret_dict['name_japanese'] = self.__parseLabel(panel)

                if split == "Type":
                    ret_dict['show_type'] = self.__parseLabel(panel)

                if split == "Episodes":
                    ret_dict['episodes'] = self.__parseLabel(panel)

                if split == "Status":
                    ret_dict['status'] = self.__parseLabel(panel)

                if split == "Aired":
                    ret_dict['aired'] = self.__parseLabel(panel)

                if split == "Broadcast":
                    ret_dict['broadcast_time'] = self.__parseLabel(panel)

                if split == "Producers":
                    ret_dict['producers'] = self.__parseList(panel)

                if split == "Licensors":
                    ret_dict['licensors'] = self.__parseList(panel)

                if split == "Studios":
                    ret_dict['studios'] = self.__parseList(panel)

                if split == "Source":
                    ret_dict['source'] = self.__parseLabel(panel)

                if split == "Genres":
                    ret_dict['genres'] = self.__parseList(panel)

                if split == "Duration":
                    ret_dict['episode_length'] = self.__parseLabel(panel)

                if split == "Rating":
                    ret_dict['rating'] = self.__parseLabel(panel).split(' ')[0]

                if split == "Score":
                    ret_dict['score_and_scorers'] = ", ".join([part.text for part in panel.find_all('span')][1:])

                if split == "Members":
                    ret_dict['members'] = "".join(self.__parseLabel(panel).split(','))

                if split == "Favorites":
                    ret_dict['favorites'] = "".join(self.__parseLabel(panel).split(','))

            except Exception as e:
                print(f"Encountered an error '{e}' at '{url}'.")

        return ret_dict

    def buildCSV(self, end_page, start_page=0):
        link = 'Unknown'
                
        for i in range(start_page, end_page):
            
            print(f"Scraping page {i}...")

            csv_filename = f"anime-{self.date}-{i}.csv"
            csv_path = os.path.join(self.csv_dir, csv_filename)

            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = DictWriter(csvfile, fieldnames=self.field_names)
                
                writer.writeheader()

                url_page = f"https://myanimelist.net/topanime.php?limit={i*50}"
                req_list = requests.get(url_page)
                soup_list = BeautifulSoup(req_list.content, 'html.parser')
                shows = soup_list.find_all('tr', class_='ranking-list')

                for show in shows:
                    try:
                        link = show.find('a').get('href')
                        data_row = self.__createRow(link)
                        writer.writerow(data_row)

                        time.sleep(2) # These are required to stop the website from blocking us

                    except Exception as e:
                        print(f"Encountered error '{e}' at '{link}'.")
                        
                        time.sleep(2)
        
        print("Dataset creation completed successfully.")

    def __parseRatingCol(self, rating):
        if rating == 'None':
            return 'R+' # We do this because if a show is unlabelled, then only people who can watch any show, being R+ can watch this unclassified rating

    # This will parse our episode length column and return the amount of minutes the show lasted for
    def __parseEpLenCol(self, time_raw):
        try:
            time_split = time_raw.split(' ')

            # This will be the condition if it contains a sec
            if time_split[1] == 'sec.':
                return 1

            # This will be our condition if it contains a min
            elif time_split[1] == 'min.':
                return int(time_split[0])

            # These will be the conditions if it contains an hr
            elif time_split[1] == 'hr.':

                if len(time_split) > 2:

                    if time_split[3] == 'min.':
                        return 60 * int(time_split[0]) + int(time_split[2])

                return 60 * int(time_split[0])

        except:
            return pd.NaT

    def __parseEpisodesCol(self, episodes):
        try:
            return int(episodes)
        
        except:
            return pd.NaT

    def compileDF(self):
        dfs = []
        for csv in os.listdir(self.csv_dir):
            dfs.append(pd.read_csv(os.path.join(self.csv_dir, csv)))

        self.df = pd.concat(dfs)

        kept_columns = ['name_english', 'name_japanese', 'show_type', 'episodes', 'producers', 'licensors', 'studios', 'genres', 'episode_length', 'rating', 'description']
        self.df = self.df[kept_columns]

        # Data manipulating and cleaning
        self.df['episode_length'] = self.df['episode_length'].apply(self.__parseEpLenCol)
        self.df['episodes'] = self.df['episodes'].apply(self.__parseEpisodesCol)

        # Still potentially might need a way to parse the rating and the show_type columns - might use k-means-clustering to classify the ratings and show types 

        return self.df