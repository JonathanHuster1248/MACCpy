# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 22:35:48 2022

@author: jonat
"""

def read_data(DIR):
    """
    

    Parameters
    ----------
    DIR : String
         The location (directory) of the "home" location. Within the folder should
         be data/[file].csv.

    Returns
    -------
    plant_data : pandas DF
        Data about plant behavior including name, generation, emissions, etc.
    cost_data : pandas DF
        Data about the capital, fuel, and OM costs associated with plants by fuel type.
    cf_data : pandas DF
        Data about capactiy factors for technologies.
    age_data : pandas DF
        Data about the payoff lifetimes (and shutdown lifetimes) of existing plants

    """
    
    
    import os 
    import pandas
    
    plant_data_path = os.path.join(DIR, "data", "plant_data.csv")
    cost_data_path = os.path.join(DIR, "data", "plantCost.csv")
    capacity_factors_data_path = os.path.join(DIR, "data", "plantCapacityFactor.csv")
    age_data_path = os.path.join(DIR, "data", "plantAge.csv")
    
    plant_data = pandas.read_csv(plant_data_path, header = 1, comment = "#", skip_blank_lines=True)
    cost_data  = pandas.read_csv(cost_data_path, header = 1, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    cf_data    = pandas.read_csv(capacity_factors_data_path, header = 1, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    age_data   = pandas.read_csv(age_data_path, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    
    return plant_data, cost_data, cf_data, age_data
