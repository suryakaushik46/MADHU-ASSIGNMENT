import csv
import datetime
import math
import sim_parameters
import numpy as np
import pandas as pd
import helper
# list to hold the simulated data 
list_dict_of_samples_as_per_date=[]


#list to hold all data in csv
list_dictonary_of_countries=[]

# list to hold the summary data
list_test=[]
global_count=0

def next_covid_state(age_group,state):
    """_summary_
    This function is used to give the next state according to the age_group and the present state

    Args:
        age_group (_type_): _description_
        state (_type_): _description_

    Returns:
        _type_: _description_
    """
    # This function will return a record with the values of a random samples taken according to the age group and the state
    return np.random.choice(
                list(sim_parameters.TRASITION_PROBS[age_group][state].keys()),replace=True,
                 p = list(sim_parameters.TRASITION_PROBS[age_group][state].values()))
    




def run_days_for_sample(person_id,age_group_name,country,date_obj,days):
   """_summary_
    This is function which is responsible for the simulating through the given sample and agegroup 
    Args:
        person_id (_type_): _description_
        age_group_name (_type_): _description_
        country (_type_): _description_
        date_obj (_type_): _description_
        days (_type_): _description_
    """
    # ASSIGNING the initial state of the simulation as 'H'
   intitial_state='H'
   # ASSIGNING the current state of the simulation as 'H'
   current_state='H'
   # ASSIGNING the previous state of the simulation as 'H'
   prev_state='H'
   #print("|||||||||||||||||||||||")
   #print(days)
   # Assigning the days remain for the particular age group of particular state 
   days_remain=sim_parameters.HOLDING_TIMES[age_group_name][current_state]
   # checking the condition is that particular age group and the curent state has days remain or not?
   if(days_remain!=0):
        # IF the days are remain then the days_remain will be decremented by 1
        days_remain-=1
    # iterating through the remain number of days
   for i in range(days):
        # checking the days_remain are equals to 0 or not ?
        if(days_remain==0):
                # if days_remain are equal to 0 then the details about the particular sample will be appended to the list
                list_dict_of_samples_as_per_date.append(
                    {
                        "person_id":person_id,
                        "age_group_name":age_group_name,
                        "country":country,
                        "date":date_obj,
                        "state":current_state,
                        "staying":days_remain,
                        "prev_state":prev_state
                    }

                );
                # assigning the prev state with the current state
                prev_state=current_state
                # calling the next_covid_state function which is used to get the next following the state in the simulation
                current_state=next_covid_state(age_group_name,current_state)
                # Incrementing the date for doing the simulation of next day
                date_obj=date_obj+datetime.timedelta(days = 1)
                # assigning the number of days remain in the current state
                days_remain=sim_parameters.HOLDING_TIMES[age_group_name][current_state]
                # checking the condition whether days_remain or not
                if(days_remain!=0):
                    # if days remain then decrement by 1
                    days_remain-=1

        # if days_remain equal to 0 at the beginning the current data will be appended to the list of dict 
        else :
            list_dict_of_samples_as_per_date.append(
                    {
                        "person_id":person_id,
                        "age_group_name":age_group_name,
                        "country":country,
                        "date":date_obj,
                        "state":current_state,
                        "staying":days_remain,
                        "prev_state":prev_state
                    }

                );
            # assigning the prev state with the current state
            prev_state=current_state
            # Incrementing the date for doing the simulation of next day
            date_obj=date_obj+datetime.timedelta(days = 1)
            # decrementing the days_remain by 1
            days_remain-=1
            pass
    # storing the list in which the simulated results according to the age group are stored by convertig them into a dataframe
   df=pd.DataFrame(list_dict_of_samples_as_per_date)
   # converting the dataframe into .csv file
   df.to_csv('file1.csv',index=False)
   return

def get_summrized_data(country,date_obj,days):
    """_summary_
    This is the function which is used to create the a3_covid_simulated_summary file 


    Args:
        country (_type_): _description_
        date_obj (_type_): _description_
        days (_type_): _description_
    """
    # iterating through the range of days which is differnece betweeen the start date and the end date
    for i in range(days):
        # a dictionary which has the classification of number of samples belongs to whch state 
        dict_per={
        'H':0, 'I':0, 'S':0, 'D':0, 'M':0
        }
        #print(i)
        # iterating through all the available records in the final result dictionary which has the simulated results
        for j in range(i,len(list_dict_of_samples_as_per_date),days):
            # iterating through record in the final dictionary
            for k in list_dict_of_samples_as_per_date[j]:
                # checking if the current iteration record with the state in the dictionary 
                if(k=='state'):
                    # incrementing the count of state according to the final dict file
                    dict_per[list_dict_of_samples_as_per_date[j][k]]+=1
        # appending the final results for the a3_summary file with the following data which is used for plotting final graph
        list_test.append({
            "date":date_obj,
            "country":country,
            "D":dict_per['D'],
            "H":dict_per['H'],
            "I":dict_per['I'],
            "M":dict_per['M'],
            "S":dict_per['S']
        }); 
        # inrementing the date by 1
        date_obj=date_obj+datetime.timedelta(days = 1)           

            
    # converting the final summary file into data frame type
    df=pd.DataFrame(list_test)
    # converting the data frame into the .csv file
    df.to_csv('file2.csv',index=False)
    return 


