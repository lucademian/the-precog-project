import pandas as pd

HOMICIDE_DATA = './Data/homicide-data.csv'
DEMOGRAPHIC_DATA = './Data/acs2015_census_tract_data.csv'
SHOOTING_DATA = './Data/fatal-police-shootings-data.csv'
AGE_DISTRIBUTION = './Data/age_distribution.csv'
state_abbrev_df = pd.read_csv('./Data/state_abbrev.csv')

def read_age_dist(filename):
    '''To read the age population distribution file'''
    df = pd.read_csv(filename)
    # Change state names to abbreviations
    df['State'] = df['State'].apply(find_abbreviation)
    # Drop irrelevant columns
    df = df.drop(['Footnotes', 'Total'], axis=1)
    return df


def read_demographic_data(filename, age_df):
    '''To read and clean the demographic data'''
    df = pd.read_csv(filename)

    # For each row, convert percentages to total values in the city using the total population
    df['Hispanic'] = (df['Hispanic'] / 100) * df['TotalPop']
    df['White'] = (df['White'] / 100) * df['TotalPop']
    df['Black'] = (df['Black'] / 100) * df['TotalPop']
    df['Native'] = (df['Native'] / 100) * df['TotalPop']
    df['Asian'] = (df['Asian'] / 100) * df['TotalPop']

    # Group the data by state and use the sum
    df = df.groupby(['State']).sum().reset_index()
    # select relevant columns
    df = df[['State', 'TotalPop', 'Men', 'Women', 'Hispanic', 'White', 'Black', 'Native', 'Asian']]
    # Drop Puerto Rico
    df = df[df['State'] != 'Puerto Rico']
    # Change state names to abbreviations
    df['State'] = df['State'].apply(find_abbreviation)

    # Merge the age population distribution dataset to the other demographic data
    df = pd.merge(df, age_df, on='State', how='inner')

    # Rename the columns
    df.columns = ['State', 'TotalPop', 'Male', 'Female', 'Hispanic', 'White', 'Black', 'Native', 'Asian', '0-18',
                  '19-25', '26-34', '35-54', '55-64', '65+']

    return df


def date_to_year(val):
    '''To convert a date to year'''
    val = str(val)
    # select the year as a 4 digit number
    year = val[:4]

    return int(year)


def read_homicide_data(filename):
    '''To read and clean the homicide data'''
    df = pd.read_csv(filename)
    # Drop irrelevant columns
    df = df.drop(['uid', 'victim_last', 'victim_first', 'disposition', 'city'], axis=1)
    # Drop rows containing unknown age
    df = df[~df['victim_age'].str.contains('Unknown')]
    # convert dates to year
    df['reported_date'] = df['reported_date'].apply(date_to_year)
    # convert state abbreviations to upper case
    df['state'] = df['state'].str.upper()

    return df


def read_police_shootings(filename):
    '''To read and clean the police shooting data'''
    df = pd.read_csv(filename)
    # Select relevant columns
    df = df[['age', 'date', 'gender', 'race', 'state', 'longitude', 'latitude']]
    # race abbreviations to complete names
    race_dct = {'A': 'Asian', 'B': 'Black', 'W': 'White', 'H': 'Hispanic', 'N': 'Native'}
    # gender abbreviations to complete names
    gender_dct = {'M': 'Male', 'F': 'Female'}
    # Rename gender and race values
    df = df.replace({'race': race_dct})
    df = df.replace({'gender': gender_dct})
    df = df.dropna()
    # Rename columns
    df.rename(columns={'date': 'reported_date', 'race': 'victim_race', 'age': 'victim_age',
                       'gender': 'victim_sex'}, inplace=True)
    # convert date to year
    df['reported_date'] = df['reported_date'].apply(date_to_year)
    # remove rows with race values being zero
    df = df[df['victim_race'] != 0]
    # remove rows containing 'O' as values
    mask = (df == 'O').any(axis=1)
    df = df.drop(index=df[mask].index)

    return df


def find_abbreviation(string):
    '''Find the state abbreviation from complete name'''
    abbrev = state_abbrev_df.loc[state_abbrev_df['State'] == string, 'Abbreviation'].iloc[0]
    return abbrev


