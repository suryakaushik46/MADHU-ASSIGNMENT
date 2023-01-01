import csv
import datetime
import math
import sim_parameters
import numpy as np
import pandas as pd
import helper
list_dict_of_samples_as_per_date=[]


#list to hold all data in csv
list_dictonary_of_countries=[]

list_test=[]
global_count=0
def next_covid_state(age_group,state):
    """_summary_

    Args:
        age_group (_type_): _description_
        state (_type_): _description_

    Returns:
        _type_: _description_
    """
    return np.random.choice(
                list(sim_parameters.TRASITION_PROBS[age_group][state].keys()),replace=True,
                 p = list(sim_parameters.TRASITION_PROBS[age_group][state].values()))
    




def run_days_for_sample(person_id,age_group_name,country,date_obj,days):
   """_summary_

    Args:
        person_id (_type_): _description_
        age_group_name (_type_): _description_
        country (_type_): _description_
        date_obj (_type_): _description_
        days (_type_): _description_
    """
   intitial_state='H'
   current_state='H'
   prev_state='H'
   #print("|||||||||||||||||||||||")
   #print(days)
   days_remain=sim_parameters.HOLDING_TIMES[age_group_name][current_state]
   if(days_remain!=0):
        days_remain-=1
   for i in range(days):
        if(days_remain==0):
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
                prev_state=current_state
                current_state=next_covid_state(age_group_name,current_state)
                date_obj=date_obj+datetime.timedelta(days = 1)
                days_remain=sim_parameters.HOLDING_TIMES[age_group_name][current_state]
                if(days_remain!=0):
                    days_remain-=1
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
            prev_state=current_state
            date_obj=date_obj+datetime.timedelta(days = 1)
            days_remain-=1
            pass
   df=pd.DataFrame(list_dict_of_samples_as_per_date)
   df.to_csv('file1.csv',index=False)
   
   return

def get_summrized_data(country,date_obj,days):
    """_summary_

    Args:
        country (_type_): _description_
        date_obj (_type_): _description_
        days (_type_): _description_
    """
    for i in range(days):
        dict_per={
        'H':0, 'I':0, 'S':0, 'D':0, 'M':0
        }
        #print(i)
        for j in range(i,len(list_dict_of_samples_as_per_date),395):
            for k in list_dict_of_samples_as_per_date[j]:
                if(k=='state'):
                    dict_per[list_dict_of_samples_as_per_date[j][k]]+=1
        
        list_test.append({
            "date":date_obj,
            "country":country,
            "D":dict_per['D'],
            "H":dict_per['H'],
            "I":dict_per['I'],
            "M":dict_per['M'],
            "S":dict_per['S']
        }); 
        date_obj=date_obj+datetime.timedelta(days = 1)           

            
        
        
    df=pd.DataFrame(list_test)
    df.to_csv('file2.csv',index=False)
    
        
    
        
    return 






def run_for_less_5(samples,day_diffs,start_date_object,country):
    """_summary_

    Args:
        samples (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    global_count=0
    for i in range(samples):
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
    for i in range(samples):
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
    for i in range(samples):
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
    for i in range(samples):
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
    for i in range(samples):
        run_days_for_sample(i,"over_65",country,start_date_object,day_diffs)
    return



def run_days(list_smaple,day_diffs,start_date_object,country):
    """_summary_

    Args:
        list_smaple (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
        country (_type_): _description_
    """
    run_for_less_5(list_smaple[0],day_diffs,start_date_object,country)
    run_for_5_to_14(list_smaple[1],day_diffs,start_date_object,country)
    run_for_15_to_24(list_smaple[2],day_diffs,start_date_object,country)
    run_for_25_to_64(list_smaple[3],day_diffs,start_date_object,country)
    run_for_over_65(list_smaple[4],day_diffs,start_date_object,country)
    get_summrized_data(country,start_date_object,day_diffs)

    return 

def get_data_samples(country,sample_ratio,day_diffs,start_date_object):
    """_summary_

    Args:
        country (_type_): _description_
        sample_ratio (_type_): _description_
        day_diffs (_type_): _description_
        start_date_object (_type_): _description_
    """
    list_smaple=[];
    print(country)
    for c in list_dictonary_of_countries:
        smaples=0
        if(country==c['country']):
            for s in c:
                if s!='country' and s!='population' and s!='median_age':
                    x=float(c[s])

                    #print(x,smaples,(x*smaples)/100)
                    list_smaple.append(math.floor((x*smaples)/100))
                elif s=='population':
                    print(c[s])
                    x=float(c[s])
                    smaples=math.floor(x)//sample_ratio


    print(list_smaple)
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

    with open(csv_filename) as f:
        reader= csv.DictReader(f)
        for row in reader:
            list_dictonary_of_countries.append(row)
        print(f'length of dict {len(list_dictonary_of_countries)}')

    start_date_object = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_object = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    day_diff_obj=end_date_object-start_date_object
    day_diff=day_diff_obj.days+1
    SAMPLE_RATIO=sample_ratio
    
    for c in countries:
        get_data_samples(c,sample_ratio,day_diff,start_date_object)

    helper.create_plot('file2.csv',countries)
    return 