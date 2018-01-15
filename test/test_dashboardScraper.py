from __future__ import print_function

import unittest

from dashboardScraper import DashboardScraper


class TestDashboardScraper(unittest.TestCase):

    def test_connection(self):
        scraper = DashboardScraper()
        scraper.connect()
        self.assertEqual(scraper.driver.title,'Current Opportunities')
        scraper.disconnect()

    def test_games_odd_matrices(self):
        scraper = DashboardScraper()
        scraper.connect()

        games = scraper.get_games_elements()
        odd_matrices = scraper.get_odd_matrices()
        self.assertEqual(len(games),len(odd_matrices))
        scraper.disconnect()
