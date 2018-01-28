from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Bet365Scraper():
    def __init__(self):
        """
        Scraper class, used for extracting games information from
        """
        self.driver = None

    def connect(self, url='https://www.bet365.com/en/'):
        """
        Connects to the Bet365 initial page
        :param url: url of the website
        :return: None
        """
        try:
            self.driver = webdriver.Firefox()
            self.driver.get(url)
        except Exception as e:
            print(e)

    def disconnect(self):
        """
        Disconnect from website and close driver
        :return: None
        """
        self.driver.close()

    def travel_to_games_list(self):
        """
        This function uses selenium to travel from the main page to the one containing obbs of the
        major games in Europe
        :return:
        """
        # click on sports banner, once it is loaded
        sports_banner = WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID, 'dv1')))
        sports_banner.click()
        # click on 'Elite Euro List', once previous page is loaded
        top_coupons = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'tc-TopCouponStemRenderer')))
        top_coupons.find_elements_by_class_name('tc-TopCouponLinkButton')[1].click()
        # change odds to decimal
        odds_selector = WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'hm-OddsDropDownSelections.hm-DropDownSelections')))
        odds_selector.click()
        odds_items = WebDriverWait(self.driver,5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'hm-DropDownSelections_Item')))
        odds_items[1].click()

    def _get_major_leagues(self):
        """
        Returns a list of the major league matches, each of to be further preprocessed
        :return: list of major league matches
        """
        return WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'gl-MarketGroup.cm-CouponMarketGroup')))

    def _get_matches_from_league(self, league):
        """

        :param league:
        :return:
        """
        # extract title of the league
        league_title = str(league.find_element(By.CLASS_NAME, 'cm-CouponMarketGroupButton_Title').text)
        # get grid, containing matches, times and odds
        matches_odds_grid = league.find_element(By.CLASS_NAME, 'gl-MarketGroup_Wrapper')

        # extract matches and odds from grid
        matches_row = matches_odds_grid.\
            find_element(By.CLASS_NAME, 'sl-MarketCouponFixtureLabelBase.gl-Market_HasLabels')
        [odds_1_row, odds_X_row, odds_2_row] = matches_odds_grid.\
            find_elements(By.CLASS_NAME, 'sl-MarketCouponValuesExplicit33')


if __name__ == '__main__':
    bet_scraper = Bet365Scraper()
    bet_scraper.connect()
    bet_scraper.travel_to_games_list()
    print(len(bet_scraper._get_major_leagues()))
