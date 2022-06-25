# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 14:14:47 2022

@author: jonat
"""

# Plotting
PAGE_WIDTH = 6.99  # in
ROW_HEIGHT = 2.5  # in

# Physical 
year_hours = 8760

# Energy conversions

# from_to
mw_kw = 1000
mmbtu_btu = 1e6
giga = 1e9

# Mass 
lb_kg = 0.4536
kg_tonne = 0.001

# US States
US_STATES = {"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"}

US_STATE_ABB = {"AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"}

US_CONTINENTAL = {"Alabama","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"}

US_CONTINENTAL_ABB = {"AL","AZ","AR","CA","CO","CT","DE","DC","FL","GA","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"}


# Filtering constraints
min_cf = 0
max_cf = 1.05 

# Default Fossil fuels
default_fossil = ["Coal", "Gas", "Gas_SC", "Gas_CC", "Oil"]

# Default Replacements
default_replacement = ["Gas", "Wind","Solar"]

# Plotting 
colors = {"Coal_Gas":"#f8766d", 
          "Coal_Solar":"#CD9600",
          "Coal_Wind": "#7CAE00",
          "Gas_SC_Gas":  "#00BE67", 
          "Gas_CC_Gas":  "#00BE67",
          "Gas_Gas":  "#00BE67", 
          "Gas_SC_Solar":"#00BFC4",
          "Gas_CC_Solar":"#00BFC4",
          "Gas_Solar":"#ffd700",
          "Gas_SC_Wind":"#00A9FF",
          "Gas_CC_Wind":"#00A9FF",
          "Gas_Wind":"#00A9FF",
          "Oil_Gas":"#C77CFF",
          "Oil_Wind":"#FF61CC",
          "Oil_Solar":"#800000",
         "National":"#a6a6a6"}