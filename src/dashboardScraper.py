from __future__ import print_function

from collections import namedtuple
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By



class DashboardScraper():
    def __init__(self):
        """
        Scraper class, interacting with the sporting dashboard on http://184.73.28.182/
        """
        # set up chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.expanded_mode = False

    def connect(self, url='http://184.73.28.182/'):
        """
        Connects to the dashboard
        :param url: url of the sporting arbitrage dashboard
        :return: None
        """
        try:
            self.driver.get(url)
        except Exception as e:
            print(e)

    def refresh(self):
        """
        Refreshes the page
        :return:
        """
        try:
            self.driver.refresh()
        except Exception as e:
            print(e)

    def disconnect(self):
        """
        Disconnect from dashboard and close driver
        :return: None
        """
        self.driver.close()

    def get_json_data(self):
        """
        Returns data about the current games in json format
        :return:
        """
        # refresh page before collecting data
        self.refresh()
        games = self._get_games_elements()
        self._expand_games(games)
        odds_matrices = self._get_odd_matrices()

        games_info = []
        for game, odds_matrix in zip(games, odds_matrices):
            info = {}
            info['game'] = self._get_info_from_game(game)
            info['odds_matrix'] = self._get_info_from_odds_matrix(odds_matrix)
            games_info.append(info)

        return games_info

    def get_tuples_data(self):
        """
        Returns data from dashbouard as a list of namedtuples, each of which containes the following fields:

            * timestamp     : string containing the query time
            * date          : string containing the date of the match
            * game          : match between the teams
            * league        : league in which the teams are playing
            * odd_matrix    : pandas DataFrame, having as index 1 X 2, as columns the different bookies and as values
                              the odds offered by the bookies

        :return: list of namedtuples
        """
        # refresh page before collecting data
        self.refresh()
        games = self._get_games_elements()
        self._expand_games(games)
        odds_matrices = self._get_odd_matrices()
        # obtain list of namedtuples
        scraped_games = []
        for game, odds_matrix in zip(games, odds_matrices):
            scraped_games.append(self._get_tuple_from_game(game, odds_matrix))
        return scraped_games

    def _get_tuple_from_game(self, game, odd_matrix):
        """
        Function which extracts information from game and odd_matric selenium elements, and returns a namedtuple with
        the following fields:
            * timestamp     : string containing the query time
            * date          : string containing the date of the match
            * game          : match between the teams
            * league        : league in which the teams are playing
            * odd_matrix    : pandas DataFrame, having as index 1 X 2, as columns the different bookies and as values
                              the odds offered by the bookies
        :param game: selenium element, containing the game information
        :param odd_matrix: selenium element, containing the matrix of odds
        :return: namedtuple, with fields specified above
        """
        # initialize named tuple
        scraped_game = namedtuple('ScrapedGame',  ['timestamp', 'date', 'game', 'league', 'odd_matrix'])
        # fill values in named tuple from game
        game_contents = [element.text for element in game.find_elements_by_css_selector('td')]
        scraped_game.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scraped_game.date = str(game_contents[4])
        scraped_game.game = str(game_contents[1])
        scraped_game.league = str(game_contents[2])
        # get single rows from odd matrix
        table = odd_matrix.find_element(By.CLASS_NAME, 'accordian-body').find_element(By.CLASS_NAME, 'table-striped')
        table_body = table.find_element(By.CSS_SELECTOR,'tbody')
        table_body_elements = table_body.find_elements(By.CSS_SELECTOR, 'tr')
        # add column in scraped_odd_matrix, containing the bookie as column name, and odds as values
        scraped_odd_matrix = pd.DataFrame(index=['1', 'X', '2'])
        for body in table_body_elements:
            body_elements = body.find_elements(By.CSS_SELECTOR, 'td')
            bookie = str(body_elements[0].text)
            odds_1 = body_elements[1].text.split('\n')[0]
            odds_X = body_elements[2].text.split('\n')[0]
            odds_2 = body_elements[3].text.split('\n')[0]
            scraped_odd_matrix[bookie] = pd.Series([odds_1, odds_X, odds_2], index=scraped_odd_matrix.index)
        scraped_game.odd_matrix = scraped_odd_matrix
        return scraped_game

    def _get_games_elements(self):
        """
        Returns a list of all games
        :return: list of all games
        """
        try:
            container_element = self.driver.find_element_by_class_name('container')
            table_element = container_element.find_element_by_css_selector('table.table-striped')
            games = table_element.find_elements_by_class_name('accordion-toggle')
            return games
        except Exception as e:
            print(e)

    def _expand_games(self, games):
        """
        Expands all games, in order to show odds matrix
        :param games: list of available games
        :return: None
        """
        try:
            # click over each game container, in order to expand it
            for game in games:
                game.click()
            # notify that a click has been done
            self.expanded_mode = not self.expanded_mode
        except Exception as e:
            print(e)

    def _get_odd_matrices(self):
        """
        Returns list of all odd matrices
        :return:
        """
        try:
            container_element = self.driver.find_element_by_class_name('container')
            table_element = container_element.find_element_by_css_selector('table.table-striped')
            odd_matrices = table_element.find_elements_by_class_name('hiddenRow')
            return odd_matrices
        except Exception as e:
            print(e)

    def _get_info_from_game(self, game):
        """
        Extract info from game and returns dictionary with fields: timestamp | sport | match_title |
        league | result_to_bet | date | time_to_match | best_bookie | best_odds | mean | median
        :param game: game from which information should be extracted
        :return: dictionary, containing the information
        """
        try:
            game_contents = [element.text for element in game.find_elements_by_css_selector('td')]

            game_info = {}
            game_info['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            game_info['sport'] = str(game_contents[0])
            game_info['match_title'] = str(game_contents[1])
            game_info['league'] = str(game_contents[2])
            game_info['result_to_bet'] = str(game_contents[3])
            game_info['date'] = str(game_contents[4])
            game_info['time_to_match'] = str(game_contents[5])
            game_info['best_bookie'] = str(game_contents[6])
            game_info['best_odds'] = float(game_contents[7])
            game_info['mean'] = float(game_contents[8].split('/')[0].strip())
            game_info['median'] = float(game_contents[8].split('/')[1].strip())
            return game_info
        except Exception as e:
            print(e)

    def _get_info_from_odds_matrix(self, odds_matrix):
        """
        Extracts info from odds_matrix and returns an array of named tuples, each having the following fields:
        bookie | odds_1 | timestamp_1 | odds_X | timestamp_X | odds_2 | timestamp_2
        :param odds_matrix: element containing the odds_matrix
        :return: Array of named tuples
        """
        # extract rows from odds_matrix (in table_body_elements
        table = odds_matrix.find_element(By.CLASS_NAME, 'table-striped.table-bordered')
        table_body = table.find_element(By.CSS_SELECTOR,'tbody')
        table_body_elements = table_body.find_elements(By.CSS_SELECTOR, 'tr')
        # for each element, extract information and return named tuple
        odds_info_array = []
        for body in table_body_elements:
            body_elements = body.find_elements(By.CSS_SELECTOR, 'td')
            odds_info = {}
            odds_info['bookie'] = str(body_elements[0].text)
            odds_info['odds_1'] = float(body_elements[1].text.split('\n')[0])
            odds_info['timestamp_1'] = str(body_elements[1].text.split('\n')[1])
            odds_info['odds_X'] = float(body_elements[2].text.split('\n')[0])
            odds_info['timestamp_X'] = str(body_elements[2].text.split('\n')[1])
            odds_info['odds_2'] = float(body_elements[3].text.split('\n')[0])
            odds_info['timestamp_2'] = str(body_elements[3].text.split('\n')[1])
            odds_info_array.append(odds_info)

        return odds_info_array

if __name__ == '__main__':

    scraper = DashboardScraper()
    scraper.connect()

    games = scraper.get_tuples_data()

    for game in games:
        print(game.odd_matrix)

    scraper.disconnect()