def state_data(df):
    '''Convert incident data to state specific data'''
    states_lst = []
    # iterate over years
    for year in df['reported_date'].unique():
        # filter df by selected year
        year_df = df[df['reported_date'] == year]
        # iterate over states
        for state in year_df['state'].unique():
            # create dict to count vals and convert to df
            state_dict = {'State': state, 'Year': None, 'Hispanic': 0, 'White': 0, 'Other': 0, 'Black': 0, 'Asian': 0,
                          'Native': 0, 'Unknown': 0, '0-18': 0, '19-25': 0, '26-34': 0, '35-54': 0, '55-64': 0,
                          '65+': 0, 'Male': 0, 'Female': 0, 'Total': 0}
            # iterate over state-specific df to count occurances
            for i, row in year_df[year_df['state'] == state].iterrows():
                # count occurences of each variable in incident df
                race = row['victim_race']
                age = int(row['victim_age'])
                sex = row['victim_sex']
                state_dict['Year'] = year
                state_dict['Total'] += 1
                state_dict[sex] += 1
                state_dict[race] += 1
                # count occurences by age buckets
                if age >= 0 and age < 19:
                    state_dict['0-18'] += 1
                elif age >= 19 and age < 26:
                    state_dict['19-25'] += 1
                elif age >= 26 and age < 35:
                    state_dict['26-34'] += 1
                elif age >= 35 and age < 55:
                    state_dict['35-54'] += 1
                elif age >= 55 and age < 65:
                    state_dict['55-64'] += 1
                elif age >= 65:
                    state_dict['65+'] += 1
            states_lst.append(state_dict)

    state_df = pd.DataFrame(states_lst)

    return state_df


def state_incident_rate(demographic_df, incident_df, col_name):
    '''To find the state-specific incident rate by state population'''
    rate_lst = []
    # iterate over incident df
    for i, row in incident_df.iterrows():
        state = row['State']
        total_incidents = row['Total']
        total_pop = demographic_df[demographic_df['State'] == state]['TotalPop']
        # find the incident rate
        incident_rate = float(total_incidents / total_pop)
        rate_lst.append(incident_rate)
    incident_df[col_name] = rate_lst

    return incident_df


def incident_probability_given_attributes(incident_data, census_data, attributes, state, rate_col):
    """
    This function finds the conditional probability of an incident given a set of attributes for a given state and
    year. It takes advantage of Bayes' theorem to calculate P(I|x,y,z...) as we are able to calculate
    P(I|x), P(I|y), p(I|z), ... independently and we assume conditional independence between variables x, y, z, ...
    in the population data.

    P(I|x,y,z,...) = (P(I|x) * P(I|y) * P(I|z) * ...) / P(H)
    """
    # Find the mean values across all years by state
    incident_data_row = incident_data.groupby(['State']).mean().reset_index()
    # filter census data by state
    census_data_row = census_data[census_data["State"] == state]
    # find the incident probability in state
    p_incident = incident_data_row.iloc[0][rate_col]
    # find the total population and total incidents
    total_pop = census_data_row.iloc[0]["TotalPop"]
    total_incidents = incident_data_row.iloc[0]["Total"]
    prod = 1
    # iterate over list of given attributes
    for attribute in attributes:
        # find the attribute population in census data
        total_attribute_pop = census_data_row.iloc[0][attribute]
        # find the number of incidents with individuals of given attributes
        incidents_for_attribute = incident_data_row.iloc[0][attribute]
        # calculate the probability of the attribute
        p_attribute = total_attribute_pop / total_pop
        # calculate the probability of the attribute given total incidents
        p_attribute_given_incident_rate = incidents_for_attribute / total_incidents
        # find the product of the attribute probabilities given incidents
        prod = prod * a_given_b(p_attribute_given_incident_rate, p_incident, p_attribute)
    return prod / p_incident


def a_given_b(b_given_a, a, b):
    '''Bayes Theorem'''
    return (b_given_a * a) / b


if __name__ == "__main__":
    # Read in data files
    homicide_df = read_homicide_data(HOMICIDE_DATA)
    shooting_df = read_police_shootings(SHOOTING_DATA)
    age_dist_df = read_age_dist(AGE_DISTRIBUTION)
    demographic_df = read_demographic_data(DEMOGRAPHIC_DATA, age_dist_df)

    # create state-specific dataframes
    state_homicide_df = state_data(homicide_df)
    state_shooting_df = state_data(shooting_df)
    state_homicide_df = state_incident_rate(demographic_df, state_homicide_df, 'Homicide_Rate')
    state_shooting_df = state_incident_rate(demographic_df, state_shooting_df, 'Police_Shooting_Rate')