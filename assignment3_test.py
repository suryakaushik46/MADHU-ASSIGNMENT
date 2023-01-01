from inspect import stack
from turtle import st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sim_parameters import TRASITION_PROBS, HOLDING_TIMES
from helper import create_plot

def run(countries_csv_name, countries, sample_ratio, start_date, end_date):

    #get given country data
    countries_csv  = pd.read_csv(countries_csv_name)

    #create empty new dataframe for selected countries
    countries_data = pd.DataFrame(columns=countries_csv.columns)

    #assign data of selected countries from original country dataframe to countries_data
    for country in countries:
        countries_data = pd.concat([countries_data,countries_csv.loc[countries_csv['country'] == country]])

    #delete median_age as it is not required for the simulation
    del countries_data['median_age']
    
    #divide population by sample_ratio and round to floor
    countries_data['population'] = countries_data['population'].div(sample_ratio).astype(int)
    
    #use percentage to get the population of a country based on its sample population
    for index in range(len(countries_data)):
        countries_data.iloc[index, 2:] = countries_data.iloc[index, 2:].astype(float).mul(countries_data.iloc[index,1]).floordiv(100)

    #create empty final dataframes
    simulated = pd.DataFrame(columns=['person_id','age_group_name','country','date','state','staying_days','prev_state'])
    summary = pd.DataFrame(columns=['date','country','D','H','I','M','S'])

    #date calculation
    date_start = datetime.strptime(start_date, '%Y-%m-%d')
    date_end = datetime.strptime(end_date, '%Y-%m-%d')
    days = (date_end - date_start).days

    #iterate through each country
    for country in countries_data.iterrows():

        #create new dataframe representing a countries population-individual state on a specific day
        country_state = pd.DataFrame(columns=['age_group','prev_state','for_days','state','days_left'])

        #starting default data (healthy)
        for age_group, count in country[1].iloc[2:].to_dict().items():
            for person in range(int(count)):
                country_state.loc[len(country_state)] = [age_group, 'H', 1, 'H', 0]

        #day-0 summary [all healthy]
        count = list(country_state['state'].values)
        count_fin = []
        for state in 'DHIMS':
            count_fin.append(count.count(state))
        summary.loc[len(summary)] = [datetime.strftime(date_start, '%Y-%m-%d'), country[1].iloc[0]] + count_fin

        #iterate through number of days to run simulation for
        for day_count in range(days):
            #print(day_count)
            #iterate through every individual in a country for the fiven date
            for p_id, person_data in country_state.iterrows():

                #add the following data to a3-covid-simulated-timeseries.csv dataframe
                simulated.loc[len(simulated)] = [p_id, person_data['age_group'], country[1].iloc[0], datetime.strftime(date_start + timedelta(days=day_count), '%Y-%m-%d'),person_data['state'],person_data['for_days'] - person_data['days_left'], person_data['prev_state']]
                
                #get previous state
                prev_state = country_state.loc[p_id, 'state']

                #predict the next state based on transition state probabilities
                if(person_data['state'] == 'H'):
                    trans = TRASITION_PROBS[person_data['age_group']]['H']
                    next_state = np.random.choice(list(trans.keys()), p = list(trans.values()))

                    country_state.loc[p_id, ['state', 'prev_state', 'days_left', 'for_days']] = [next_state, 'H', HOLDING_TIMES[person_data['age_group']][next_state]+ 1, HOLDING_TIMES[person_data['age_group']][next_state]]

                elif(person_data['state'] == 'D'):
                    country_state.loc[p_id, ['state', 'prev_state', 'days_left']] = ['D', 'D', 0]
                    simulated.loc[len(simulated)-1] = [p_id, person_data['age_group'], country[1].iloc[0], datetime.strftime(date_start + timedelta(days=day_count), '%Y-%m-%d'),person_data['state'],0, person_data['prev_state']]

                else:
                    #skip the current individual for a day as fas as the individual is supposed to remain in a state for >1 days
                    if(person_data['days_left']==1):
                        country_state.loc[p_id, 'prev_state'] = person_data['state']
                        trans = TRASITION_PROBS[person_data['age_group']][person_data['state']]
                        next_state = np.random.choice(list(trans.keys()), p = list(trans.values()))

                        #if state was changed, add a row with updated previous state
                        if(prev_state!=next_state):
                            country_state.loc[p_id, ['state', 'prev_state', 'for_days', 'days_left']] = [next_state, prev_state, HOLDING_TIMES[person_data['age_group']][next_state] + 1, HOLDING_TIMES[person_data['age_group']][next_state] + 1]
                        else:
                            country_state.loc[p_id, ['state', 'prev_state', 'for_days', 'days_left']] = [next_state, person_data['prev_state'], HOLDING_TIMES[person_data['age_group']][next_state] + 1, HOLDING_TIMES[person_data['age_group']][next_state] + 1]
                
                #subtract one day from every individual's 'days_left'
                country_state.iloc[p_id, 4] = country_state.iloc[p_id, 4] - 1

            #get the amount of people(frequency) in each type of state for every day and add it to a3-covid-summary-timeseries dataframe
            count = list(country_state['state'].values)
            count_fin = []
            for state in 'DHIMS':
                count_fin.append(count.count(state))
            summary.loc[len(summary)] = [datetime.strftime(date_start + timedelta(days=day_count), '%Y-%m-%d'), country[1].iloc[0]] + count_fin

           # print(day_count)

    #save dataframes
    simulated = simulated.sort_values(['country','person_id'])
    simulated.to_csv('a3-covid-simulated-timeseries.csv', index=False)
    summary.to_csv('a3-covid-summary-timeseries.csv', index=False)
    create_plot('a3-covid-summary-timeseries.csv', countries)
