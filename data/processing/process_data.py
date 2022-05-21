# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 12:15:26 2022

@author: jonat
"""
import os
import sys

sys.path.insert(0, './EIA/')
sys.path.insert(0, './EIA_CEMS/')

import process_eia_data
import join_CEMS_EIA


def create_path(path):
    '''Helper function to create directories if needed.'''
    if not os.path.exists(path):
        os.makedirs(path)
    return path

if __name__ == '__main__': 
    DIR = create_path('C:\\Users\\jonat\\OneDrive\\Desktop\\General\\School\\Stanford\\Research\\MACC\\MACCpy\\data\\processing')
    EIA_DIR = create_path(os.path.join(DIR,"EIA"))
    CEMS_DIR = create_path(os.path.join(DIR,"CEMS"))
    
    OUT_FILE = os.path.join(DIR,"..", "processed", "plant_data.csv")
    
    
    start_year = 2020
    end_year = 2020
    
    for year in range(start_year, end_year+1):
        # Process EIA
        EIA_RAW_FILE = os.path.join(EIA_DIR, "..", "..", "raw", "EIA", str(year), "3_1_Generator_Y2017.xlsx" )
        EIA_LOC_FILE = os.path.join(EIA_DIR, "..", "..", "raw", "EIA", str(year), "2___Plant_Y2017.xlsx" )
        EIA_FUEL_FILE = os.path.join(EIA_DIR, "eia_tech_mapping.csv" )
        EIA_CLEAN_FILE = os.path.join(EIA_DIR, str(year), "EIA_mapping.csv")
        
        process_eia_data.merge_EIA(EIA_RAW_FILE, EIA_LOC_FILE, EIA_FUEL_FILE, EIA_CLEAN_FILE)    
        
        # Process CEMS
        
        # Join EIA and CEMS
        CEMS_FILE = os.path.join(DIR, "CEMS", str(year), "aggregated_cems.csv")
        join_CEMS_EIA.join_CEMS_EIA(CEMS_FILE, EIA_CLEAN_FILE, OUT_FILE)
    # Write output