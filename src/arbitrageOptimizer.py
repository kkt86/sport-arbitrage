import pandas as pd


class ArbitrageOptimizer:
    def __init__(self):
        # initialize variables for game data
        self._best_bookie = None
        self._best_odds = None
        self._date = None
        self._league = None
        self._match_title = None
        self._odds_mean = None
        self._odds_median = None
        self._result_to_bet = None
        self._time_to_match = None
        self._odds_matrix = None

    def load_game(self, game):
        """
        This function loads information about the game and odd matrix into the class private variables
        :param game: game as dictionary
        :return: None
        """
        self._extract_game(game)
        self._extract_odd_matrix(game)

    def get_optimal_ratio(self):
        """
        Computes the optimal ratio of the capital to bet, according to the Kelly criteria:

        ratio = (best_odds - mean_odds)/((best_odds - 1)*mean_odds)
        :return: optimal ratio as float
        """
        try:
            best_odds = float(self._best_odds)
            mean_odds = float(self._odds_mean)
            return (best_odds - mean_odds)/((best_odds-1)*mean_odds)
        except ValueError:
            return 0.0

    def get_arbitrage_opportunity(self):
        """
        This function evaluates if there exist an arbitrage opportunity in the current game, and if yes, returns the
        the amounth to be bet on each odd
        :return:
        """
        try:
            # get max odds for each outcome
            max_odds = self._odds_matrix.max(axis=1)
            # check if the sum of the inverses of the max odds is less then one, if yes, arbitrage opportunity exists
            sum_inverse_odds = sum(1/max_odds)
            if sum_inverse_odds >= 1.:
                # no arbotrage exists for this game
                return {'arbitrage': 'no'}
            else:
                # arbitrage exists for this game
                output = {'abitrage' : 'yes'}
                # compute arbitrage profit
                output['profit'] = 1 - sum_inverse_odds
                # get bookies for best odds
                bookie_odds_1 = self._odds_matrix.columns[self._odds_matrix.loc['1'] == max_odds.loc['1']][0]
                bookie_odds_X = self._odds_matrix.columns[self._odds_matrix.loc['X'] == max_odds.loc['X']][0]
                bookie_odds_2 = self._odds_matrix.columns[self._odds_matrix.loc['2'] == max_odds.loc['2']][0]
                # compute amounth to bet on each outcome
                probabilities = 1/max_odds
                amounth_1 = probabilities['1']/sum(probabilities)
                amounth_X = probabilities['X']/sum(probabilities)
                amounth_2 = probabilities['2']/sum(probabilities)
                bet = {}
                bet['1'] = {'bookie': bookie_odds_1, 'bet_size': amounth_1, 'odds': max_odds['1']}
                bet['X'] = {'bookie': bookie_odds_X, 'bet_size': amounth_X, 'odds': max_odds['X']}
                bet['2'] = {'bookie': bookie_odds_2, 'bet_size': amounth_2, 'odds': max_odds['2']}
                output['bet'] = bet
                return output
        except ValueError:
            return {'arbitrage': 'no'}

    def _extract_game(self, game):
        """
        This function extracts information about the game (from json format)
        and stores it into the class private variables
        :param game: game as dictionary
        :return: None
        """
        self._best_bookie = game['game']['best_bookie']
        self._best_odds = game['game']['best_odds']
        self._date = game['game']['date']
        self._league = game['game']['league']
        self._match_title = game['game']['match_title']
        self._odds_mean = game['game']['mean']
        self._odds_median = game['game']['median']
        self._result_to_bet = game['game']['result_to_bet']
        self._time_to_match = game['game']['time_to_match']

    def _extract_odd_matrix(self, game):
        """
        This function extracts the odd matrix from the dictionary and loads it into private variable
        :param game: game as dictionary
        :return: None
        """
        odd_matrix = pd.DataFrame(index=['1', 'X', '2'])
        for bookie_odds in game['odds_matrix']:
            bookie = bookie_odds['bookie']
            odds_1 = bookie_odds['odds_1']
            odds_X = bookie_odds['odds_X']
            odds_2 = bookie_odds['odds_2']
            odd_matrix[bookie] = pd.to_numeric(pd.Series([odds_1, odds_X, odds_2], index=odd_matrix.index),
                                               errors='coerce')
        self._odds_matrix = odd_matrix


if __name__ == '__main__':

    # define game in json format
    game = {'game': {'best_bookie': 'Betfair',
                     'best_odds': 2.0,
                     'date': '2018-02-03 16:00:00',
                     'league': 'Northern Ireland: Irish Cup',
                     'match_title': 'Ballyclare vs. Glentoran',
                     'mean': 1.81,
                     'median': 2.0,
                     'result_to_bet': '2',
                     'sport': 'soccer',
                     'time_to_match': '02:49:36',
                     'timestamp': '2018-02-03 13:10:23'},
            'odds_matrix': [{'bookie': '', 'odds_1': u'', 'odds_2': u'', 'odds_X': u''},
                            {'bookie': '', 'odds_1': u'3.90', 'odds_2': u'2.00', 'odds_X': u'2.88'},
                            {'bookie': 'Betfair Exchange',
                             'odds_1': u'5.02',
                             'odds_2': u'1.02',
                             'odds_X': u'1.01'},
                            {'bookie': 'BetVictor',
                             'odds_1': u'3.75',
                             'odds_2': u'4.00',
                             'odds_X': u'2.88'},
                            {'bookie': 'Paddy Power',
                             'odds_1': u'3.75',
                             'odds_2': u'2.00',
                             'odds_X': u'4.88'}]}

    arbitrageOptimizer = ArbitrageOptimizer()
    arbitrageOptimizer.load_game(game)

    print arbitrageOptimizer.get_optimal_ratio()
    print arbitrageOptimizer.get_arbitrage_opportunity()





