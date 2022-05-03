# Using Machine Learning to Predict Future Baseball Hall of Fame Inductees
The goal of this is to construct a model based of previous players, both in the hall of fame and not, in order to predict which current players are on track to be inducted into the Hall of Fame. Leveraging the abundance of stats logged and calculated and the importance it plays in estimating the quality of players, it theoretically should be possible to constuct a confident model for "Hall of Fame worthiness". This model can then be applied to current players or recently retired to see if they are already worthy of the Hall, current players to see if they're on track to be inducted, and even long-retired players to see if they statistically deserved their induction status.

This served as my final project for AMS 561 in the Spring 2022 semester at Stony Brook University.
## Libraries:
Requires Python 3.8+ and the following libraries: `numpy`, `pandas`, `matplotlib` and `scikit-learn`. In the future it may require `tensorflow`
## Data:
The data comes from [Lahman's Baseball Database](https://www.seanlahman.com/baseball-archive/statistics/), specifically the .zip collection of csv files which can be directly downloaded [here](https://github.com/chadwickbureau/baseballdatabank/archive/refs/tags/v2022.2.zip). It contains player-season level data dating back all the way to 1871. Running the model training in `predictive-models.py` doesn't require the data be downloaded, as the files `pitchingdata.csv` and `battingdata.csv` already contain the processed data. However, in order to run the rest of the code (`playwithdata.ipynb`, `makedata.py`, `baseballstats.py`), the files need to be downloaded from the like above and placed in the same directory.


## Files:
Going to separate the code into several files based on what the intended goal of the file is. My thinking is that this will reduce cluttering in the notebooks and allow for better visualization and clearer understanding of what the results are.
### `README`:
Provides documentation and links to all necessary downloads.

### `baseballstats.py`:
A collection of different functions for generating different stats based off the database. Most functions will just take the playerID and output a float (or int). Makes the notebook files much cleaner by allowing many of the functions, especially the ones that will likely be called across different notebooks, collected all in one place. It also serves as the main interface between the rest of the code and the baseball database

### `make-data.py`:
Takes the functions in `baseballstats` and builds the two dataframes (pitchers and hitters) that will be used in model training. This will save a lot of runtime later and memory since we won't be building the dataframes from scratch every time. If the csv files need to be updated (like in future years when more data is available), then the code will need to be tweaked and rerun. 

### `playwithdata.ipynb`:
Tests all of the functions in `baseballstats` and ensures that the code is working properly. Additionally, some visualization of the processed data is included here prior to the ML model training.

### `predictive-models.ipynb`:
Constructs multiple different machine learning models with different mixes of stats from `baseballstats.py`. While it would be simpler to just make one that incorporates everything and perform LASSO regression to eliminate the irrelevant ones, the goal is instead to assess how well some of these stats change how well the model classifies.

### `Fangraphs-Leaderboard.csv`:
Baseball statistics site [Fangraphs](https://www.fangraphs.com/) has a few of their own weighted stats, like Fielding-Independent Pitching (FIP) and weighted On-Base Average (wOBA). This file is a table of the weights they use to calculate these stats by year, as these values are adjusted every year and must be accounted for.

### `pitchingdata.csv` and `battingdata.csv`:
Contains all data after preprocessing. Only players who were eligible for the Hall and have since past their eligibility period are included in these files. Created with `make-data.py`, some visualizations of the data in these files can be seen in `playwithdata.ipynb`.