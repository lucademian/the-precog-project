# The Precog Project ReadMe
By: Nicolai Jacobsen, Jake Friedman, Luca Demian, and Andre Kirby

## Overview
We first did exploratory data analysis on the datasets gathered, those being from Washington Post and US Census datasets. This allowed us to clean the data, and we could then calculate the probabilities of homicide based on gender, age, race, and location, as well as the likelihood of someone being affected by a police shooting (based on the same factors). This was done by creating a probability function that found the conditional probability of an incident given a set of attributes all of this aformentioned data science work was done in Python. This logic was then ported over to a JavaScript/svelte front-end that represents all this data and allows the users of the website to find out where they fall under according to their demographics and our calculated probabilities. 

### Datasets Used: 
The Washington Post Police Shooting [Dataset](https://github.com/washingtonpost/data-police-shootings): The Washington Post Police shooting dataset contains records of all persons shot by an on-duty police officer from 2015 to 2023, in the United States, as well as the agencies involved in each event. It is updated regularly as fatal shootings are reported and as facts emerge about individual cases.

The Washington Post Homicide [Dataset](https://github.com/washingtonpost/data-homicides): The Washington Post collected data on more than 52,000 criminal homicides over the past 10 years in 50 of the largest American cities. The data included the location of the homicide, whether an arrest occurred and, demographic information about the victim. 

2020 US Census [Dataset](https://www.kaggle.com/datasets/zusmani/us-census-2020) (from Kaggle): This dataset is from the US Census website and was cleaned for Kaggle to increase accessibility. There are no personal identifiable information in this dataset.

US 2021 Age Distribution [Dataset](https://www.kff.org/other/state-indicator/distribution-by-age/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D): Population and demographic data in this dataset is based on analysis of the Census Bureau’s American Community Survey (ACS) and thus it may differ from other population estimates by the Census Bureau. The US and state population data displayed on this site are only for civilians. Population numbers are rounded to the nearest 100. 

### EDA and Probability Algorithms in Python
We used Pandas for the Exploratory Data Analysis to clean and adjust the datasets we had as needed. 

We found the conditional probability of a certain incident occuring (ie. homicide or police shooting) with the function `incident_probability_given_attributes`. This function finds the conditional probability of an incident given a set of attributes for a given state and year. It uses Bayes' theorem to calculate P(I|x,y,z...) as we are able to calculate P(I|x), P(I|y), p(I|z), ... independently and we assume conditional independence between variables x, y, z, ... in the population data. Therefore, we know that: P(I|x,y,z,...) = (P(I|x) * P(I|y) * P(I|z) * ...) / P(H)

### The Precog Project Front-End (Interactive Website)


