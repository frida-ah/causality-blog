# Interaction effects in linear regression
This code was created for the Medium blog "".


### How to run code locally
In the Terminal:
- Make sure Miniconda (or Anaconda) is installed. If you prefer another option, you will not need to follow the following steps.
- Clone GitHub code
``` git clone git@github.com:frida-ah/interactions_medium_blog.git```
- Create a conda environment  
``` conda create -n interactions-blog python=3.9  ```
- Activate the new conda environment
``` conda activate interactions-blog ```
- Install the required python packages
``` pip install -r requirements.txt ```



### Data sources
#### Keyword searches
The timeseries within Google Trends search data mimics the real sales of a product. https://trends.google.com/trends/explore?cat=71&date=today%205-y&geo=NL&q=ijs 

#### Weather in the Netherlands
In order to run the code, you will first need to donwload the weather data from https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/. The observation type TAVG which represents the average temperature of a timestamp, is measured in the tenth of degrees Celsius in the dataset. So, it needs to be converted to Celsius degrees by dividing with 10.