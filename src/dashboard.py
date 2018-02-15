import joblib
import pandas as pd
from dashboardScraper import DashboardScraper
from arbitrageOptimizer import ArbitrageOptimizer

from bokeh.io import show, output_file
from bokeh.layouts import column, row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, DataTable, Panel, TableColumn, Tabs, TextInput
from bokeh.plotting import figure, curdoc


# load games
games = joblib.load('../data/sample.dat')


# create table of the current opportunities
def get_data_table_from_games(games):
    optimizer = ArbitrageOptimizer()
    data_match = []
    data_league = []
    data_result_to_bet = []
    data_date = []
    data_time_to_match = []
    data_best_bookie = []
    data_best_odds = []
    data_mean_median = []
    data_ratio = []

    for game in games:
        data_match.append(game['game']['match_title'])
        data_league.append(game['game']['league'])
        data_result_to_bet.append(game['game']['result_to_bet'])
        data_date.append(game['game']['date'])
        data_time_to_match.append(game['game']['time_to_match'])
        data_best_bookie.append(game['game']['best_bookie'])
        data_best_odds.append(game['game']['best_odds'])
        data_mean_median.append(str(game['game']['mean']) + "/" + str(game['game']['mean']))
        optimizer.load_game(game)
        data_ratio.append(round(100*optimizer.get_optimal_ratio(),1))

    data = dict(
        match = data_match,
        league = data_league,
        result_to_bet = data_result_to_bet,
        date = data_date,
        time_to_match = data_time_to_match,
        best_bookie = data_best_bookie,
        best_odds = data_best_odds,
        mean_median = data_mean_median,
        ratio = data_ratio,
    )

    source = ColumnDataSource(data)

    columns = [
        TableColumn(field="match", title="Mitch Title"),
        TableColumn(field="league", title="League"),
        TableColumn(field="result_to_bet", title="Result to Bet"),
        TableColumn(field="date", title="Date"),
        TableColumn(field="time_to_match", title="Time to Match"),
        TableColumn(field="best_bookie", title="Best Bookie"),
        TableColumn(field="best_odds", title="Best Odds"),
        TableColumn(field="mean_median", title="Mean/Median"),
        TableColumn(field="ratio", title="Ratio to Bet (%)"),
    ]

    data_table = DataTable(source=source, columns=columns, width=1400, height=1000, sizing_mode='stretch_both')
    return data_table

# create DataTable for arbitrage opportunity
def get_arbitrage_table(game):
    optimizer = ArbitrageOptimizer()
    optimizer.load_game(game)
    arbitrage_opportunity = optimizer.get_arbitrage_opportunity()

    if arbitrage_opportunity['arbitrage'] != 'yes':
        return None
    else:
        column_1 = [
            arbitrage_opportunity['bet']['1']['bookie'],
            arbitrage_opportunity['bet']['1']['odds'],
            str(round(arbitrage_opportunity['bet']['1']['bet_size'], 3)),
        ]
        column_X = [
            arbitrage_opportunity['bet']['X']['bookie'],
            arbitrage_opportunity['bet']['X']['odds'],
            str(round(arbitrage_opportunity['bet']['X']['bet_size'], 3)),
        ]
        column_2 = [
            arbitrage_opportunity['bet']['2']['bookie'],
            arbitrage_opportunity['bet']['2']['odds'],
            str(round(arbitrage_opportunity['bet']['2']['bet_size'], 3)),
        ]

        data = dict(column_1=column_1, column_X=column_X, column_2=column_2,)
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field="column_1", title="1"),
            TableColumn(field="column_X", title="X"),
            TableColumn(field="column_2", title="2"),
        ]

        data_table = DataTable(source=source, columns=columns, width=500, height=200)
        return data_table, arbitrage_opportunity['profit']

# create separate tabs for the arbitrage opportunities
arbitrage_tables = []
for game in games:
    output = get_arbitrage_table(game)
    if output is not None:
        arbitrage_tables.append(output)
# sort tables in descending order of the profit
arbitrage_tables.sort(key=lambda x: x[1], reverse=True)

# create a separate tab for each arbitrage table
tabs = []
for arbitrage_table in arbitrage_tables:
    profit = str(round(100*arbitrage_table[1],1))
    tabs.append(Panel(child=arbitrage_table[0], title="Profit : {}".format(profit)))

# create text inputs for calculating optimal bets
upper_bound_1 = TextInput(title="Upper bound 1", width=300)
upper_bound_X = TextInput(title="Upper bound X", width=300)
upper_bound_2 = TextInput(title="Upper bound 2", width=300)

ratio_1 = TextInput(title="Ratio 1", width=300)
ratio_X = TextInput(title="Ratio X", width=300)
ratio_2 = TextInput(title="Ratio 2", width=300)

lower_bound_1 = TextInput(title="Lower bound 1", width=300, value="1")
lower_bound_X = TextInput(title="Lower bound X", width=300, value="1")
lower_bound_2 = TextInput(title="Lower bound 2", width=300, value="1")

bet_1 = TextInput(title="Bet on 1", width=300)
bet_X = TextInput(title="Bet on X", width=300)
bet_2 = TextInput(title="Bet on 2", width=300)

calculate_button = Button(label="Calculate", width=900)

def calculate_bets():
    ratios = [float(ratio_1.value), float(ratio_X.value), float(ratio_2.value)]
    upper_bounds = [float(upper_bound_1.value), float(upper_bound_X.value), float(upper_bound_2.value)]
    lower_bounds = [float(lower_bound_1.value), float(lower_bound_X.value), float(lower_bound_2.value)]

    bets = ArbitrageOptimizer.get_optimal_bets(ratios, upper_bounds, lower_bounds)

    bet_1.value = str(round(bets[0], 0))
    bet_X.value = str(round(bets[1], 0))
    bet_2.value = str(round(bets[2], 0))

calculate_button.on_click(calculate_bets)

# create layout to be plotted
dataTable = get_data_table_from_games(games)
arbitrageTabs = Tabs(tabs=tabs, width=900)
calculator = column(
    row(upper_bound_1, upper_bound_X, upper_bound_2),
    row(ratio_1, ratio_X, ratio_2),
    row(lower_bound_1, lower_bound_X, lower_bound_2),
    row(calculate_button),
    row(bet_1, bet_X, bet_2)
)

mainTabs = [
    Panel(child=dataTable, title="Current profitable games"),
    Panel(child=column(arbitrageTabs, calculator), title="Current arbitrage opportunities")
]
layout = column(Tabs(tabs=mainTabs), sizing_mode='stretch_both')

# add layout to dashboard
curdoc().add_root(layout)
curdoc().title = "Current arbitrage opportunities"

