# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 22:35:48 2022

@author: jonat
"""
import os 
import pandas as pd
import numpy as np

import constants

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
    
    DATA_DIR = os.path.join(DIR, "data", "processed")
    
    plant_data_path            = os.path.join(DATA_DIR, "plant_data.csv")
    cost_data_path             = os.path.join(DATA_DIR, "plantCost_NREL.csv")
    capacity_factors_data_path = os.path.join(DATA_DIR, "plantCapacityFactor_NREL.csv")
    age_data_path              = os.path.join(DATA_DIR, "plantAge.csv")
    emissions_data_path        = os.path.join(DATA_DIR, "plantEmissions.csv")
    pv_cf_data_path            = os.path.join(DATA_DIR, "pv_open_2020.csv")
    wind_cf_data_path          = os.path.join(DATA_DIR, "Open_Access_Siting_Regime_ATB_Mid_Turbine.csv")
    
    plant_data     = pd.read_csv(plant_data_path, header = 1)
    cost_data      = pd.read_csv(cost_data_path, header = 1, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    cf_data        = pd.read_csv(capacity_factors_data_path, header = 1, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    age_data       = pd.read_csv(age_data_path, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    emissions_data = pd.read_csv(emissions_data_path, header = 1, index_col = "primary_fuel", comment = "#", skip_blank_lines=True)
    pv_cf_data     = pd.read_csv(pv_cf_data_path, comment = "#", skip_blank_lines=True)
    wind_cf_data   = pd.read_csv(wind_cf_data_path, comment = "#", skip_blank_lines=True)
    
    
    return plant_data, cost_data, cf_data, age_data, emissions_data, pv_cf_data, wind_cf_data

def clean_plant_data(df, fuel_subset = ["Coal", "Gas", "Oil"]):
    
    # We'll remove data that has 
    # 1) Missing values in any column
    # 2) Non-positive generation over a year
    # 3) Non-positive emissions over a year (Unclear how BECCS would be treated here)
    # 4) Non-positive capacity
    # 5) Capacity factors less than 0 or greater than 1.05 (allowing some discrepancy and seasonal fluctuations in efficency/capacity)
    
    df_full = df.dropna(inplace = False)
    positive_generation = df_full['generation'] > 0 
    positive_consumption = df_full['fuel_consumption'] > 0
    positive_emissions = df_full['emissions'] > 0
    positive_capacity = df_full['capacity'] > 0
    feasible_cf = (df_full['generation']/(df_full['capacity']*constants.mw_kw*constants.year_hours)).between(constants.min_cf, constants.max_cf)
    in_fuel = df_full.primary_fuel.isin(["Gas", "Coal", "Oil"])

    tests_array = np.array([positive_generation, 
                            positive_consumption, 
                            positive_emissions, 
                            positive_capacity, 
                            feasible_cf, 
                            in_fuel])
    
    return df_full[np.all(tests_array, axis = 0)]