def run_for_less_5(samples,day_diffs,start_date_object,country):
    """_summary_
    This function is used to call the main simulation function for the age group of < 5
    Args:
        samples (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    global_count=0
    # iteating through every sample 
    for i in range(samples):
        # callin the simulatiom function 
        run_days_for_sample(i,"less_5",country,start_date_object,day_diffs)
    return
def run_for_5_to_14(samples,day_diffs,start_date_object,country):
    """_summary_

    Args:
        samples (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    # iteating through every sample
    for i in range(samples):
        # callin the simulatiom function
        run_days_for_sample(i,"5_to_14",country,start_date_object,day_diffs)
    return
def run_for_15_to_24(samples,day_diffs,start_date_object,country):
    """_summary_

    Args:
        samples (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    # iteating through every sample
    for i in range(samples):
        # callin the simulatiom function
        run_days_for_sample(i,"15_to_24",country,start_date_object,day_diffs)
    return
def run_for_25_to_64(samples,day_diffs,start_date_object,country):
    """_summary_

    Args:
        samples (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    # iteating through every sample
    for i in range(samples):
        # callin the simulatiom function
        run_days_for_sample(i,"25_to_64",country,start_date_object,day_diffs)
    return
def run_for_over_65(samples,day_diffs,start_date_object,country):
    """_summary_

    Args:
        samples (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    # iteating through every sample
    for i in range(samples):
        # callin the simulatiom function
        run_days_for_sample(i,"over_65",country,start_date_object,day_diffs)
    return



def run_days(list_smaple,day_diffs,start_date_object,country):
    """_summary_
    This function is used to call functions which are used for the simulation according to the age group

    Args:
        list_smaple (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    # callig the run function for age group of 0_5  
    run_for_less_5(list_smaple[0],day_diffs,start_date_object,country)
    # callig the run function for age group of 5_14  
    run_for_5_to_14(list_smaple[1],day_diffs,start_date_object,country)
    # callig the run function for age group of 15_24 
    run_for_15_to_24(list_smaple[2],day_diffs,start_date_object,country)
    # callig the run function for age group of 25_64  
    run_for_25_to_64(list_smaple[3],day_diffs,start_date_object,country)
    # callig the run function for age group of >65  
    run_for_over_65(list_smaple[4],day_diffs,start_date_object,country)
    # calling the summarised data function
    get_summrized_data(country,start_date_object,day_diffs)

    return 

def get_data_samples(country,sample_ratio,day_diffs,start_date_object):
    """_summary_
    To get the ratios for the given population of the country and distribute the samples
    how many a age group can afford
    Args:
        country (_type_): _description_
        sample_ratio (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
    """
    # creating a empty list which is used store the number of samples according to the age group
    list_smaple=[];
    print(country)
    # iterating throgh each record in the given list_dictionary_of_countires alias a3 countries.csv 
    for c in list_dictonary_of_countries:
        smaples=0
        # checking the condition that wheather the given input country is in the record or not
        if(country==c['country']):
            # iterating through the internal record of each and every record
            for s in c:
                # checking the condition to only let us take the sample percentage of the each each group 
                if s!='country' and s!='population' and s!='median_age':
                    # Assigning the given percentage value into float type
                    x=float(c[s])

                    #print(x,smaples,(x*smaples)/100)
                    # Appending the number of samples according to the age group 
                    list_smaple.append(math.floor((x*smaples)/100))
                # this is the condition which used to store the population of the country accrding to the p[resent instance
                elif s=='population':
                    print(c[s])
                    # assigning ad storing the population into x by converting into float type
                    x=float(c[s])
                    # Assigning total number of samples possibe for each country 
                    smaples=math.floor(x)//sample_ratio


    print(list_smaple)
    # calling the run_days function which is used for dividing the samples according to the age group 
    run_days(list_smaple,day_diffs,start_date_object,country)
    return



#default function run
def run(countries_csv_name:str,countries:list,sample_ratio,start_date,end_date):
    """_summary_
    Args:
        countries_csv_name (str): _description_
        countries (list): _description_
        sample_ratio (_type_): _description_
        start_date (_type_): _description_
        end_date (_type_): _description_
    """

    csv_filename = countries_csv_name
    #reading the input from the countries.csv file to a dictionary 
    with open(csv_filename) as f:
        reader= csv.DictReader(f)
        for row in reader:
            list_dictonary_of_countries.append(row)
        print(f'length of dict {len(list_dictonary_of_countries)}')

    # converting the given start date from string data type to a data time object
    start_date_object = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    # converting the given end date from string data type to a data time object
    end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    # Finding the diffenence between the start date and the end date in number of days 
    day_diff_obj=end_date_object-start_date_object
    # Incrementing the difference by 1 for getting the accurate calculation
    day_diff=day_diff_obj.days+1
    # Assigning sample ratio to global sample ratio
    SAMPLE_RATIO=sample_ratio
    # Iterating through the input given countries 
    for c in countries:
        get_data_samples(c,sample_ratio,day_diff,start_date_object)
    # calling the helper function which is used for plotting the final output graph
    helper.create_plot('file2.csv',countries)
    return 