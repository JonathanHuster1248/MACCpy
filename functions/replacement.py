# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:05:32 2022

@author: jhuster
"""

def size_capacity(gen, cf):
    """
    Parameters
    ----------
    gen : float
        the original generation we are trying to reach
    cf : float between 0 and 1
        A representative capacity factor for the technology

    Returns 
    -------
    capacity of plant with capacity factor cf to reach generation gen.

    """
    
    hours_per_year = 8760
    return gen/(cf*hours_per_year)

def estimate_emissions(generation, heatrate, heat_content, carbon_content):
    """
    Parameters
    ----------
    generation : float
        the amount of electricity generated (kwh)
    heatrate : float
        the efficiency of the power plant (btu/kwh)
    heat_content : float
        The amount of energy in the fuel (btu/kg)
    carbon_content : float
        The carbon emissions of the fuel when burned (kgCO2/kg fuel)

    Returns
    -------
    float
        kgCO2 emitted from burning of the fuel

    """
    return generation*heatrate/heat_content*carbon_content


