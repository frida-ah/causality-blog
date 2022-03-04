# Causal discovery blog
This code was created for the Medium blog "Discover confounders in a Directed Acyclic Graph".

### How to run code locally
In the Terminal:
- Make sure Miniconda (or Anaconda) is installed. If you prefer another option, you will not need to follow the following steps.
- Clone GitHub code
``` git clone git@github.com:frida-ah/causality-blog.git```
- Create a conda environment  
``` conda create -n causality-blog python=3.9  ```
- Activate the new conda environment
``` conda activate causality-blog ```
- Install the required python packages
``` pip install -r requirements.txt ```

### Data sources
#### Keyword searches
The timeseries within Google Trends search data mimics the real sales of a product. https://trends.google.com/trends/explore?cat=71&date=today%205-y&geo=NL&q=softijs 

#### Weather in the Netherlands
In order to run the code, you will first need to donwload the weather data for "De Bilt" as proxy for the Netherlands https://www.knmi.nl/nederland-nu/klimatologie/daggegevens. Temperature is measured in the tenth of degrees Celsius in the dataset. So, it needs to be converted to Celsius degrees by dividing with 10. (see data/weather_data.csv)