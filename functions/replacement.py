# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:05:32 2022

@author: jhuster
"""
import cost
import constants
import numpy
from scipy.spatial import distance

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

def estimate_emissions(generation, heatrate, carbon_content):
    """
    Parameters
    ----------
    generation : float
        the amount of electricity generated (kwh)
    heatrate : float
        the efficiency of the power plant (btu/kwh)
    carbon_content : float
        The carbon emissions of the fuel when burned (tonne CO2/btu fuel)

    Returns
    -------
    float
        tonne emitted from burning of the fuel

    """
    return generation*heatrate*carbon_content

def direct_replacement_cost(gen, cf, heatrate, var_om, fix_om, fuel_price, principle_cost, discount_rate, lifetime):
    """
    Estimates the cost of replacing "gen" generation with a new technology with 
    capacity factor "cf" and costs of technologies and lifetimes given in following 
    parameters. 

    Args:
        gen ([float])           : annual generation of electricity (kwh)
        cf  ([float])           : Capacity factor of replacement plant (NA)
        heatrate([float])       : Heatrate of the replacement (btu/kwh)
        var_om ([float])        : Variable cost of operations and maintanace $/Mwh
        fix_om ([float])        : Fixed cost of operations and maintanance $/kw
        fuel_price ([float])    : Cost of fuel input $/mmbtu of fuel
        principle_cost ([float]): Initial capital cost to build plant $/kw
        discount_rate ([float]) : Rate of discount for future income/costs (typically between 5% and 20%)
        lifetime ([float])      : Lifetime for the pay off of capital
        
    Returns:
        [float]: annualized total cost of generating, gen, with parameters provided
    """
    cap = size_capacity(gen, cf)/constants.mw_kw
    fuel = heatrate*gen/constants.mmbtu_btu
    
    return cost.total_cost(var_om, fix_om, fuel_price, principle_cost, discount_rate, lifetime, gen, cap, fuel)

def total_replacement_cost(gen, cf, heatrate, var_om, fix_om, fuel_price, principle_cost, discount_rate, lifetime,
                           o_principle, age, o_rate, o_lifeimte, o_ppy=1):
    """
    Calculate the total cost of replacement (both new capital and remaining historical capital)

    Parameters
    ----------
    gen : float
        the amount of electricity generated (kwh).
    cf : float
        Capacity factor of replacement plant (NA).
    heatrate : float
        Heatrate of the replacement (btu/kwh).
    var_om : float
        Variable cost of operations and maintanace $/Mwh.
    fix_om : float
        Fixed cost of operations and maintanance $/kw.
    fuel_price : float
        Cost of fuel input $/mmbtu of fuel.
    principle_cost : float
        Initial capital cost to build plant $/kw.
    discount_rate : float
        Rate of discount for future income/costs (typically between 5% and 20%).
    lifetime : float
        Lifetime for the pay off of capital.
    o_principle : float
        Original principle to pay off ($).
    age : float
        Current age of the plant (years).
    o_rate : float
        Original discount/interest rate for the initial principle (%).
    o_lifeimte : float
        Original payoff lifetime for the initial principle (years).
    o_ppy : float, optional
        Original payments per year. The default is 1.

    Returns
    -------
    float
        Total annualized cost of replacing initial plant with an updated plant ($/year).

    """
    
    
    
    
    direct_cost = direct_replacement_cost(gen, cf, heatrate, var_om, fix_om, fuel_price, principle_cost, discount_rate, lifetime)
    
    leftover = cost.remaining_capital(o_principle, age, o_rate, o_lifeimte, o_ppy)
    payoff_cost = cost.interval_payment(leftover, discount_rate, lifetime)

    return direct_cost+payoff_cost

def replacement_iteration(var_om, fix_om, fuel_price, principle_cost, discount_rate, lifetime, gen, cap, fuel_dem, age, emissions,
                          cf_dict, cost_dict, emissions_dict, metric=0, subset = ["Gas", "Solar", "Wind"]):
    """
    

    Parameters
    ----------
    var_om : float
        Variable cost of operations and maintanace $/Mwh.
    fix_om : float
        Fixed cost of operations and maintanance $/kw.
    fuel_price : float
        Cost of fuel input $/mmbtu of fuel.
    principle_cost : float
        Initial capital cost to build plant $/kw.
    discount_rate : float
        Rate of discount for future income/costs (typically between 5% and 20%).
    lifetime : float
        Lifetime for the pay off of capital.
    gen : float
        the amount of electricity generated (kwh).
    cap : float
        Capacity of the original plant (mw).
    fuel_dem : float
        Demand for fuel (mmbtu).
    age : float
        Age of current plant (years).
    emissions : float
        Total CO2e emissions (metric tonnes).
    cf_dict : dictionary
        Dictionary of capacity factors of replacement plants (NA).
    cost_dict : dictionary
        Dictionary of costs of replacement plants ($/kw, $/MWh).
    emissions_dict : dictionary
        Dictionary of emissions rates by fuel (tonnes/MWh).
    metric : int, optional
        Which metric to judge by 0: cost, 1: Cost/emissions, 2: emissions. The default is 0.
    subset : list(str), optional
        The subset of options that can replace your plant. The default is ["Gas", "Solar", "Wind"].
        
    Returns
    -------
    fuels : str
        The fuel that should be used to replace.
    costs : float
        The optimal metric cost.
    em_red : float
        Emissions avoided from the choice of fuels at score costs.

    """
    
    
    metrics = {0:dict(zip(subset, [None]*len(subset))), # Cost
               1:dict(zip(subset, [None]*len(subset))), # Ratio cost to emissions
               2:dict(zip(subset, [None]*len(subset))), # Emisisons
               3:dict(zip(subset, [None]*len(subset))), # FOM costs
               4:dict(zip(subset, [None]*len(subset)))} # New Costs
    
    for fuel in subset:
        # Now do each metric 
        existing_cost = cost.total_cost(var_om, fix_om, fuel_price, principle_cost, discount_rate, lifetime, gen, cap, fuel_dem) # we can put cap in if we want to annualize the remaining capital over a new lifetime, but we'll put 0 here. 
        replacement_cost = total_replacement_cost(gen,
                               cf_dict[fuel],
                               cost_dict["heat_rate_btu_per_kwh"][fuel],
                               cost_dict["variable_om_per_mwh"][fuel],
                               cost_dict["fixed_om_per_kw_year"][fuel],
                               cost_dict["fuel_price_per_btu"][fuel],
                               cost_dict["capital_cost_per_kw"][fuel],
                               discount_rate,
                               lifetime,
                               cost_dict["capital_cost_per_kw"][fuel]*constants.mw_kw*cap,
                               age,
                               discount_rate, 
                               lifetime)
        
        new_emissions = estimate_emissions(gen, 
                                           cost_dict["heat_rate_btu_per_kwh"][fuel], 
                                           emissions_dict[fuel])
        
        metrics[0][fuel] = replacement_cost-existing_cost
        metrics[1][fuel] = cost_per_emissions_abated(existing_cost, replacement_cost, emissions, new_emissions)
        metrics[2][fuel] = emissions-new_emissions
        metrics[3][fuel] = existing_cost/gen
        metrics[4][fuel] = replacement_cost/gen
    
    emissions_red = numpy.array(list(metrics[2].values()))
    
    options = numpy.array(list(metrics[metric].values()))
    choices = numpy.argmin(options, axis = 0)
    costs = options[choices, numpy.arange(options.shape[1])]# numpy.amin(options, axis = 0)
    em_red = emissions_red[choices, numpy.arange(options.shape[1])]
    fuels = numpy.array(subset)[choices]
    
    return fuels, costs, em_red

def replacement_df(df, cost_dict, cf_dict, emissions_dict, principle_cost, discount_rate, lifetime, measure_year = 2017, metric=0, subset = ["Gas", "Solar", "Wind"]):
                   
    fuels, costs, em_red = replacement_iteration(df["primary_fuel"].map(cost_dict["variable_om_per_mwh"]),
                                                 df["primary_fuel"].map(cost_dict["fixed_om_per_kw_year"]),
                                                 df["primary_fuel"].map(cost_dict["fuel_price_per_btu"]),
                                                 principle_cost, # plant_data["primary_fuel"].map(cost_dict["capital_cost_per_kw"]),
                                                 discount_rate,
                                                 lifetime,
                                                 df["generation"],
                                                 df["capacity"],
                                                 df["fuel_consumption"],
                                                 measure_year-df["commissioning_year"],
                                                 df["emissions"],
                                                 cf_dict,
                                                 cost_dict,
                                                 emissions_dict,
                                                 metric,
                                                 subset)
    return fuels, costs, em_red

def set_macc(df, neg_cap = -200, cap = 200):
    holder = df[df.metric.between(neg_cap, cap) & (df["em_red"] > 1)]
    holder.sort_values("metric", inplace = True)
    holder["cum_red"] = numpy.cumsum(holder["em_red"])/constants.giga
    holder["cum_red_prev"] = (numpy.cumsum(holder["em_red"])-holder["em_red"])/constants.giga
    holder["ori_rep"] = holder["primary_fuel"]+"_"+holder["rep_fuel"]
    
    return holder

def cost_per_emissions_abated(cost_orig, cost_new, emissions_orig, emissions_new):
    return (cost_new-cost_orig)/(emissions_orig-emissions_new)

def select_cf(loc, data_loc, cf):

    dist_array = distance.cdist(loc, data_loc)
    best_locs = numpy.argmin(dist_array, axis = 1) # the algorithm for best loc could be expanded to include other parameters as well. 
    cf_vals = cf[best_locs]
    
    return cf_vals