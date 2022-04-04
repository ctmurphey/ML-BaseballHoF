# Using Machine Learning to Predict Future Baseball Hall of Fame Inductees
The goal of this is to construct a model based of previous players, both in the hall of fame and not, in order to predict which current players are on track to be inducted into the Hall of Fame. Leveraging the abundance of stats logged and calculated and the importance it plays in estimating the quality of players, it theoretically should be possible to constuct a confident model for "Hall of Fame worthiness". This model can then be applied to current players or recently retired to see if they are already worthy of the Hall, current players to see if they're on track to be inducted, and even long-retired players to see if they statistically deserved their induction status.

This served as my final project for AMS 561 in the Spring 2022 semester at Stony Brook University.
## Libraries:
A list of all the necessary installs required to run this program. This assumes the user is running Python 3.8+ and has all of the core scientific packages (`numpy`, `scipy`, `matplotlib`, etc.) and is aware of their general purpose and use. 
### [List all non-standard libraries here, sklearn, tensorflow, etc.]
## Data:
The data comes from [Lahman's Baseball Database](https://www.seanlahman.com/baseball-archive/statistics/), specifically the .zip collection of csv files which can be directly downloaded [here](https://github.com/chadwickbureau/baseballdatabank/archive/refs/tags/v2022.2.zip). You'll need to download and unzip it into the same folder this code is in. It contains data collected all the way back to 1871 on players, teams, managers, etc.


## Files:
Going to separate the code into several files based on what the intended goal of the file is. My thinking is that this will reduce cluttering in the notebooks and allow for better visualization and clearer understanding of what the results are.
### `README`:
Provides documentation and links to all necessary downloads.

### `playwithdata.ipynb`:
First step of the code. Just loading it into a pandas dataframe and doing some basic data visualization with it. This acts as both a sanity check that the data loading works and practice for manipulating/sorting the data for the main files later on. No ML model will be trained here.