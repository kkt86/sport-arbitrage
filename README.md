# sport-arbitrage

Sporting arbitrage strategies. The idea is to investigate betting opportunities by either exploiting convenient odds, 
or exploiting inneficiencies among the bookies websites.

## Backend overview

The backend should consist in three components: `dashboardScraper`, `arbitrageFinder` and `arbitrageOptimizer`

##### dashboardScraper

The `dashboardScraper` is intended to extract information from current available games and parse it in standard format. 
Currently, I am using `namedtuple` with the following fields:

    * `timestamp`   : query time
    * `date`        : date of the match
    * `game`        : mathc to be played
    * `league`      : league in which the match is played
    * `odd_matrix`  : `pandas.DataFrame` object, having as rows the possible outcomes of the game (`1`, `X` and `2`),
                      and as columns, the odds offered by the different bookies.
                      
##### arbitrageFinder

This class is intended to find arbitrage opportunities within the odd matrices of the different games

##### arbitrageOptimizer

This class is intended to optimize the betting, once an arbitrage opportunity is found, based on 
bookie constraints, capital constraints ecc.
